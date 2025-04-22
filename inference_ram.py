import os
import torch
from PIL import Image
import pandas as pd
from transformers import CLIPProcessor, CLIPModel
import logging
from datetime import datetime

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('poster_analysis.log'),
        logging.StreamHandler()
    ]
)

# Define categories for metadata generation
subjects = ['person', 'flower', 'art', 'sculpture', 'dance', 'festival']
styles = ['modern', 'contemporary', 'abstract', 'minimalist', 'surreal']
colors = ['red', 'blue', 'pink', 'green', 'black', 'white']

def classify_scene_type(tags):
    scene_types = {
        'indoor': ['room', 'interior', 'studio', 'gallery'],
        'outdoor': ['beach', 'sea', 'sky', 'nature', 'garden'],
        'urban': ['city', 'street', 'architecture', 'building'],
        'abstract': ['abstract', 'pattern', 'texture', 'design']
    }
    
    for scene_type, keywords in scene_types.items():
        if any(keyword in tags for keyword in keywords):
            return scene_type
    return 'mixed'

def generate_metadata(file_path, tags, caption):
    metadata = {
        'file_path': file_path,
        'file_name': os.path.basename(file_path)
    }

    # Use tags for title and tags
    subject = next((tag for tag in tags if tag in subjects), 'art')
    style = next((tag for tag in tags if tag in styles), 'modern')
    color = next((tag for tag in tags if tag in colors), '')
    
    # Generate title
    title_parts = [style.capitalize(), subject.capitalize()]
    if color:
        title_parts.append(color.capitalize())
    title_parts.append('Art Print')
    metadata['title'] = ' '.join(title_parts)
    
    # Generate SEO title
    seo_title_parts = [style.capitalize(), subject.capitalize()]
    if color:
        seo_title_parts.append(color.capitalize())
    seo_title_parts.extend(['Wall Art', '|', 'Modern Home Decor'])
    metadata['seo_title'] = ' '.join(seo_title_parts)

    # Generate alt text
    background_elements = [tag for tag in tags if tag in ['beach', 'sea', 'sky', 'room', 'studio']]
    color_elements = [tag for tag in tags if tag in colors]
    main_elements = [tag for tag in tags if tag in subjects]
    
    alt_text_parts = [
        f"A {style} art print featuring {', '.join(main_elements)}" if main_elements else f"A {style} art print",
        f"Set against a {', '.join(background_elements)} background" if background_elements else "",
        f"Rendered in {', '.join(color_elements)} tones" if color_elements else "",
        f"With {', '.join([tag for tag in tags if tag not in main_elements + background_elements + color_elements])} elements" if [tag for tag in tags if tag not in main_elements + background_elements + color_elements] else ""
    ]
    metadata['alt_text'] = '. '.join(filter(None, alt_text_parts)) + '.'

    # Generate SEO description
    seo_desc_parts = [
        f"Transform your space with this {style} art print",
        f"featuring {', '.join(main_elements)}" if main_elements else "",
        f"set against {', '.join(background_elements)}" if background_elements else "",
        f"rendered in {', '.join(color_elements)} tones" if color_elements else "",
        "Professionally printed on premium paper",
        "Perfect for modern home decor"
    ]
    metadata['seo_description'] = '. '.join(filter(None, seo_desc_parts)) + '.'

    # Generate and organize tags
    base_tags = ['interior design', 'premium print', 'wall art', 'gallery quality', 'art print', 'modern decor', 'room decor', 'home decor']
    scene_type = classify_scene_type(tags)
    all_tags = set(tags + base_tags + [scene_type])
    metadata['tags'] = ', '.join(all_tags)

    return metadata

def update_csv(metadata, csv_path):
    try:
        # Read existing CSV if it exists
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            logging.info(f"Read existing CSV with {len(df)} rows")
        else:
            df = pd.DataFrame(columns=['file_path', 'file_name', 'title', 'seo_title', 'alt_text', 'seo_description', 'tags'])
        
        # Convert metadata to a DataFrame row format
        metadata_row = pd.DataFrame([{
            'file_path': str(metadata['file_path']),
            'file_name': str(metadata['file_name']),
            'title': str(metadata['title']),
            'seo_title': str(metadata['seo_title']),
            'alt_text': str(metadata['alt_text']),
            'seo_description': str(metadata['seo_description']),
            'tags': str(metadata['tags'])
        }])
        
        # Check if file already exists in CSV
        existing_idx = df.index[df['file_path'] == metadata['file_path']].tolist()
        
        if existing_idx:
            # Update existing row
            df.loc[existing_idx[0]] = metadata_row.iloc[0]
            logging.info(f"✓ Updated existing row for: {metadata['file_name']}")
        else:
            # Append new row
            df = pd.concat([df, metadata_row], ignore_index=True)
            logging.info(f"✓ Added new row for: {metadata['file_name']}")
        
        # Save to CSV
        df.to_csv(csv_path, index=False)
        logging.info(f"Successfully saved metadata for: {metadata['file_name']}")
        
    except Exception as e:
        logging.error(f"Error updating CSV: {str(e)}")
        raise

def analyze_image(image_path, processor, model):
    # Load and process image
    image = Image.open(image_path)
    inputs = processor(images=image, return_tensors="pt", padding=True)
    
    # Get model predictions
    with torch.no_grad():
        outputs = model.get_image_features(**inputs)
        outputs = outputs / outputs.norm(dim=-1, keepdim=True)  # Normalize image features
        
        # Get text features for common tags
        candidate_labels = [
            "person", "flower", "art", "sculpture", "dance", "festival",
            "beach", "sea", "sky", "room", "studio",
            "red", "blue", "pink", "green", "black", "white",
            "modern", "contemporary", "abstract", "minimalist", "surreal"
        ]
        text_inputs = processor(text=candidate_labels, return_tensors="pt", padding=True)
        text_features = model.get_text_features(**text_inputs)
        text_features = text_features / text_features.norm(dim=-1, keepdim=True)  # Normalize text features
        
        # Calculate similarity scores
        similarity = (100.0 * outputs @ text_features.T).squeeze()
        
        # Get tags above threshold
        threshold = 20.0  # Adjusted threshold for cosine similarity
        tags = [label for score, label in zip(similarity, candidate_labels) if score > threshold]
    
    return tags

def main():
    try:
        # Initialize model and processor
        processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
        model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
        
        # Set paths
        posters_dir = "/Users/tatiana/Downloads/April 17 - Poster Analysis/posters"
        csv_path = "/Users/tatiana/Downloads/April 17 - Poster Analysis/all_posters_analysis.csv"
        
        # Get list of image files
        image_files = [f for f in os.listdir(posters_dir) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        total_images = len(image_files)
        
        logging.info(f"Found {total_images} images to process")
        
        # Process each image
        for idx, image_file in enumerate(image_files, 1):
            try:
                image_path = os.path.join(posters_dir, image_file)
                logging.info(f"\nProcessing image {idx}/{total_images}: {image_file}")
                logging.info(f"Full image path: {image_path}")
                
                # Analyze image and get tags
                tags = analyze_image(image_path, processor, model)
                logging.info(f"Generated tags: {tags}")
                
                # Generate caption from tags
                caption = f"A artistic image featuring {', '.join(tags[:3])}"
                
                # Generate metadata
                metadata = generate_metadata(image_path, tags, caption)
                logging.info(f"Generated metadata: {metadata}")
                
                # Update CSV
                update_csv(metadata, csv_path)
                logging.info(f"✓ Generated metadata for: {image_file}")
                logging.info(f"  Title: {metadata['title']}")
                logging.info(f"  Tags: {len(tags)} tags generated")
                
            except Exception as e:
                logging.error(f"Error processing image {image_file}: {str(e)}")
                continue
        
        logging.info("\nBatch processing complete!")
        
    except Exception as e:
        logging.error(f"Error in main execution: {str(e)}")
        raise

if __name__ == "__main__":
    main()