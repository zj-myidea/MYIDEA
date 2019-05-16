import axios from 'axios'
import store from 'store'
import {observable} from 'mobx'
import { Pagination } from 'antd';


store.addPlugin(require('store/plugins/expire'))


export default class PostService {
    constructor(){
        this.axios = axios.create(
            {
                baseURL:'/api/post/'
            }
        )
    }
    @observable msg = ''
    @observable post = {}
    @observable posts = []
    @observable pagination = {page:1,size:20,count:0,pages:1}
    pub(title, content) {
        
        this.axios.post("pub",{
                title,content
        },{headers:{'JWT':store.get('token')}}).then(
            (response) =>{
                
                this.msg ='提交成功'
            }
        ).catch(
        (errot) =>{
            this.errMsg='提交失败'
        }
        )
        
    }
    getall(search) {
        this.axios.get(search).then(
        (response) =>{
            
            this.posts = response.data.posts
            this.pagination = response.data.pagination
        }
    ).catch(
        (errot) =>{
            this.errMsg='提交失败'
        }
        )
    }

    getpost(id) {
        this.axios.get(id).then(
        (response) =>{      
            this.post = response.data.post
        }
    ).catch(
        (errot) =>{
            this.errMsg='文章获取失败'
        }
        )
    }
    
}









