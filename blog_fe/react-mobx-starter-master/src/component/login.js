import React from 'react';
import { Link, Redirect } from "react-router-dom";
import '../css/login.css'
import UserService from '../service/user'
import { observer } from 'mobx-react'
import { message } from 'antd'
import 'antd/lib/message/style'
import { inject } from '../utils'




const service = new UserService()


@inject({ service })
@observer
export default class Login extends React.Component {

  // state = {"reg":-1}

  handelClick(event) {

    event.preventDefault();
    this.props.service.login(event.target.form[0].value, event.target.form[1].value, this)


  }
  render() {
    // if (this.state.reg != -1){

    //   return <Redirect to='/about'/>

    // }
    if (this.props.service.loggedin) {

      setTimeout(() => this.props.service.loggedin = false, 5000)
      return <Redirect to='/about' />
    }
    // if (this.props.service.errMsg){
    //   message.error(this.props.service.errMsg,3,setTimeout(()=>this.props.service.errMsg='',5000))
    // }


    return (
      <div className="login-page">
        <div className="form">
          <form className="login-form">
            <input type="text" placeholder="eamil" value="tom@qq.com" />
            <input type="password" placeholder="密码" />
            <button onClick={this.handelClick.bind(this)}>登录</button>
            <p className="message">还未注册？ <Link to="reg">马上注册</Link></p>
          </form>
        </div>
      </div>
    )

  };

}












