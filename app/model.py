#!/usr/bin/env python3
import sys, os, torch, torch.nn as nn, torchvision.transforms as T
from PIL import Image
import timm, torch.nn.functional as F

# ---------- config ----------
IMG_SIZE   = 224
# Remove hardcoded path - will be set from Flask config
CHECKPOINT = None
CLASS_NAMES = ['glioma', 'meningioma', 'no tumor', 'pituitary']
# Use CPU by default (works everywhere including EC2)
DEVICE     = torch.device("cpu")
# ----------------------------

# Model will be loaded lazily
model = None
transform = None

def initialize_model(model_path, device='cpu'):
    """Initialize model with given path and device"""
    global model, transform, CHECKPOINT, DEVICE
    
    CHECKPOINT = model_path
    DEVICE = torch.device(device)
    
    # build model arch (must match training)
    model = timm.create_model("vit_base_patch16_224", pretrained=False, num_classes=len(CLASS_NAMES))
    model.head = nn.Linear(model.head.in_features, len(CLASS_NAMES))
    model = model.to(DEVICE)
    
    # load your fine-tuned weights
    model.load_state_dict(torch.load(CHECKPOINT, map_location=DEVICE))
    model.eval()
    
    # preprocessing
    transform = T.Compose([
        T.Resize((IMG_SIZE, IMG_SIZE)),
        T.ToTensor(),
        T.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

def predict_image(image_path):
    """Predict and return results as dictionary"""
    if model is None:
        raise RuntimeError("Model not initialized. Call initialize_model() first.")
    
    img = Image.open(image_path).convert('RGB')
    x = transform(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        logits = model(x)
        probs  = F.softmax(logits, dim=1).cpu().numpy().ravel()

    top = probs.argmax()
    prediction = CLASS_NAMES[top]
    confidence = float(probs[top])
    
    # Return data instead of printing
    return {
        'prediction': prediction,
        'confidence': confidence,
        'all_probabilities': {CLASS_NAMES[i]: float(probs[i]) for i in range(len(CLASS_NAMES))}
    }

if __name__ == "__main__":
    # CLI usage
    if len(sys.argv) != 2:
        print("Usage: python predict.py <image_path>")
        sys.exit(1)
    
    # For CLI, use hardcoded path
    initialize_model("models/best_vit_brain_tumor.pth")
    result = predict_image(sys.argv[1])
    
    print(f"Predicted: {result['prediction']} ({result['confidence']:.1%})")
    for cls, p in result['all_probabilities'].items():
        print(f"{cls:>12}: {p:>6.1%}")