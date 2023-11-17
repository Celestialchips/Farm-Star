import os
from arcgis.gis import GIS
from arcgis.features import FeatureLayerCollection
import datetime

#TODO some functionality here to update map dynamically to represent on website
'''

0 1 * * * /usr/bin/python3 /updater.py

'''

def update_feature_layer(api_key, feature_layer_item_id, new_data_path):
    gis = GIS(api_key=api_key)
    feature_layer_item = gis.content.get(feature_layer_item_id)
    feature_layer_collection = FeatureLayerCollection.fromitem(feature_layer_item)
    feature_layer_collection.manager.overwrite(new_data_path)

if __name__ == "__main__":
    api_key = os.getenv('ESRI_API_KEY')
    feature_layer_item_id = ''
    date_str = datetime.datetime.now().strftime('%Y%m%d')
    new_data_path = f'../../artemis/{date_str}_data.geojson'
    
    update_feature_layer(api_key, feature_layer_item_id, new_data_path)
