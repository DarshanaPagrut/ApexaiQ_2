import pdfplumber
import pandas as pd

pdf_path = "Windows-and-Office-Configuration-Support-Matrix-2024-10-01.pdf"

tables_list = []  # To store all tables

with pdfplumber.open(pdf_path) as pdf:
    for page_num, page in enumerate(pdf.pages, start=1):
        tables = page.extract_tables()
        if tables:
            for table in tables:
                df = pd.DataFrame(table)
                print(f"\n--- Page {page_num} ---\n")
                print(df.to_string(index=False))
                tables_list.append(df)


if tables_list:
    combined_df = pd.concat(tables_list, ignore_index=True)
    # print("\n=== Combined Table Data ===\n")
    # print(combined_df.to_string(index=False))

combined_df.to_csv("extracted_tables.csv", index=False)

