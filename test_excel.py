import pandas as pd

def read_excel(file):
    plate = pd.read_excel(file, sheet_name="Plate")
    holes = pd.read_excel(file, sheet_name="Holes")
    return plate, holes

plate, holes = read_excel("template\Plate_template.xlsx")

print(plate)
print(holes)