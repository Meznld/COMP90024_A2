import React from 'react';
//import L from 'leaflet';
import { TileLayer, useMap, MapContainer, Marker, Popup } from 'react-leaflet';
import './map.css';

export class Map1 extends React.Component {
    //map = L.map("map1", {
    //    center: [51.505, -0.09],
    //    zoom: 13
    //})
    render() {
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
                <MapContainer center={[-37.813, 144.963]} zoom={12} scrollWheelZoom={false}>
                    <TileLayer
                        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />
                    <Marker position={[51.505, -0.09]}>
                        <Popup>
                        A pretty CSS3 popup. <br /> Easily customizable.
                        </Popup>
                    </Marker>
                </MapContainer>
            </div>
            </>
        )
    }
}