from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PyPDFLoader

import csv
# Load the PDF document
loader = PyPDFLoader(r"C:\Users\adity\Downloads\An Introduction to Programming and Computer Science with Python, Clayton Cafiero.pdf")
docs = loader.load()

# Join the text from all pages (assuming docs contains multiple pages)
full_text = " ".join(doc.page_content for doc in docs)

# Split the text after every 1500 words
splitter = RecursiveCharacterTextSplitter(chunk_size=5000, chunk_overlap=500)
text_chunks = splitter.split_text(full_text)


# Print the parts separately
r"""
for idx, chunk in enumerate(text_chunks):
    print(f"Part {idx + 1}:")
    print(chunk)
    print("\n" + "-" * 50 + "\n")"""
c=1
import google.generativeai as genai

# Initialize Pinecone client
genai.configure(api_key='AIzaSyCay112ajwakcbG6l5wTLK5WTSKBlzJH44')

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

model = genai.GenerativeModel(
    model_name="gemini-pro",
    safety_settings=safety_settings
)

# Memory to store previous interactions
memory = []

def format_memory(memory):
    formatted_memory = ""
    for interaction in memory:
        formatted_memory += f"User: {interaction['query']}\nAssistant: {interaction['response']}\n"
    return formatted_memory

def generate_response(text_chunk):
    global memory

    # Format the memory of previous interactions
    context = format_memory(memory)


    prompt = (
        f"""
    Act as a content formatter. Your task is to take the provided unformatted document and transform it into a structured and well-formatted output based on the information provided.

    ### Formatting Instructions:

    1. **Content Structuring:**  
       - Identify key sections and organize them under appropriate headings and subheadings.
       - Ensure logical flow and clarity in the content.

    2. **Metadata Inclusion:**  
       - Include all metadata such as page numbers, line numbers, and source names as provided.
       - Clearly indicate the metadata at the beginning or in relevant sections.

    3. **Code Formatting:**  
       - If there is any code, provide it with proper syntax highlighting and enclose it within triple backticks.
       - Mention the programming language before the triple backticks.

       Example:
       ```python
       # Python code example
       print("Hello, World!")
       
    4.give difference in tabular format if possible 
    5.include examples clearly if provided   
    6.do not generate any content by your self just format privided content also keep answers in breif do not cut short it just put it full content as it is without changing any thing
    if content is of 1000 words give all 1000 words do not cut short it stirictly follow this rule no content or should be modified give exact same length content as provided
    content={text_chunk}

"""
                )


    result = model.generate_content(contents=prompt)
    response =result.text


    # Save the current interaction in memory
    #memory.append({"query": query, "response": response})
    #print(response)
    return response
 # Change to "professional" for professional mode

with open('formatted_text.csv', mode='a', encoding='utf-8') as csvfile:
    fieldnames = ['Unformatted_Text', 'Formatted_Text']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    # Write header if the file is empty
    csvfile.seek(0, 2)
    if csvfile.tell() == 0:
        writer.writeheader()

    # Iterate over each document, split, and append to CSV
    for doc in docs:
        # Split the document into chunks using the splitter
        text_chunks = splitter.split_documents([doc])

        for text_chunk in text_chunks:
            print(text_chunk ,"\n\n\n/")

            # Generate a formatted response for each chunk
            formatted_text = generate_response(text_chunk)
            print("this is formatted text\n\n ",formatted_text)

            # Append the unformatted text chunk and the formatted response to the CSV
            writer.writerow({
                'Unformatted_Text': text_chunk,
                'Formatted_Text': formatted_text
            })

print("Data has been successfully written to CSV.")