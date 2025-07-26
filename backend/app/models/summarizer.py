import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import logging
import time
from typing import Optional
from app.config.settings import settings

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class NewsSummarizer:
    """
    A class to handle news article summarization using BART model
    """
    
    def __init__(self):
        self.model_name = settings.SUMMARIZER_MODEL
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = None
        self.model = None
        self._load_model()
    
    def _load_model(self):
        """Load the BART model and tokenizer"""
        try:
            logger.info(f"Loading model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name)
            self.model.to(self.device)
            self.model.eval()
            logger.info(f"Model loaded successfully on {self.device}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def preprocess_text(self, text: str) -> str:
        """
        Clean and preprocess the input text
        """
        # Remove extra whitespaces and newlines
        text = ' '.join(text.split())
        
        # Truncate text if it's too long for the model
        tokens = self.tokenizer.encode(text, truncation=True, max_length=settings.MAX_INPUT_LENGTH)
        text = self.tokenizer.decode(tokens, skip_special_tokens=True)
        
        return text
    
    def summarize(self, text: str, max_length: Optional[int] = None, min_length: Optional[int] = None) -> dict:
        """
        Summarize the given text using BART model
        
        Args:
            text (str): Input text to summarize
            max_length (int, optional): Maximum length of summary
            min_length (int, optional): Minimum length of summary
            
        Returns:
            dict: Summary results with metadata
        """
        start_time = time.time()
        
        try:
            # Set default values
            max_length = max_length or settings.MAX_OUTPUT_LENGTH
            min_length = min_length or settings.MIN_OUTPUT_LENGTH
            
            # Ensure min_length is less than max_length
            if min_length >= max_length:
                min_length = max_length - 20
                
            # Preprocess the text
            processed_text = self.preprocess_text(text)
            original_length = len(text.split())
            
            # Tokenize input
            inputs = self.tokenizer.encode(
                processed_text,
                return_tensors="pt",
                truncation=True,
                max_length=settings.MAX_INPUT_LENGTH
            ).to(self.device)
            
            # Generate summary
            with torch.no_grad():
                summary_ids = self.model.generate(
                    inputs,
                    max_length=max_length,
                    min_length=min_length,
                    length_penalty=2.0,
                    num_beams=4,
                    early_stopping=True,
                    no_repeat_ngram_size=3
                )
            
            # Decode summary
            summary = self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
            summary_length = len(summary.split())
            processing_time = time.time() - start_time
            
            logger.info(f"Summarization completed in {processing_time:.2f} seconds")
            
            return {
                "summary": summary,
                "original_length": original_length,
                "summary_length": summary_length,
                "processing_time": processing_time
            }
            
        except Exception as e:
            logger.error(f"Error during summarization: {str(e)}")
            raise
    
    def is_model_loaded(self) -> bool:
        """Check if model is properly loaded"""
        return self.model is not None and self.tokenizer is not None

# Global summarizer instance
summarizer = None

def get_summarizer() -> NewsSummarizer:
    """Get or create the global summarizer instance"""
    global summarizer
    if summarizer is None:
        summarizer = NewsSummarizer()
    return summarizer
