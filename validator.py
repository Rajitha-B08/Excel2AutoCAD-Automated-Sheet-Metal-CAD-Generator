def validate_plate(plate,holes):

    errors=[]

    length = plate["length"][0]
    width = plate["width"][0]
    thickness = plate["thickness"][0]

    if length<=0:
        errors.append("Length must be positive")

    if width<=0:
        errors.append("Width must be positive")

    if thickness<=0:
        errors.append("Thickness must be positive")

    if length>2000:
        errors.append("Length too large")

    if width>2000:
        errors.append("Width too large")

    if thickness>200:
        errors.append("Thickness too large")

    for i,row in holes.iterrows():

        if row["x"]<0 or row["y"]<0:
            errors.append(f"Hole {i} negative position")

        if row["x"]>length or row["y"]>width:
            errors.append(f"Hole {i} outside plate")

        if row["diameter"]<=0:
            errors.append(f"Hole {i} invalid diameter")

    return errors