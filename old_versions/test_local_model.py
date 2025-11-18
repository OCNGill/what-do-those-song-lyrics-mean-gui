"""
Quick test to verify local model loads and works.
"""
import logging

logging.basicConfig(level=logging.INFO)

print("Testing local model setup...")
print("1. Importing transformers...")

try:
    from transformers import pipeline
    print("   ✓ transformers imported successfully")
except ImportError as e:
    print(f"   ✗ Failed to import transformers: {e}")
    print("   Run: pip install transformers torch sentencepiece")
    exit(1)

print("\n2. Loading model (google/flan-t5-small)...")
print("   Note: First run will download ~80MB model")

try:
    model = pipeline(
        "text2text-generation",
        model="google/flan-t5-small",
        device=-1,  # CPU only
        max_length=256,
    )
    print("   ✓ Model loaded successfully")
except Exception as e:
    print(f"   ✗ Failed to load model: {e}")
    exit(1)

print("\n3. Testing inference with sample text...")

test_prompt = """
Analyze these song lyrics and explain:
1. The main theme
2. Key symbolic meanings
3. The emotional message

Lyrics:
We all live in a yellow submarine
Yellow submarine, yellow submarine

Interpretation:
"""

try:
    result = model(test_prompt, max_length=150, do_sample=False)
    interpretation = result[0]['generated_text'].strip()
    
    print("   ✓ Inference successful!")
    print("\n" + "="*60)
    print("SAMPLE OUTPUT:")
    print("="*60)
    print(interpretation)
    print("="*60)
    
except Exception as e:
    print(f"   ✗ Inference failed: {e}")
    exit(1)

print("\n✓ All tests passed! Local model is ready to use.")
print("  You can now run the app with: streamlit run app.py")
