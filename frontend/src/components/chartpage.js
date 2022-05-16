import React, { useRef, useState, useEffect } from "react";
import { Select } from 'antd';
import "antd/dist/antd.min.css";
import Barchart from "./barchart";

const Chartpage = () => {
    const [selection1, setSelection1] = useState(null);
    const [barchart1, setBarchart1] = useState(null);
    const [selection2, setSelection2] = useState(null);
    const [barchart2, setBarchart2] = useState(null);

    function handleChange1(value) {
        if (value != "select value for chart1") {
            setBarchart1(true);
            setSelection1(value);
        }
    }
    function handleChange2(value) {
        setBarchart2(true);
        setSelection2(value);
    }

    return (
        <div style={{height: '100%', width: '100%'}}>
            <div><Select defaultValue="select a chart1" style={{ width: 200 }} onChange={handleChange1}>
                <Option value="mortgage">mortgage monthly</Option>
                <Option value="rent">rent weekly</Option>
                <Option value="familyinc">family income weekly</Option>
                <Option value="personalinc">personal income weekly</Option>
                <Option value="householdinc">household income weekly</Option>
                <Option value="crypto">positive crypto tweet percentage</Option>
                <Option value="covid">positive covid tweet percentage</Option>
                <Option value="election">positive election tweet percentage</Option>
                <Option value="housing">positive housing tweet percentage</Option>
            </Select>
            <Select defaultValue="select a chart2" style={{ width: 200 }} onChange={handleChange2}>
                <Option value="mortgage">mortgage monthly</Option>
                <Option value="rent">rent weekly</Option>
                <Option value="familyinc">family income weekly</Option>
                <Option value="personalinc">personal income weekly</Option>
                <Option value="householdinc">household income weekly</Option>
                <Option value="crypto">positive crypto tweet percentage</Option>
                <Option value="covid">positive covid tweet percentage</Option>
                <Option value="election">positive election tweet percentage</Option>
                <Option value="housing">positive housing tweet percentage</Option>
            </Select></div>
            {barchart1 ? <Barchart selection={selection1}/> : <></>}
            {barchart2 ? <Barchart selection={selection2}/> : <></>}
        </div>
    )
};

export default Chartpage;