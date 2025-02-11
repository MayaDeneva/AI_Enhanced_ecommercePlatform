from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import pickle

# Define paths
model_path = "D:/UNI/4 kurs/GENAI/Project1/.venv/bert_product_classifier"
label_encoder_path = "D:/UNI/4 kurs/GENAI/Project1/.venv/bert_product_classifier/label_encoder.pkl"

# Load trained model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)

import pickle

label_encoder_path = "D:/UNI/4 kurs/GENAI/Project1/.venv/bert_product_classifier/label_encoder.pkl"

# Load label encoder with explicit binary mode
try:
    with open(label_encoder_path, "rb") as f:
        label_encoder = pickle.load(f)
    print("Label encoder loaded successfully!")
except Exception as e:
    print(f"❌ Error loading label_encoder: {e}")


# Function to predict category
def predict_category(product_title):
    inputs = tokenizer(product_title, return_tensors="pt", padding="max_length", truncation=True, max_length=128)
    outputs = model(**inputs)
    predicted_label = torch.argmax(outputs.logits, dim=1).item()
    return label_encoder.inverse_transform([predicted_label])[0]

# # Example Prediction
# product_title = "Protein Powder"
# predicted_category = predict_category(product_title)
# print(f"Predicted Category: {predicted_category}")
