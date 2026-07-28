# Import necessary libraries
from qgis.core import (QgsRasterLayer, QgsProject, QgsVectorLayer, 
                       QgsFeature, QgsGeometry, QgsPoint, QgsPointXY, QgsProcessingFeatureSourceDefinition, QgsField)
from PyQt5.QtWidgets import QFileDialog, QInputDialog
import processing
from PyQt5.QtCore import QVariant

# Prompt user to select a .nc file
file_dialog = QFileDialog()
netcdf_file_path, _ = file_dialog.getOpenFileName(None, 
                        "Select NetCDF File", "", 
                        "NetCDF Files (*.nc)")

# Initialize the raster layer variable
raster_layer = None

# Load the NetCDF file as a raster layer if a file was selected and a variable name is provided
if netcdf_file_path:
    variable_name, ok = QInputDialog.getText(None, 
                                             "Enter Variable Name", 
                                             "Enter the name of the variable to load:")
    if ok and variable_name:
        # Attempt to load the raster layer
        raster_layer = QgsRasterLayer(f'NETCDF:"{netcdf_file_path}":{variable_name}', variable_name)
        
        # Check if the layer is valid and add it to the project
        if raster_layer.isValid():
            QgsProject.instance().addMapLayer(raster_layer)
            print(f"Successfully added the raster layer: {variable_name}")
        else:
            print("Failed to load the specified variable as a raster layer.")
    else:
        print("No variable name entered.")
else:
    print("No file selected!")

# Polygonize the raster layer if it was loaded successfully
if raster_layer and raster_layer.isValid():
    
    # Run the 'rasterpolygonize' processing tool
    params = {
        'INPUT': raster_layer,
        'BAND': 1,  # Assuming the first band, adjust if necessary
        'FIELD': 'DN',  # Field name for raster values in the vector output
        'OUTPUT': 'TEMPORARY_OUTPUT' 
    }
    result = processing.run("gdal:polygonize", params)

    # Load and add the resulting polygonized layer
    vector_layer = QgsVectorLayer(result['OUTPUT'], f"{variable_name}_polygonized", "ogr")
    if vector_layer.isValid():
        QgsProject.instance().addMapLayer(vector_layer)
        print(f"Successfully added the polygonized vector layer: {variable_name}_polygonized")
        
    else:
        print("Failed to load the polygonized vector layer.")
        
plg = vector_layer

# save the new polygon         
shp_file_path, _ = QFileDialog.getSaveFileName(None, "Save the shapefile", "", "Shapefiles (*.shp)")
QgsVectorFileWriter.writeAsVectorFormat(plg, shp_file_path, 'utf-8', driverName = 'ESRI Shapefile')
