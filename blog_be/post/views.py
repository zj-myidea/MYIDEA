from django.shortcuts import render
# Create your views here.
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.http import HttpResponseBadRequest, HttpResponseNotFound
from user.views import authenticate
import datetime
import simplejson
from .models import Post, Content
from user.models import User
import math
@authenticate
def pub(request:HttpRequest):
    post = Post()
    content = Content()
    try:

        payload = simplejson.loads(request.body)
        post.title = payload['title']

        content.content = payload['content']

        post.postdate = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        post.auther = User(id=request.user.id)
        post.save()
        content.post = post
        content.save()

        return JsonResponse({'post_id':post.id})


    except Exception as e:
        print(e)
        return  HttpResponseBadRequest()

def vailable_arg(d:dict, keyword:str, type_func, default, vail_func):
    try:
        ret = d.get(keyword)
        ret = type_func(ret)
        ret = vail_func(ret,default )
    except:
        ret = default
    return ret

def getall(request:HttpRequest): # post?page=1&size=20

    page = vailable_arg(request.GET, 'page', int, 1, lambda x,y:x if x>0 else y)
    size = vailable_arg(request.GET, 'size', int, 20, lambda x,y:x if x>0 and x<101 else y)

    try:
        start = (page - 1) * size
        posts = Post.objects.order_by('-id')
        count = posts.count()
        print(count)
        posts = posts[start:start+size]
        return JsonResponse({
            "posts":[ {
                'post_id':post.id,
                'title':post.title
                       } for post in posts],
            'pagination':{
                'page':page,
                'size':size,
                'count':count,
                'pages':math.ceil(count/size)
            }
        },json_dumps_params={'ensure_ascii':False})
    except Exception as e:
        return  HttpResponseNotFound()



def get(request:HttpRequest,id):

    try:
        post = Post.objects.get(id=int(id))
        return JsonResponse({
            'post':{
                'post':post.id,
                'title':post.title,
                'content':post.content.content,
                'auther':post.auther.name,
                'auther_id':post.auther.id,
                'postdate':post.postdate

            }
        },json_dumps_params={'ensure_ascii':False})

    except Exception as e:
        return  HttpResponseNotFound()