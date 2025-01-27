from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader(
    r"C:\Users\adity\Downloads\data_communication_computer_network_tutorial.pdf",
)
docs = loader.load()
#print(docs)
chunk_size=400
i=0

 for chunk_size in docs:
    print(chunk_size)
