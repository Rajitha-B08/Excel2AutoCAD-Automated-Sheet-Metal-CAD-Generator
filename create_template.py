import pandas as pd
import os

os.makedirs("templates", exist_ok=True)

plate_data = {
    "length":[200],
    "width":[100],
    "thickness":[10]
}

holes_data = {
    "x":[20,180,20,180],
    "y":[20,20,80,80],
    "diameter":[10,10,10,10]
}

with pd.ExcelWriter("templates/template.xlsx") as writer:
    pd.DataFrame(plate_data).to_excel(writer,sheet_name="Plate",index=False)
    pd.DataFrame(holes_data).to_excel(writer,sheet_name="Holes",index=False)

print("Template created")