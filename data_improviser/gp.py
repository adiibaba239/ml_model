from langchain_community.document_loaders import PyPDFLoader

# Load the PDF document
loader = PyPDFLoader(r"C:\Users\adity\Downloads\data_communication_computer_network_tutorial.pdf")
docs = loader.load()

# Join all page contents into a single text block
full_text = " ".join(doc.page_content for doc in docs)

# Split based on word count
def split_text_by_word_count(text, words_per_chunk=1500):
    words = text.split()  # Split by spaces to get individual words
    chunks = [" ".join(words[i:i + words_per_chunk]) for i in range(0, len(words), words_per_chunk)]
    return chunks

# Get the text chunks
text_chunks = split_text_by_word_count(full_text, words_per_chunk=1500)

# Print each part
for idx, chunk in enumerate(text_chunks):
    print(f"Part {idx + 1}:\n")
    print(chunk)
    print("\n" + "-" * 50 + "\n")
