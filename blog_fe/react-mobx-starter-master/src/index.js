import React from 'react';
import ReactDom from 'react-dom';
import { BrowserRouter as Router, Route, Link } from "react-router-dom";
import Login from './component/login'
import Reg from './component/reg'
import Pub from './component/pub'
import L from './component/list'
import Post from './component/post'
import Line from './component/myline'
import { Layout, Menu, Icon,LocaleProvider } from 'antd';


import 'antd/lib/layout/style'
import 'antd/lib/menu/style'
import 'antd/lib/icon/style'
import zh_CN from 'antd/lib/locale-provider/zh_CN';

const { Header, Content, Footer } = Layout;
const Home = () => (
  <div>
    hello
  </div>
);

const About = () => (
  <div>
    <h1>博客项目</h1>
    <ul>
      <li>采用前后端分离开发模式</li>
      <li>前端使用最新的React技术，后端使用Django框架</li>
      <li>使用Restful风格设计服务间API接口</li>
      <li>无session认证技术</li>
      <li>阿里开源Antd组件</li>
    </ul>

  </div>
);



class Root extends React.Component {
  render() {
    return (
      <Router>
        <Layout>
          <Header>
            <Menu mode="horizontal" theme='dark' >
              <Menu.Item key="home">
                <Link to='/'><Icon type="home" />主页</Link>
              </Menu.Item>
              <Menu.Item key="login">
                <Link to='/login'><Icon type="login" />登录</Link>
              </Menu.Item>
              <Menu.Item key="reg">
                <Link to='/reg'><Icon type="reg" />注册</Link>
              </Menu.Item>
              <Menu.Item key="pub">
                <Link to='/pub'><Icon type="pub" />发布文章</Link>
              </Menu.Item>
              <Menu.Item key="list">
                <Link to='/list'><Icon type="list" />文章列表</Link>
              </Menu.Item>
              <Menu.Item key="about">
                <Link to='/about'><Icon type="about" />关于</Link>
              </Menu.Item>
            </Menu>
          </Header>
          <Content style={{ padding: '8px 50px' }}>
            <div style={{ background: '#fff', padding: 24, minHeight: 280 }}>
              <Route exact path="/" component={Home} />
              <Route path="/about" component={About} />
              <Route path="/login" component={Login} />
              <Route path="/pub" component={Pub} />
              <Route path="/list" component={L} />
              <Route path="/reg" component={Reg} />
              <Route path="/post/:id" component={Post} />
              <Route path="/show/:id" component={Line} />
            </div>
          </Content>
          <Footer style={{ textAlign: 'center' }}>
            zhoujing ©2018 Created
           </Footer>

        </Layout>
      </Router>

    )

  };

}

ReactDom.render(<LocaleProvider locale={zh_CN}><Root /></LocaleProvider>, document.getElementById('root'))

