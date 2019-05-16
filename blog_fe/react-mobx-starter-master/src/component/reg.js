import React from 'react';
import { Link, Redirect } from "react-router-dom";
import '../css/login.css'
import UserService from '../service/user'
import {observer} from 'mobx-react'
import { message } from 'antd'
import {inject} from '../utils'

import 'antd/lib/message/style'

const service = new UserService()
    

@inject({service})
@observer
export default class Reg extends React.Component {
    handelClick(event) {
        event.preventDefault();
        console.log(event.target.form[0])
        this.props.service.reg(event.target.form[0].value, event.target.form[1].value,event.target.form[2].value)
    }
    render() {
        if (this.props.service.regged){
            console.log('observer login')
            setTimeout(()=>this.props.service.regged=false,5000)
            return <Redirect to='/'/>
          }
        if (this.props.service.errMsg){
            message.error(this.props.service.errMsg,3,setTimeout(()=>this.props.service.errMsg='',5000))
          }
          
        return (
            <div className="login-page">
                <div className="form">
                    <form className="register-form">
                        <input type="text" placeholder="姓名" />
                        <input type="text" placeholder="邮箱" />
                        <input type="password" placeholder="密码" />
                        <input type="password" placeholder="重复密码" />
                        <button onClick={this.handelClick.bind(this)}>注册</button>
                        <p className="message">已经注册? <Link to="login">登录</Link></p>
                    </form>
                </div>
            </div>
        )

    };

}