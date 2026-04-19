import subprocess
import os

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))

def run_freecad(product):

    cmd = [
        r"C:\Program Files\FreeCAD 1.0\bin\freecadcmd.exe",
        os.path.join(PROJECT_DIR,"cad_runner.py"),
        "--",
        product
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)

    print("FreeCAD Output:")
    print(result.stdout)

    print("FreeCAD Errors:")
    print(result.stderr)


def run_pipeline(product,file):

    run_freecad(product)

    output_dir = os.path.join(PROJECT_DIR,"outputs")

    file_map = {
        "plate":"plate_3d.FCStd",
        "bracket":"bracket_3d.FCStd",
        "flange":"flange_3d.FCStd",
        "motor_mount":"motor_mount_3d.FCStd",
        "gear_plate":"gear_plate_3d.FCStd",
        "assembly":"automation_assembly.FCStd",
        "u_channel":"u_channel_3d.FCStd",
        "cabinet":"cabinet_3d.FCStd",
        "control_box":"control_box_3d.FCStd",
        "enclosure":"enclosure_3d.FCStd",
        "machine_frame":"machine_frame_3d.FCStd"
    }

    cad_file = os.path.join(output_dir,file_map[product])

    if os.path.exists(cad_file):

        return {
            "status":"success",
            "cad_file":cad_file
        }

    else:

        return {
            "status":"error",
            "cad_file":None
        }