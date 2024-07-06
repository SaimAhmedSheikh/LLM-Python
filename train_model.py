from transformers import Trainer, TrainingArguments, AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset

# Load dataset
dataset = load_dataset('csv', data_files={"train":'train.csv', 'test': 'test.csv'}, delimiter='|')

# Check if the dataset has splits
if 'train' not in dataset:
    dataset = dataset.train_test_split(test_size=0.1)

print(dataset['train'].to_pandas().count())
print(dataset['test'].to_pandas().count())

# Initialize tokenizer and model
model_name = "EleutherAI/gpt-neo-2.7B"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
# Add a padding token to the tokenizer
tokenizer.pad_token = tokenizer.eos_token

# Tokenize the dataset
def preprocess_function(examples):
    inputs = examples['Results']
    targets = examples['Summary']
    model_inputs = tokenizer(inputs, max_length=512, truncation=True, padding='max_length', )
    labels = tokenizer(targets, max_length=512, truncation=True, padding='max_length')
    model_inputs["labels"] = labels["input_ids"]
    return model_inputs

tokenized_dataset = dataset.map(preprocess_function, batched=True, remove_columns=dataset["train"].column_names)

# Fine-tune the model
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=2,
    per_device_eval_batch_size=2,
    num_train_epochs=3,
    weight_decay=0.01,
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    eval_dataset=tokenized_dataset["test"],
)

trainer.train()
