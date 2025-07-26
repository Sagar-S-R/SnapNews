from transformers import DPRQuestionEncoderTokenizer, DPRQuestionEncoder
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch
import numpy as np
import faiss
import os
from app.config.settings import settings

# Load pre-trained models
def load_models():
    model_path = settings.MODEL_PATH
    
    # Load DPR models for retrieval
    dpr_tokenizer = DPRQuestionEncoderTokenizer.from_pretrained(
        os.path.join(model_path, "dpr_tokenizer")
    )
    dpr_model = DPRQuestionEncoder.from_pretrained(
        os.path.join(model_path, "dpr_model")
    )
    
    # Load generator models for summarization
    generator_tokenizer = AutoTokenizer.from_pretrained(
        os.path.join(model_path, "generator_tokenizer")
    )
    generator_model = AutoModelForSeq2SeqLM.from_pretrained(
        os.path.join(model_path, "generator_model")
    )
    
    # Set models to evaluation mode
    dpr_model.eval()
    generator_model.eval()
    
    return dpr_tokenizer, dpr_model, generator_tokenizer, generator_model

# Initialize models
dpr_tokenizer, dpr_model, generator_tokenizer, generator_model = load_models()

# Load or create FAISS index
def load_or_create_faiss_index(embeddings_path, dimension=768):
    """Load existing FAISS index or create a new one"""
    index_path = os.path.join(settings.MODEL_PATH, "faiss_index")
    
    if os.path.exists(index_path):
        # Load existing index
        index = faiss.read_index(index_path)
        # Load embeddings
        document_embeddings = np.load(embeddings_path)
        return index, document_embeddings
    else:
        # Create a new index
        index = faiss.IndexFlatL2(dimension)
        return index, None

# Encode corpus for retrieval
def encode_corpus(corpus):
    """Encode a list of documents using the DPR model"""
    encoded_corpus = []
    
    for doc in corpus:
        inputs = dpr_tokenizer(doc, return_tensors="pt", max_length=512, truncation=True)
        with torch.no_grad():
            outputs = dpr_model(**inputs)[0]
        encoded_corpus.append(outputs.numpy())
    
    # Convert to numpy array and reshape
    encoded_corpus = np.vstack(encoded_corpus)
    
    return encoded_corpus

# Build FAISS index
def build_faiss_index(document_embeddings):
    """Build a FAISS index from document embeddings"""
    dimension = document_embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(document_embeddings)
    
    # Save the index
    index_path = os.path.join(settings.MODEL_PATH, "faiss_index")
    faiss.write_index(index, index_path)
    
    return index

# Retrieve relevant documents
def retrieve_documents(query, index, document_embeddings, corpus, top_k=3):
    """Retrieve the top-k relevant documents for a query"""
    # Encode the query
    inputs = dpr_tokenizer(query, return_tensors="pt", max_length=512, truncation=True)
    with torch.no_grad():
        query_embedding = dpr_model(**inputs)[0].numpy()
    
    # Search the index
    D, I = index.search(query_embedding, top_k)
    
    # Get the retrieved documents
    retrieved_docs = [corpus[i] for i in I[0]]
    
    return retrieved_docs

# Summarize text
def generate_summary(text, max_length=150):
    """Generate a summary for the given text"""
    inputs = generator_tokenizer(text, return_tensors="pt", max_length=1024, truncation=True)
    
    with torch.no_grad():
        summary_ids = generator_model.generate(
            inputs["input_ids"],
            num_beams=4,
            max_length=max_length,
            early_stopping=True,
            no_repeat_ngram_size=3
        )
    
    summary = generator_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    return summary

# Main RAG summarization function
def rag_summarize(text, corpus=None, index=None, document_embeddings=None):
    """
    Summarize text using RAG approach.
    If corpus, index, and document_embeddings are not provided,
    it will simply summarize the input text without retrieval.
    """
    # If retrieval parameters are provided, use RAG approach
    if corpus and index and document_embeddings is not None:
        # Retrieve relevant documents
        retrieved_docs = retrieve_documents(text, index, document_embeddings, corpus)
        
        # Combine original text with retrieved documents
        context = " ".join(retrieved_docs)
        combined_text = f"{text} Context: {context}"
        
        # Generate summary
        summary = generate_summary(combined_text)
    else:
        # Simple summarization without retrieval
        summary = generate_summary(text)
    
    return summary