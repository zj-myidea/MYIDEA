import axios from 'axios'
import store from 'store'
import {observable} from 'mobx'


store.addPlugin(require('store/plugins/expire'))


export default class UserService {
    @observable  loggedin = false
    @observable  regged = false
    @observable  errMsg = ''

    login(email, password) {
        axios.post("api/user/login",{
            email:email,
            password:password
        }).then(
            (response) =>{
                
                store.set('token', response.data.token, (new Date()).getTime() + (8*3600*1000))
                this.loggedin =true
            }
        ).catch(
        (errot) =>{
            this.errMsg='登录失败'
        }
        )
        
    }
    
    reg(name,email, password) {
        
        
        axios.post("api/user/reg",{
            name:name,
            email:email,
            password:password
        }).then(
            (response) =>{
              
                store.set('token', response.data.token, (new Date()).getTime() + (8*3600*1000))
                this.regged =true
                
            }
        ).catch(
            (errot) =>{
                this.errMsg='注册失败'
            }
            )
        
    }
}









