from osgeo import gdal
import numpy as np
import laspy

# Define the input LAS file and output TIFF file
input_las_file = "input_las.las"
input_tif_file = "input_tif.tif"
output_tif_file = "output_tif.tif"

# Open the TIFF dataset
tif_dataset = gdal.Open(input_tif_file, gdal.GA_Update)

# Get the dimensions of the TIFF dataset
tif_width = tif_dataset.RasterXSize
tif_height = tif_dataset.RasterYSize

# Get the geotransform information from the input TIFF file
geotransform = tif_dataset.GetGeoTransform()

# Create a new band for the output TIFF
num_bands = tif_dataset.RasterCount
print(f"num_bands: {num_bands}")
# num_bands = tif_dataset.RasterCount + 1
output_dataset = gdal.GetDriverByName("GTiff").Create(output_tif_file, tif_width, tif_height, num_bands, gdal.GDT_Float32)

# Set the geotransform and CRS information for the output TIFF
output_dataset.SetGeoTransform(geotransform)
output_dataset.SetProjection(tif_dataset.GetProjection())

# Copy existing bands from input TIFF to output TIFF
for i in range(1, num_bands):
    band_data = tif_dataset.GetRasterBand(i).ReadAsArray()
    output_dataset.GetRasterBand(i).WriteArray(band_data)

# Open the LAS file
las_reader = laspy.read(input_las_file)

# Get the LAS point cloud data
las_points = las_reader.points
print(f"las_points: {las_points}")
print(f"las_points count: {len(las_points)}")

# Create an empty array for the new elevation band
elevation_band = np.zeros((tif_height, tif_width), dtype=np.float32)

# Populate the elevation data from LAS to the new band
for i in range(len(las_points)):
    x = int((las_points["X"][i] - geotransform[0]) / geotransform[1])
    y = int((las_points["Y"][i] - geotransform[3]) / geotransform[5])

    print(f"x: {x}, y: {y}")

    # Check if the indices are within bounds
    if 0 <= x < tif_width and 0 <= y < tif_height:
        elevation_band[y, x] = las_points["Z"][i]

print(f"elevation_band: {elevation_band}")

# Write the elevation data to the new band
output_dataset.GetRasterBand(num_bands).WriteArray(elevation_band)

# Close the datasets
tif_dataset = None
output_dataset = None

print("Elevation data from LAS file added to the TIFF file with correct georeferencing.")
