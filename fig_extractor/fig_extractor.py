import fitz  # PyMuPDF
import os

def extract_figures_with_headings(pdf_path, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    doc = fitz.open(pdf_path)  # Open the PDF file
    figures_with_headings = []

    for page_num in range(len(doc)):
        page = doc[page_num]
        images = page.get_images(full=True)  # Get all images on the page

        for img_index, img in enumerate(images):
            # Extract image
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]

            # Save the image
            img_filename = f"{output_folder}/page{page_num + 1}_figure{img_index + 1}.{image_ext}"
            with open(img_filename, "wb") as img_file:
                img_file.write(image_bytes)

            # Locate the text near the image
            bbox = img[1:5]  # Get image bounding box
            nearby_text = page.get_textbox(fitz.Rect(*bbox))  # Extract text around the image

            # Store figure and heading information
            figures_with_headings.append({
                "page": page_num + 1,
                "image_path": img_filename,
                "heading": nearby_text.strip()
            })

    return figures_with_headings


# Usage
pdf_path = r"C:\Users\adity\Downloads\data_communication_computer_network_tutorial.pdf"
output_folder = "extracted_figures"
figures = extract_figures_with_headings(pdf_path, output_folder)

# Print the extracted figures with headings
for item in figures:
    print(f"Page {item['page']}:")
    print(f"Image: {item['image_path']}")
    print(f"Heading: {item['heading']}")
    print("-" * 50)
