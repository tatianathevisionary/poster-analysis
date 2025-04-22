import sys
import torch
import transformers
import PIL
import pandas
import numpy
import tqdm

def test_installation():
    print("Testing installation...")
    
    # Test Python version
    print(f"Python version: {sys.version}")
    
    # Test PyTorch
    print(f"PyTorch version: {torch.__version__}")
    print(f"CUDA available: {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"CUDA version: {torch.version.cuda}")
    
    # Test other dependencies
    print(f"Transformers version: {transformers.__version__}")
    print(f"Pillow version: {PIL.__version__}")
    print(f"Pandas version: {pandas.__version__}")
    print(f"NumPy version: {numpy.__version__}")
    print(f"Tqdm version: {tqdm.__version__}")
    
    print("\nAll dependencies installed successfully!")

if __name__ == "__main__":
    test_installation() 