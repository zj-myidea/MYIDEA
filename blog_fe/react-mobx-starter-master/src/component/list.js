import React from 'react';
import { Link } from "react-router-dom";
import PostService from '../service/post'
import { observer } from 'mobx-react'
import { List } from 'antd'
import { inject, parse_qs } from '../utils'

import 'antd/lib/message/style'
import 'antd/lib/list/style'

const service = new PostService()


@inject({ service })
@observer
export default class L extends React.Component {
    constructor(props) {
        super(props)

        const { location: { search } } = props
        props.service.getall(search)
        //windows.location.herf = /list + search

    }
    handle(pageNo, size) {
        var search = '?page=' + pageNo + '&size=' + size
        this.props.service.getall(search)
    }
    getUrl(current) {
        const { location: { search } } = this.props
        var { size = 20 } = parse_qs(search)

        return '/list?page=' + current + '&size=' + size
    }
    itemRender(current, type, originalElement) {
        
        if (current == 0 || current == this.props.service.pagination.pages + 1) return originalElement
        if (type === 'page') {
            return <Link to={this.getUrl(current)}>{current}</Link>;
        }
        if (type === 'next') {
            return <Link to={this.getUrl(current)} className="ant-pagination-item-link"><i aria-label="图标: right" className="anticon anticon-right"><svg viewBox="64 64 896 896" className="" data-icon="right" width="1em" height="1em" fill="currentColor" aria-hidden="true"><path d="M765.7 486.8L314.9 134.7A7.97 7.97 0 0 0 302 141v77.3c0 4.9 2.3 9.6 6.1 12.6l360 281.1-360 281.1c-3.9 3-6.1 7.7-6.1 12.6V883c0 6.7 7.7 10.4 12.9 6.3l450.8-352.1a31.96 31.96 0 0 0 0-50.4z"></path></svg></i>
            </Link>;
        }
        if (type === 'prev') {
            return <Link to={this.getUrl(current)} className="ant-pagination-item-link"><i aria-label="图标: left" className="anticon anticon-left"><svg viewBox="64 64 896 896" className="" data-icon="left" width="1em" height="1em" fill="currentColor" aria-hidden="true"><path d="M724 218.3V141c0-6.7-7.7-10.4-12.9-6.3L260.3 486.8a31.86 31.86 0 0 0 0 50.3l450.8 352.1c5.3 4.1 12.9.4 12.9-6.3v-77.3c0-4.9-2.3-9.6-6.1-12.6l-360-281 360-281.1c3.8-3 6.1-7.7 6.1-12.6z"></path></svg></i></Link>;
        }
        //
        return originalElement;
    }





    render() {
        const data = this.props.service.posts
        const pagi = this.props.service.pagination
        if (data !== []) {
            return (

                <List bordered
                    itemLayout="horizontal"
                    dataSource={data}
                    renderItem={item => (
                        <List.Item>
                            <List.Item.Meta
                                title={<Link to={"/post/" + item.post_id}>{item.title}</Link>}
                            />
                        </List.Item>
                    )}
                    pagination={{
                        onChange: this.handle.bind(this),
                        pageSize: pagi.size,
                        total: pagi.count,
                        current: pagi.page,
                        itemRender: this.itemRender.bind(this)
                    }}
                />
            )
        }
        else {
            return (<List bordered
                itemLayout="horizontal"
                dataSource={data}
                renderItem={item => (
                    <List.Item>
                        <List.Item.Meta
                            title={<Link to={"/post/" + item.post_id}>{item.title}</Link>}
                        />
                    </List.Item>
                )}
                
            />)
        }
    }



}