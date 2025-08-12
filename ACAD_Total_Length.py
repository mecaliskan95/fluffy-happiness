# https://pypi.org/project/pyautocad/
# https://pyautocad.readthedocs.io/en/latest/

from pyautocad import Autocad
import math

acad = Autocad(create_if_not_exists=False, visible=True)
print(f"Connected to DWG: {acad.doc.Name}")

total_length = 0

acad.prompt("\nSelect objects to measure length...\n")

acad.prompt("\nType SELECTION or ALL: ")
choice = acad.doc.Utility.GetString(0, "\nEnter choice (SELECTION/ALL): ")
choice = choice.strip().upper()

if choice == "ALL":
    for obj in acad.iter_objects():
        if obj.ObjectName == "AcDbCircle":
            circumference = 2 * math.pi * obj.Radius
            total_length += circumference
        elif obj.ObjectName in ("AcDbLine", "AcDbArc", "AcDbPolyline", "AcDbSpline"):
            total_length += obj.Length
        
elif choice == "SELECTION":
    for obj in acad.get_selection("Select objects"):
        if obj.ObjectName == "AcDbCircle":
            circumference = 2 * math.pi * obj.Radius
            total_length += circumference
        elif obj.ObjectName in ("AcDbLine", "AcDbArc", "AcDbPolyline", "AcDbSpline"):
            total_length += obj.Length

if choice in ["SELECTION", "ALL"]:
    acad.prompt(f"\nTotal length: {total_length:.2f}\n")
else:
    acad.prompt("\nNo valid selection made.\n")