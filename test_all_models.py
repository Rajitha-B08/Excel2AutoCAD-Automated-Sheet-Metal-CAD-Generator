"""
Test script to verify all CAD model generators produce separate 3D and 2D files.
Run with: python test_all_models.py
"""
import subprocess
import os
import sys
import time

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))
FREECAD_CMD = r"C:\Program Files\FreeCAD 1.0\bin\freecadcmd.exe"
CAD_RUNNER = os.path.join(PROJECT_DIR, "cad_runner.py")
OUTPUT_DIR = os.path.join(PROJECT_DIR, "outputs")

# Products and their expected output files (3D + 2D)
PRODUCTS = {
    "enclosure":     ("enclosure_3d.FCStd",     "enclosure_2d.FCStd"),
    "machine_frame": ("machine_frame_3d.FCStd", "machine_frame_2d.FCStd"),
    "u_channel":     ("u_channel_3d.FCStd",     "u_channel_2d.FCStd"),
    "control_box":   ("control_box_3d.FCStd",   "control_box_2d.FCStd"),
    "cabinet":       ("cabinet_3d.FCStd",       "cabinet_2d.FCStd"),
    "flange":        ("flange_3d.FCStd",        "flange_2d.FCStd"),
    "gear_plate":    ("gear_plate_3d.FCStd",    "gear_plate_2d.FCStd"),
    "motor_mount":   ("motor_mount_3d.FCStd",   "motor_mount_2d.FCStd"),
}


def test_product(product, file_3d, file_2d):
    """Run one product generation and check for separate 3D and 2D outputs."""
    path_3d = os.path.join(OUTPUT_DIR, file_3d)
    path_2d = os.path.join(OUTPUT_DIR, file_2d)

    # Clean old outputs
    for p in [path_3d, path_2d]:
        if os.path.exists(p):
            os.remove(p)

    cmd = [FREECAD_CMD, CAD_RUNNER, "--", product]
    print(f"\n{'='*60}")
    print(f"  Testing: {product}")
    print(f"{'='*60}")

    start = time.time()
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    elapsed = time.time() - start

    if result.stderr.strip():
        # Only show non-FreeCAD-boilerplate errors
        errs = [l for l in result.stderr.strip().split('\n')
                if 'FreeCAD' not in l and 'LGPL' not in l and l.strip()]
        if errs:
            print(f"  STDERR: {'; '.join(errs[:3])}")

    success = True
    issues = []

    if result.returncode != 0:
        issues.append(f"Exit code: {result.returncode}")
        success = False

    # Check 3D file
    if os.path.exists(path_3d):
        sz = os.path.getsize(path_3d)
        print(f"  3D Model: {file_3d} ({sz:,} bytes)")
        if sz < 100:
            issues.append("3D file too small")
            success = False
    else:
        issues.append(f"3D file NOT created: {file_3d}")
        success = False

    # Check 2D file
    if os.path.exists(path_2d):
        sz = os.path.getsize(path_2d)
        print(f"  2D Drawing: {file_2d} ({sz:,} bytes)")
        if sz < 100:
            issues.append("2D file too small")
            success = False
    else:
        issues.append(f"2D file NOT created: {file_2d}")
        success = False

    # Check STEP file (optional)
    step_path = os.path.join(OUTPUT_DIR, product + "_3d.step")
    if os.path.exists(step_path):
        print(f"  STEP File: {product}_3d.step ({os.path.getsize(step_path):,} bytes)")

    status = "PASS" if success else "FAIL"
    print(f"  Result: {status} ({elapsed:.1f}s)")
    for issue in issues:
        print(f"    - {issue}")

    return success


def main():
    print("=" * 60)
    print("  CAD Model Test Suite (Separate 3D + 2D Output)")
    print("=" * 60)

    if not os.path.exists(FREECAD_CMD):
        print(f"ERROR: FreeCAD not found at {FREECAD_CMD}")
        sys.exit(1)

    os.makedirs(OUTPUT_DIR, exist_ok=True)

    results = {}
    for product, (f3d, f2d) in PRODUCTS.items():
        try:
            results[product] = test_product(product, f3d, f2d)
        except subprocess.TimeoutExpired:
            print(f"  Result: FAIL (timeout)")
            results[product] = False
        except Exception as e:
            print(f"  Result: FAIL ({e})")
            results[product] = False

    # Summary
    print(f"\n{'='*60}")
    print("  SUMMARY")
    print(f"{'='*60}")
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    for product, ok in results.items():
        print(f"  {product:20s} : {'PASS' if ok else 'FAIL'}")
    print(f"\n  {passed}/{total} passed")
    print(f"{'='*60}")

    sys.exit(0 if passed == total else 1)


if __name__ == "__main__":
    main()
