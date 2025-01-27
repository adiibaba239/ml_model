from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter

# Load the PDF
loader = PyPDFLoader(r"C:\data_communication_computer_network_tutorial.pdf")
docs = loader.load()

# Specify the chunk size
chunk_size = 400
chunk_overlap = 50  # Optional: overlap between chunks for context

# Initialize the text splitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=chunk_size,
    chunk_overlap=chunk_overlap
)

# Break each document into chunks
all_chunks = []
for doc in docs:
    chunks = text_splitter.split_text(doc.page_content)
    all_chunks.extend(chunks)

# Print the chunks
for i, chunk in enumerate(all_chunks):
    print(f"Chunk {i+1}:\n{chunk}\n")
