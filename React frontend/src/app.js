import React from 'react';
import {Layout, Menu} from 'antd';
import "antd/dist/antd.min.css";
import {Outlet, Link} from 'react-router-dom';

const { Header, Content, Footer } = Layout;
export class App extends React.Component {
    render() {
        return(
            <Layout>
                <Header style={{background: "white"}}>
                    <Menu mode="horizontal">
                        <Menu.Item><nav><Link to={"/mappage"}>nav to map page</Link></nav></Menu.Item>
                        <Menu.Item><nav><Link to={"/graphpage"}>nav to graph page</Link></nav></Menu.Item>
                        <Menu.Item><nav><Link to={"/newpage"}>nav to new empty page</Link></nav></Menu.Item>
                    </Menu>
                </Header>
                <Content style={{ padding: '0 50px', height: 680}}>
                    <Outlet />
                </Content>
                <Footer style={{textAlign: 'center'}}>This is footer: COMP90024 assignment2</Footer>
            </Layout>
        );
    }
}