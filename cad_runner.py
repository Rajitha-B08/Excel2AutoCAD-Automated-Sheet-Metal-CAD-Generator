import sys
import os

# FreeCAD path
FREECADPATH = r"C:\Program Files\FreeCAD 1.0\bin"
sys.path.append(FREECADPATH)

import FreeCAD

# Project directory
PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(PROJECT_DIR)

from excel_reader import read_excel

# Product argument passed after "--"
product = sys.argv[-1]

print("Running CAD generation for:", product)

# Map product names to their actual template file names
TEMPLATE_MAP = {
    "plate":         "Plate_template.xlsx",
    "bracket":       "bracket_template.xlsx",
    "flange":        "flange_template.xlsx",
    "motor_mount":   "motor_mount_template.xlsx",
    "gear_plate":    "gear_plate_template.xlsx",
    "u_channel":     "u_channel.xlsx",
    "machine_frame": "machine_frame.xlsx",
    "enclosure":     "enclosure.xlsx",
    "control_box":   "control_box.xlsx",
    "cabinet":       "cabinet.xlsx",
}

# Resolve Excel file: first check template/ folder, then project root
template_name = TEMPLATE_MAP.get(product, product + ".xlsx")
input_file = os.path.join(PROJECT_DIR, "template", template_name)
if not os.path.exists(input_file):
    # Fallback: look in project root (for uploaded files via Streamlit)
    input_file = os.path.join(PROJECT_DIR, product + ".xlsx")
if not os.path.exists(input_file):
    input_file = os.path.join(PROJECT_DIR, "input.xlsx")

# Output directory
output_dir = os.path.join(PROJECT_DIR, "outputs")
os.makedirs(output_dir, exist_ok=True)

# Read Excel (except assembly which has no sheet)
data = None
if product != "assembly":
    data = read_excel(input_file, product)

# -------------------------
# EXISTING COMPONENTS
# -------------------------

if product == "plate":

    from cad_model.plate import generate_plate
    generate_plate(data["plate"], output_dir)

elif product == "bracket":

    from cad_model.bracket import generate_bracket
    generate_bracket(data["bracket"], output_dir)

elif product == "flange":

    from cad_model.flange import generate_flange
    generate_flange(data["flange"], output_dir)

elif product == "motor_mount":

    from cad_model.motor_mount import generate_motor_mount
    generate_motor_mount(data["motor_mount"], output_dir)

elif product == "gear_plate":

    from cad_model.gear_plate import generate_gear_plate
    generate_gear_plate(data["gear_plate"], output_dir)

elif product == "assembly":

    from cad_model.assembly import generate_assembly
    generate_assembly(output_dir)

# -------------------------
# NEW SHEET METAL PARTS
# -------------------------

elif product == "enclosure":

    from cad_model.enclosure import generate_enclosure
    generate_enclosure(data["enclosure"], output_dir)

elif product == "control_box":

    from cad_model.control_box import generate_control_box
    generate_control_box(data["control_box"], output_dir)

elif product == "machine_frame":

    from cad_model.machine_frame import generate_machine_frame
    generate_machine_frame(data["machine_frame"], output_dir)

elif product == "u_channel":

    from cad_model.u_channel import generate_u_channel
    generate_u_channel(data["u_channel"], output_dir)

elif product == "cabinet":

    from cad_model.cabinet import generate_cabinet
    generate_cabinet(data["cabinet"], output_dir)

else:

    print("Invalid product name:", product)

print("CAD generation finished")