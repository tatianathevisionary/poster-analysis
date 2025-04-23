# Image Analysis and Metadata Generator

A Python-based tool for analyzing images and generating structured metadata in CSV format. This tool processes images to extract meaningful information and organizes it into a structured format for easy integration with other systems.

## Features

- **Image Analysis**: Processes images to extract visual features and characteristics
- **Metadata Generation**: Creates structured data including:
  - Image titles
  - Alt text descriptions
  - SEO-optimized descriptions
  - Scene classification (indoor, outdoor, abstract, etc.)
  - Visual cohesion scores
  - Relevant tags and categories
- **CSV Export**: Saves all generated metadata in a structured CSV format
- **Batch Processing**: Handles multiple images in a single run
- **Progress Tracking**: Shows real-time progress of image processing

## Requirements

- Python 3.8+
- PyTorch 2.0+
- CUDA-capable GPU (recommended)
- 8GB+ RAM

## Installation

1. Clone the repository:
```bash
git clone https://github.com/tatianathevisionary/poster-analysis.git
cd poster-analysis
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Test the installation:
```bash
python test_installation.py
```

## Usage

1. Place your images in the `input/` directory
2. Run the analysis script:
```bash
python inference_ram.py
```

3. Check the results:
- Generated metadata will be saved in `output/metadata.csv`
- Logs are available in `poster_analysis.log`

## CSV Output Format

The generated CSV file (`output/metadata.csv`) includes the following columns:
- `image_path`: Path to the processed image
- `title`: Generated title for the image
- `alt_text`: Descriptive alt text for accessibility
- `seo_description`: SEO-optimized description
- `tags`: Comma-separated list of relevant tags
- `scene_type`: Classification of the scene (indoor, outdoor, abstract, etc.)
- `cohesion_score`: Numerical score indicating visual harmony (0-1)

## Directory Structure

```
poster-analysis/
├── input/              # Place your images here
├── output/             # Generated metadata and results
├── ram/               # RAM model files
├── pretrained/        # Pretrained models
├── inference_ram.py   # Main analysis script
├── test_installation.py
├── requirements.txt
├── README.md
└── LICENSE
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

For support, please open an issue in the GitHub repository or contact support@metaposters.ai 