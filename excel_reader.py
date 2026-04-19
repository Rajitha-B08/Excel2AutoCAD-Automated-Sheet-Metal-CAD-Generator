import pandas as pd


def _find_sheet(sheets, target):
    """Find a sheet name case-insensitively. Returns the actual sheet name
    or raises ValueError if not found."""
    target_lower = target.lower().replace("_", "").replace(" ", "")
    for s in sheets:
        if s.lower().replace("_", "").replace(" ", "") == target_lower:
            return s
    raise ValueError(f"Sheet '{target}' not found. Available: {sheets}")


def read_excel(file, product):

    sheets = pd.ExcelFile(file).sheet_names

    data = {}

    # -------------------------
    # EXISTING PRODUCTS
    # -------------------------

    if product == "plate":

        plate_sheet = _find_sheet(sheets, "Plate")
        holes_sheet = _find_sheet(sheets, "Holes")

        data["plate"] = pd.read_excel(file, sheet_name=plate_sheet)
        data["holes"] = pd.read_excel(file, sheet_name=holes_sheet)


    elif product == "bracket":

        sheet = _find_sheet(sheets, "Bracket")
        data["bracket"] = pd.read_excel(file, sheet_name=sheet)


    elif product == "flange":

        sheet = _find_sheet(sheets, "Flange")
        data["flange"] = pd.read_excel(file, sheet_name=sheet)


    elif product == "motor_mount":

        sheet = _find_sheet(sheets, "MotorMount")
        data["motor_mount"] = pd.read_excel(file, sheet_name=sheet)


    elif product == "gear_plate":

        sheet = _find_sheet(sheets, "GearPlate")
        data["gear_plate"] = pd.read_excel(file, sheet_name=sheet)


    # -------------------------
    # NEW SHEET METAL PRODUCTS
    # -------------------------

    elif product == "u_channel":

        sheet = _find_sheet(sheets, "UChannel")
        data["u_channel"] = pd.read_excel(file, sheet_name=sheet)


    elif product == "machine_frame":

        sheet = _find_sheet(sheets, "MachineFrame")
        data["machine_frame"] = pd.read_excel(file, sheet_name=sheet)


    elif product == "enclosure":

        sheet = _find_sheet(sheets, "Enclosure")
        data["enclosure"] = pd.read_excel(file, sheet_name=sheet)


    elif product == "control_box":

        sheet = _find_sheet(sheets, "ControlBox")
        data["control_box"] = pd.read_excel(file, sheet_name=sheet)


    elif product == "cabinet":

        sheet = _find_sheet(sheets, "Cabinet")
        data["cabinet"] = pd.read_excel(file, sheet_name=sheet)


    return data