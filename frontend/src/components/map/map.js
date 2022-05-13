// fetch backend and get a geojson data with concate properties of shapefiles and "sa2_g02_selected_medians_and_averages_census_2016-7286388448228732680.json"
// display map and choropleth map of "median_rent_weekly"
// no legend yet
import React, {useState, useEffect, useRef} from 'react';
import { TileLayer, MapContainer, GeoJSON } from 'react-leaflet';
import './map.css';

const Map = () => {
    const [geodata, setGeodata] = useState({});
    const [fetched, setFetched] = useState(false);

    useEffect(() => {
        async function fetchData() {
            const result = await fetch("http://localhost:5000/aurin").then((response) => response.json())
            setGeodata(result);
            console.log(result);
            console.log("geopandas fetch done");
            setFetched(true);
        }
        fetchData();
    }, []);

    const geoJsonRef = useRef();

    function getColor(d) {
        return d > 500 ? '#800026' :
               d > 450  ? '#BD0026' :
               d > 400  ? '#E31A1C' :
               d > 350  ? '#FC4E2A' :
               d > 300   ? '#FD8D3C' :
               d > 250   ? '#FEB24C' :
               d > 200   ? '#FED976' :
                          '#FFEDA0';
    }
    const style = (feature) => {
        return ({
            fillColor: getColor(feature.properties.median_rent_weekly),
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '2',
            fillOpacity: 0.7
        });
    }

    const highlightFeature = (e) => {
        let layer = e.target;
    
        //layer.setStyle({
        //    weight: 5,
        //    color: '#666',
        //    dashArray: '',
        //    fillOpacity: 0.7
        //});
    
        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
        console.log(typeof layer.feature.properties);
        if (layer.feature.properties) {
            layer.bindPopup(Object.keys(layer.feature.properties).map(function (k) {
              return k + ": " + layer.feature.properties[k];
            }).join("<br />"), {
              maxHeight: 200
            }).openPopup();
        }
    }
    const resetHighlight = (e) => {
        geoJsonRef.current.resetStyle(e.target);
    }
    const onEachFeature = (feature, layer) => {
        layer.on({
            mouseover: highlightFeature,
            mouseout: resetHighlight
        });
    }

    return(
        <>
        <link rel="stylesheet" href="https://unpkg.com/leaflet@1.8.0/dist/leaflet.css"
        integrity="sha512-hoalWLoI8r4UszCkZ5kL8vayOGVae1oxXe/2A4AO6J9+580uKHDO3JdHb7NzwwzK5xr/Fs0W40kiNHxM9vyTtQ=="
        crossorigin=""
        />
        <script src="https://unpkg.com/leaflet@1.8.0/dist/leaflet.js"
            integrity="sha512-BB3hKbKWOc9Ez/TAwyWxNXeoV9c1v6FIeYiBieIWkpLjauysF18NzgR1MBNBXf8/KABdlkX68nAhlwcDFLGPCQ=="
            crossorigin="">
        </script>

        <div id="map1" style={{height: '100%'}}>
            <MapContainer center={[-37.813, 144.963]} zoom={9} scrollWheelZoom={false}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {fetched ? <GeoJSON data={geodata} onEachFeature={onEachFeature} style={style} ref={geoJsonRef}/> : <></>}
            </MapContainer>
        </div>
        </>
    )
}

export default Map;