import pdfplumber
import pandas as pd

with pdfplumber.open("Pharmacy_Doctor Scenario.pdf") as pdf:
        first_page = pdf.pages[0]
        tables = first_page.extract_tables()

if tables:
        df = pd.DataFrame(tables[0])
        print(df)
else:
        print("No tables found on the first page.")

df.to_excel("extracted_table.xlsx", index=False)
print("Saved to extracted_table.xlsx.")