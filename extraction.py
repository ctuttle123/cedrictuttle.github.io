import pdfplumber

with pdfplumber.open("Pharmacy_Doctor Scenario.pdf") as pdf:
    # access the first page
    first_page = pdf.pages[0]
    # extract text from first page
    text = first_page.extract_text()

    with open("extracted_text.txt", "w", encoding="utf-8") as f:
        f.write(text)

    print("Text from first page has been saved to 'extracted_text.txt'.")