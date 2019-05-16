import React from 'react';
import { Link, Redirect } from "react-router-dom";
import PostService from '../service/post'
import { observer } from 'mobx-react'
import { Comment, message, Tooltip,Icon } from 'antd'
import { inject } from '../utils'
import 'antd/lib/message/style'
import 'antd/lib/icon/style'
import 'antd/lib/comment/style'
import 'antd/lib/tooltip/style'

import moment from 'moment'

const service = new PostService()


@inject({ service })
@observer
export default class Post extends React.Component {

    constructor(props) {
        super(props)

        const { match: { params } } = props

        props.service.getpost(params.id)
        //windows.location.herf = /list + search

    }
    state = {
        likes: 0,
        dislikes: 0,
        action: null,
    }

    like = () => {
        this.setState({
            likes: 1,
            dislikes: 0,
            action: 'liked',
        });
    }

    dislike = () => {
        this.setState({
            likes: 0,
            dislikes: 1,
            action: 'disliked',
        });
    }
    render() {
        const { likes, dislikes, action } = this.state;

        const actions = [
            <span>
                <Tooltip title="Like">
                    <Icon
                        type="like"
                        theme={action === 'liked' ? 'filled' : 'outlined'}
                        onClick={this.like}
                    />
                </Tooltip>
                <span style={{ paddingLeft: 8, cursor: 'auto' }}>
                    {likes}
                </span>
            </span>,
            <span>
                <Tooltip title="Dislike">
                    <Icon
                        type="dislike"
                        theme={action === 'disliked' ? 'filled' : 'outlined'}
                        onClick={this.dislike}
                    />
                </Tooltip>
                <span style={{ paddingLeft: 8, cursor: 'auto' }}>
                    {dislikes}
                </span>
            </span>
           
        ];
        if (this.props.service.errMsg) {
            message.info(this.props.service.errMsg, 3, setTimeout(() => this.props.service.errMsg = '', 5000))
        }
        
        let { title,auther, content, postdate } = this.props.service.post
        
            
        console.log()
        return (
            <Comment
                actions={actions}
                author={(<p>{'作者：'+JSON.stringify(auther)}</p>)}
                content={(
                    <p>{content}</p>
                )}
                datetime={(
                    <Tooltip >
                        <p><span>{'发布时间'+moment(postdate).format('YYYY-MM-DD HH:mm:ss')}</span></p>
                    </Tooltip>
                )}
            />
        )

    };

}