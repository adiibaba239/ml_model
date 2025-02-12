import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

# Load the fine-tuned model and tokenizer
model_path = "./fine_tuned_t5"
tokenizer = T5Tokenizer.from_pretrained(model_path)
model = T5ForConditionalGeneration.from_pretrained(model_path)

# Ensure model is in evaluation mode
model.eval()


def format_text(input_text, model, tokenizer, max_length=512):
    """
    Formats the given text using the fine-tuned T5 model.

    Args:
        input_text (str): The unformatted text to process.
        model (T5ForConditionalGeneration): The fine-tuned T5 model.
        tokenizer (T5Tokenizer): The tokenizer used with the model.
        max_length (int): Maximum length of the generated text.

    Returns:
        str: The formatted output text.
    """
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

    with torch.no_grad():
        output = model.generate(**inputs, max_length=max_length)

    return tokenizer.decode(output[0], skip_special_tokens=True)


# Example Usage
if __name__ == "__main__":
    input_text = """page_content='Data Communication and Computer Network 
 74 
When a packet is received by a router has its MF (more fragments) bit set to 1, the 
router then knows that it is  a fragmented packet and parts of the original packet is 
on the way. 
If packet is fragmented too small, the overhead is increases. If the packet is 
fragmented too large, intermediate router may not be able to process it and it might 
get dropped.' metadata={'source': 'C:\\Users\\adity\\Downloads\\data_communication_computer_network_tutorial.pdf', 'page': 81}"""

    formatted_output = format_text(input_text, model, tokenizer)
    print("Formatted Output:\n", formatted_output)
