import openpyxl, csv, sys
wb = openpyxl.load_workbook('r.xlsx', data_only=True)
sheet = wb.active
with open('output.txt', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, delimiter='\t')
    for row in sheet.iter_rows(values_only=True):
        writer.writerow(['' if cell is None else cell for cell in row])