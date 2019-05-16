import React from 'react';
import { Link, Redirect } from "react-router-dom";
import PostService from '../service/post'
import { observer } from 'mobx-react'
import { Form, message, Input, Button } from 'antd'
import { inject } from '../utils'
import FormItem from 'antd/lib/form/FormItem'
import 'antd/lib/message/style'
import 'antd/lib/form/style'
import 'antd/lib/input/style'
import 'antd/lib/button/style'

const service = new PostService()
const { TextArea } = Input;

@inject({ service })
@observer
export default class pub extends React.Component {
    handelClick(event) {
        event.preventDefault();
        console.log(event.target)
        this.props.service.pub(event.target[0].value, event.target[1].value)
        console.log(event.target[0].value, event.target[1].value)
    }
    render() {

        if (this.props.service.msg) {
            message.info(this.props.service.msg, 3, setTimeout(() => this.props.service.msg = '', 5000))
        }

        return (
            <Form layout="vertical" onSubmit={this.handelClick.bind(this)}>
                <FormItem label="标题:" labelCol={{span:1}} wrapperCol={{span:14}} 
                    >
                    <Input  />
                </FormItem>
                <FormItem 
                    label="文章内容:"  wrapperCol={{span:23}} labelCol={{span:1}} >
                    <TextArea rows={24} />
                </FormItem>
                <FormItem 
                    wrapperCol={{ span: 12, offset: 11 }} >
                    <Button type="primary" htmlType="submit">提交</Button>
                </FormItem>
                >
            </Form>
        )

    };

}