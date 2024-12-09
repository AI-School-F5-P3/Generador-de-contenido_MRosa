from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from src.traductor import TraductorM2M100
from src.utils import RAISED_HAND, GREEN_CIRCLE, PASTEL_YELLOW, RESET

class Moderation:
    def __init__(self, model_name="cardiffnlp/twitter-roberta-base-offensive"):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)  
        
    def moderate(self, texto: str) -> float:
        print(f"\n{RAISED_HAND} {PASTEL_YELLOW}TEXTO PARA MODERAR -------> {texto}{RESET}\n")
        traduccion = TraductorM2M100().translate_to_english(texto)
        print(f"\n{GREEN_CIRCLE} {PASTEL_YELLOW}TEXTO TRADUCIDO -------> {traduccion}{RESET}\n")
        inputs = self.tokenizer(traduccion, return_tensors="pt", truncation=False, max_length=7500)
        outputs = self.model(**inputs)
        probabilities = torch.softmax(outputs.logits, dim=1)
        # Índice 1 representa contenido ofensivo
        offensive_score = probabilities[0][1].item()
        return offensive_score
