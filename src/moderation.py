from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from src.traductor import TraductorM2M100

class Moderation:
    def __init__(self, model_name="cardiffnlp/twitter-roberta-base-offensive"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)  
        
    def validar_moderacion(self, texto: str) -> float:
        traduccion = TraductorM2M100().traducir_a_ingles(texto)
        inputs = self.tokenizer(traduccion, return_tensors="pt", truncation=False, max_length=7500)
        outputs = self.model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)
        # Índice 1 representa contenido ofensivo
        offensive_score = probabilities[0][1].item()
        return offensive_score
