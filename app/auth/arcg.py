import os
import getpass
from datetime import datetime
from arcgis.gis import GIS

#TODO upload to ArcGIS programmatically to update map

'''
use cronjob to schedule tasks
'''

class GisUploader:
    @staticmethod
    def upload_geojson_to_arcgis(api_key, directory_path, prefix=''):
        gis = GIS(api_key=api_key)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        geojson_files = [f for f in os.listdir(directory_path) if f.endswith('.geojson')]

        for geojson_file in geojson_files:
            unique_filename = f"{prefix}{timestamp}_{geojson_file}"
            file_path = os.path.join(directory_path, geojson_file)

            item_properties = {
                'title': os.path.splitext(unique_filename)[0],
                'description': f'Uploaded via ARTEMIS {prefix}',
                'tags': f'GeoJSON, API, Upload, {prefix}',
                'type': 'GeoJson'
            }

            try:
                if not os.path.isfile(file_path):
                    print(f"File {file_path} does not exist.")
                    continue

                item = gis.content.add(item_properties, data=file_path)
                if not item:
                    print(f"Failed to create item for {unique_filename}. Item is None.")
                    print(f"Item properties: {item_properties}")
                    continue

                print(f"Item created: {item.title}, ID: {item.id}")

                feature_layer_item = item.publish()
                if not feature_layer_item:
                    print(f"Failed to publish feature layer for {unique_filename}.")
                    print(f"Item ID: {item.id}")
                    continue

                print(f"Feature Layer Item ID: {feature_layer_item.id} for {unique_filename}")
            except Exception as e:
                print(f"Failed to upload and publish {unique_filename}: {e}")
