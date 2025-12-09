# Brain Tumor Classification API

Deep learning-based brain tumor classification using Vision Transformer (ViT).

## Features
- 4-class classification: Glioma, Meningioma, No Tumor, Pituitary
- REST API with Flask
- Docker support
- Production-ready deployment

## Quick Start

### Local Development
pip install -r requirements.txt
python run.py### Docker
docker build -t brain-tumor-api .
docker run -p 8000:8000 brain-tumor-api### API Endpoints
- `GET /` - Web interface
- `POST /predict` - Upload image for classification
- `GET /health` - Health check

## Model
- Architecture: Vision Transformer (ViT-Base)
- Input: 224x224 RGB images
- Classes: 4 tumor types