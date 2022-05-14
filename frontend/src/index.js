import React from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import { Chart1 } from './components/chart1';
import MapMortgage from './components/map/mapMortgage';
import MapRent from './components/map/mapRent';
import MapFamily from './components/map/mapFamily';
import MapPersonal from './components/map/mapPersonal';
import MapHousehold from './components/map/mapHousehold';
import Newpage from './components/newpage';
import {App} from './app'

ReactDOM.render(
<BrowserRouter>
<Routes>
    <Route path='/' element={<App />}>
        <Route path='mortgage' element={<MapMortgage />}></Route>
        <Route path='rent' element={<MapRent />}></Route>
        <Route path='family' element={<MapFamily />}></Route>
        <Route path='personal' element={<MapPersonal />}></Route>
        <Route path='household' element={<MapHousehold />}></Route>
        <Route path='graphpage' element={<Chart1 />}></Route>
        <Route path='newpage' element={<Newpage />}></Route>
    </Route>
</Routes>
</BrowserRouter>, 
document.getElementById("reactdiv"));