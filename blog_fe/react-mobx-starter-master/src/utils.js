import React from 'react'

const inject = obj => Comp => props => <Comp {...obj} {...props}/>

function parse_qs(search){
    var re = /(\w+)=([^&]+)/
    var ret = {}
    if (search[0]=='?'){
        search = search.substr(1)
    
    search.split('&').forEach(element => {

        var math = re.exec(element)
        if (math){
            ret[math[1]]=math[2]
        }
        
    });
    return ret
    }
}

export {inject,parse_qs}