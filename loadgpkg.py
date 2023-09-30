import os
from PyQt5.QtWidgets import QFileDialog
from qgis.core import QgsProject, QgsVectorLayer
import qgis.utils

layers_in_order = [
    "ops_landings",
    "stream_road_xing",
    "stream_trail_xing",
    "ops_skids_existing",
    "ops_skids_proposed",
    "ops_roads_perm",
    "ops_roads_proposed",
    "ops_roads_seasonal",
    "ops_roads_nonapp",
    "base_country_road",
    "base_haul_route",
    "ops_roads_abandoned",
    "ops_eez",
    "bound_no_ops",
    "stream_class1",
    "stream_class2",
    "stream_class3",
    "stream_spring",
    "bound_harvest_area",
    "bound_best_prop_outline",
    "bound_assesors_outline",
    "bound_survey_monuments",
    "base_powerlines",
    "base_structures",
]

# Reverse the list for loading in the correct order
layers_in_order.reverse()

# Use QFileDialog to get the GeoPackage path
gpkg_path, _ = QFileDialog.getOpenFileName(
    None, "Select GeoPackage", "", "GeoPackages (*.gpkg);;All Files (*)"
)
if not gpkg_path:
    raise Exception("No GeoPackage selected!")


def load_layers_from_geopackage(gpkg_path, layers_in_order):
    project = QgsProject.instance()

    for layer_name in layers_in_order:
        uri = f"{gpkg_path}|layername={layer_name}"
        layer = QgsVectorLayer(uri, layer_name, "ogr")

        if not layer.isValid():
            qgis.utils.iface.messageBar().pushMessage(
                f"Layer {layer_name} failed to load!", level=qgis.utils.Qgis.Warning
            )
            continue

        project.addMapLayer(layer, True)
        style_name = layer_name
        success = layer.loadNamedStyle(f"{gpkg_path}|layername={style_name}")
        if not success[1]:
            qgis.utils.iface.messageBar().pushMessage(
                f"Failed to load style for {layer_name}", level=qgis.utils.Qgis.Warning
            )

    qgis.utils.iface.mapCanvas().refreshAllLayers()


# Call the function to load layers
load_layers_from_geopackage(gpkg_path, layers_in_order)
