import React from 'react';
import ReactDOM from 'react-dom';
import { Chart1 } from './components/chart1';
import Map from './components/map/map';
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import Newpage from './components/newpage';
import {App} from './app'

ReactDOM.render(
<BrowserRouter>
<Routes>
    <Route path='/' element={<App />}>
        <Route path='mappage' element={<Map />}></Route>
        <Route path='graphpage' element={<Chart1 />}></Route>
        <Route path='newpage' element={<Newpage />}></Route>
    </Route>
</Routes>
</BrowserRouter>, 
document.getElementById("reactdiv"));