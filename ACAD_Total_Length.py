import math
from pyautocad import Autocad

# Connect to AutoCAD
acad = Autocad(create_if_not_exists=False, visible=True)
print(f"Connected to DWG: {acad.doc.Name}")

# Initialize total length
total_length = 0

# Get user choice for object selection
choice = acad.doc.Utility.GetString(0, "\nEnter choice (SELECTION/ALL): ").strip().upper()

# Get the objects based on user choice
if choice == "ALL":
    objects = acad.iter_objects()
elif choice == "SELECTION":
    objects = acad.get_selection("Select objects")
else:
    objects = []

# Iterate through the selected objects
for obj in objects:
    obj_type = obj.ObjectName

    if obj_type == "AcDbCircle": # Circle
        circumference = 2 * math.pi * obj.Radius
        total_length += circumference

    elif obj_type == "AcDbEllipse": # Ellipse
        # Ellipse perimeter approximation (Ramanujan’s formula)
        a = obj.MajorAxisLength / 2
        b = obj.MinorAxisLength / 2
        h = ((a - b) ** 2) / ((a + b) ** 2)
        perimeter = math.pi * (a + b) * (1 + (3*h) / (10 + math.sqrt(4 - 3*h)))
        total_length += perimeter

    elif obj_type == "AcDbArc": # Arc
        total_length += obj.ArcLength

    elif obj_type in ("AcDbLine", "AcDbPolyline", "AcDb2dPolyline", "AcDbSpline"): 
        # Line, Polyline, 2D Polyline, Spline
        try:
            total_length += obj.Length
        except:
            pass  # skip if property not found

# Final output
if objects:
    acad.prompt(f"\nTotal length: {total_length}\n")
else:
    acad.prompt("\nNo valid selection made.\n")