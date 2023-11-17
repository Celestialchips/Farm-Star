require([
    "esri/Map",
    "esri/views/MapView",
    "esri/layers/FeatureLayer"
  ], function(Map, MapView, FeatureLayer) {
    var map = new Map({
      basemap: "topo-vector"
    });
  
    var view = new MapView({
      container: "viewDiv",
      map: map,
      center: [-118.71511,34.09042], 
      zoom: 11
    });
  
    // Add multiple layers to the map
    var layer1 = new FeatureLayer({
      url: "https://services6.arcgis.com/3tKBZy9r0mwAeNvJ/arcgis/rest/services/original_points_lv/FeatureServer"
    });
  
    var layer2 = new FeatureLayer({
      url: "https://services6.arcgis.com/3tKBZy9r0mwAeNvJ/arcgis/rest/services/filtered_points_expanded_lv/FeatureServer"
    });

    var layer3 = new FeatureLayer({
        url: "https://services6.arcgis.com/3tKBZy9r0mwAeNvJ/arcgis/rest/services/filtered_points_concave_lv/FeatureServer"
      });
    
    var layer4 = new FeatureLayer({
    url: "https://services6.arcgis.com/3tKBZy9r0mwAeNvJ/arcgis/rest/services/expanded_hull_lv/FeatureServer"
    });

    var layer5 = new FeatureLayer({
        url: "https://services6.arcgis.com/3tKBZy9r0mwAeNvJ/arcgis/rest/services/concave_hull_lv/FeatureServer"
      });
    
    var layer6 = new FeatureLayer({
    url: "https://services6.arcgis.com/3tKBZy9r0mwAeNvJ/arcgis/rest/services/all_attom_points_lv/FeatureServer"
    });
  
    map.add(layer1);
    map.add(layer2);
    map.add(layer3);
    map.add(layer4);
    map.add(layer5);
    map.add(layer6);
  });
  