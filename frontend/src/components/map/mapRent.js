import React, { useState, useEffect, useRef } from 'react';
import { TileLayer, useMap, MapContainer, LayersControl, Marker, Popup, GeoJSON } from 'react-leaflet';
import './map.css';
import L from "leaflet";
import './legend.css';

const MapRent = () => {
    const [geodata, setGeodata] = useState({});
    const [fetched, setFetched] = useState(false);
    const geoJsonRef = useRef();

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
            fillColor: getColor(feature.properties["median_rent_weekly"]),
            weight: 2,
            opacity: 1,
            color: 'white',
            dashArray: '2',
            fillOpacity: 0.7
        });
    }
    
    const highlightFeature = (e) => {
        let layer = e.target;
    
        layer.setStyle({
            weight: 5,
            color: '#666',
            dashArray: '',
            fillOpacity: 0.7
        });
    
        if (!L.Browser.ie && !L.Browser.opera && !L.Browser.edge) {
            layer.bringToFront();
        }
        console.log(typeof layer.feature.properties);
        //layer.bindPopup(JSON.stringify(layer.feature.properties)).openPopup();
        if (layer.feature.properties) {
            layer.bindPopup(
                "suburb: " + layer.feature.properties["feature_n2"] + "<br .>" + 
                "median rent weekly: " + layer.feature.properties["median_rent_weekly"], 
                {maxHeight: 200}
            ).openPopup();
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
    function Legend() {
        const map = useMap();
        useEffect(() => {
            const legend = L.control({ position: "bottomleft" });
            legend.onAdd =  function (map) {
    
            var div = L.DomUtil.create('div', 'info legend'),
                grades = [0, 200, 250, 300, 350, 400, 450, 500],
                labels = [];
        
            // loop through our density intervals and generate a label with a colored square for each interval
            for (var i = 0; i < grades.length; i++) {
                div.innerHTML +=
                    '<i style="background:' + getColor(grades[i] + 1) + '"></i> ' +
                    grades[i] + (grades[i + 1] ? '&ndash;' + grades[i + 1] + '<br>' : '+');
            }
        
            return div;
        };
        
        legend.addTo(map);
        }, [map]);
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

        <div id="map" style={{height: '100%'}}>
            <MapContainer center={[-37.813, 144.963]} zoom={9} scrollWheelZoom={false}>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                />
                {fetched ? <><GeoJSON data={geodata} onEachFeature={onEachFeature} style={style} ref={geoJsonRef}/><Legend /></> : <></>}
            </MapContainer>
        </div>
        </>
    )
}
export default MapRent;