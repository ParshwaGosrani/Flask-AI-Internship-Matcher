import nltk
from sentence_transformers import SentenceTransformer

def download_all_models():
    """
    Downloads all necessary models for the project.
    Run this script once before starting the web app.
    """
    print("--- Starting Model Download ---")

    # 1. Download NLTK stopwords
    print("Downloading NLTK stopwords...")
    nltk.download('stopwords')
    print("✅ NLTK stopwords downloaded.")

    # 2. Download and cache the Sentence Transformer model
    print("\nDownloading Sentence Transformer model (this may take a few minutes)...")
    model_name = 'distilbert-base-nli-stsb-mean-tokens'
    # This line will download the model and save it to a local cache
    SentenceTransformer(model_name)
    print("✅ Sentence Transformer model downloaded and cached.")

    print("\n--- Setup Complete! You can now run the main application. ---")

if __name__ == '__main__':
    download_all_models()