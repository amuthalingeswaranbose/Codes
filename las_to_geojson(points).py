import laspy
import json
import pdb

# Input LAS file
las_file_path = "input_file_name.las"

# Output GeoJSON file
geojson_file_path = "output.geojson"

# Read the LAS file
in_file = laspy.read(las_file_path)

print(f"Number of points in LAS file: {len(in_file)}")

# Create a GeoJSON-like feature collection
feature_collection = {
    "type": "FeatureCollection",
    "features": []
}

# Iterate through LAS points and create features
for i, (x, y, z) in enumerate(zip(in_file.x, in_file.y, in_file.z)):
    print(f"count: {i} -> x: {x}, y {y}")
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [x, y]
        },
        "properties": {
            "Z": z
        }
    }
    feature_collection["features"].append(feature)

# Save the feature collection as GeoJSON
with open(geojson_file_path, "w") as geojson_file:
    json.dump(feature_collection, geojson_file)

print(f"GeoJSON file saved to {geojson_file_path}")
