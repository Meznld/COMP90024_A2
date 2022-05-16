import React, { useState, useEffect, useRef } from 'react';
import { TileLayer, useMap, MapContainer, LayersControl, Marker, Popup, GeoJSON } from 'react-leaflet';
import './map.css';
import L from "leaflet";
import './legend.css';
import Markers from './markers';

const MapMortgage = () => {
    const [geodata, setGeodata] = useState({});
    const [fetched, setFetched] = useState(false);
    const geoJsonRef = useRef();

    useEffect(() => {
        async function fetchData() {
            const result = await fetch("http://localhost:5000/aurin/geodata").then((response) => response.json())
            setGeodata(result);
            console.log(result);
            console.log("geopandas fetch done");
            setFetched(true);
        }
        fetchData();
    }, []);

    function getColor(d) {
        return d > 2200 ? '#800026' :
               d > 2100  ? '#BD0026' :
               d > 2000  ? '#E31A1C' :
               d > 1900  ? '#FC4E2A' :
               d > 1800   ? '#FD8D3C' :
               d > 1700   ? '#FEB24C' :
               d > 1600   ? '#FED976' :
                          '#FFEDA0';
    }
    const style = (feature) => {
        return ({
            fillColor: getColor(feature.properties["median_mortgage_repay_monthly"]),
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
                "Suburb: " + layer.feature.properties["feature_n2"] + "<br .>" + 
                "Meadian Monthly Mortgage Repayment: $" + layer.feature.properties["median_mortgage_repay_monthly"], 
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
        L.control({ position: "bottomleft" })
        useEffect(() => {
            const legend = L.control({ position: "bottomleft" });
            legend.onAdd =  function (map) {
    
            var div = L.DomUtil.create('div', 'info legend'),
                grades = [0, 1600, 1700, 1800, 1900, 2000, 2100, 2200],
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
        //Will execute on unmount, or map change
        return () => {
            map.removeControl(legend)
            }
        }, [map]);
    }

    return(
        <>
        {fetched ? 
        <>
        <GeoJSON data={geodata} onEachFeature={onEachFeature} style={style} ref={geoJsonRef}/>
        <Legend />
        <LayersControl position="topright">
            <LayersControl.Overlay name="top suburbs with positive crypto tweets percentage">
                <Markers selection={"crypto"}/>
            </LayersControl.Overlay>
            <LayersControl.Overlay name="top suburbs with positive covid tweets percentage">
                <Markers selection={"covid"}/>
            </LayersControl.Overlay>
            <LayersControl.Overlay name="top suburbs with positive election tweets percentage">
                <Markers selection={"election"}/>
            </LayersControl.Overlay>
            <LayersControl.Overlay name="top suburbs with positive housing tweets percentage">
                <Markers selection={"housing"}/>
            </LayersControl.Overlay>
        </LayersControl>
        </> 
        : <></>}
        </>
    )
}
export default MapMortgage;