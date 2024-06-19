import PyPDF2
import pandas as pd

# Open the PDF file
with open('example.pdf', 'rb') as pdf_file:
    # Create a PDF reader object
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    
    # Initialize an empty list to store extracted text
    text_data = []
    
    # Loop through each page in the PDF
    for page_num in range(pdf_reader.numPages):
        # Extract text from the page
        page_text = pdf_reader.getPage(page_num).extractText()
        
        # Append the extracted text to the list
        text_data.append(page_text)
        
# Create a DataFrame from the extracted text
df = pd.DataFrame(text_data, columns=['Text'])

# Write DataFrame to CSV file
df.to_csv('output.csv', index=False)
