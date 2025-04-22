# MetaPosters.ai - AI-Powered Poster Art Store

A sophisticated system for analyzing and generating metadata for poster images using state-of-the-art AI models.

## Features

- **Advanced Image Analysis**: Utilizes the RAM (Recognize Anything Model) for comprehensive image understanding
- **Intelligent Tagging**: Automatically generates relevant tags and categories
- **Scene Classification**: Identifies scene types (indoor, outdoor, abstract, etc.)
- **Cohesion Scoring**: Evaluates image composition and visual harmony
- **Metadata Generation**: Creates SEO-optimized titles, descriptions, and alt text
- **CSV Export**: Saves all metadata in a structured format for easy integration

## Requirements

- Python 3.8+
- PyTorch 2.0+
- CUDA-capable GPU (recommended)
- 8GB+ RAM

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/poster-automation.git
cd poster-automation
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

1. Place your poster images in the `input/` directory
2. Run the analysis script:
```bash
python inference_ram.py
```

3. Check the results:
- Generated metadata will be saved in `output/metadata.csv`
- Logs are available in `poster_analysis.log`

## Directory Structure

```
poster-automation/
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

## Output Format

The generated CSV file includes:
- Image path
- Generated title
- Alt text
- SEO description
- Tags
- Scene type
- Cohesion score

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