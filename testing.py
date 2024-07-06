from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# Load the fine-tuned model
model_name_or_path = "./t5-finetuned-model"  # Path to the fine-tuned model
tokenizer = AutoTokenizer.from_pretrained(model_name_or_path)
model = AutoModelForSeq2SeqLM.from_pretrained(model_name_or_path)

# Define the input prompt
input_prompt = "summarize: Albumin:45.1, Testosterone:17.99, Prolactin:238, Oestradiol:103.2, LH:5.54, FSH:1.98, SHBG:30.25, Testosterone:0.389"

# Tokenize the input prompt
inputs = tokenizer(input_prompt, return_tensors="pt")

# Generate text
output_sequences = model.generate(
    input_ids=inputs["input_ids"],
    max_length=200,  # Maximum length of the generated text
    # num_return_sequences=1,  # Number of sequences to generate
    # no_repeat_ngram_size=2,  # Prevent repeating n-grams
    # do_sample=True,
    # top_k=50,  # Use top-k sampling
    # top_p=0.95,  # Use top-p sampling
    # temperature=1.0,  # Control the randomness of predictions
)

# Decode the generated text
generated_text = tokenizer.decode(output_sequences[0], skip_special_tokens=True)

print(generated_text)
