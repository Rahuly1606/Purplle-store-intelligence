import pandas as pd

excel_file = r"data/layouts/Brigade Road - Store layout.xlsx"

xls = pd.ExcelFile(excel_file)

print("\nSHEETS:")
print(xls.sheet_names)

for sheet in xls.sheet_names:

    print("\n" + "=" * 60)
    print(f"SHEET: {sheet}")
    print("=" * 60)

    df = pd.read_excel(
        excel_file,
        sheet_name=sheet
    )

    print(df.head(10))