from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse, HttpRequest, JsonResponse,HttpResponseBadRequest
import simplejson
import jwt
from .models import User
import bcrypt
import logging
import datetime
FORMAT = '%(asctime)s  %(message)s'
AUTH_EXPIRE = 60*60*8
logging.basicConfig(format=FORMAT, level=logging.INFO)
# Create your views here.
def gen_token(user_id):
    return jwt.encode({"user_id":user_id, 'exp':int(datetime.datetime.now().timestamp()) + AUTH_EXPIRE},
                      settings.SECRET_KEY, 'HS256').decode()
def reg(request:HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        query = User.objects.filter(email = email)
        
        if query:
            return HttpResponseBadRequest()
        password = bcrypt.hashpw(payload['password'].encode(), bcrypt.gensalt())
        name = payload['name']
        user = User()
        user.email = email
        user.password = password
        user.name = name
        try:
            user.save()
            return JsonResponse({'token':gen_token(user.id)})
        except:raise

    except Exception as e:
        logging.info(e)
        return HttpResponseBadRequest()


def login(request:HttpRequest):
    try:
        payload = simplejson.loads(request.body)
        email = payload['email']
        password = payload['password']
        user = User.objects.filter(email=email).first()
        if not user:
            
            return HttpResponseBadRequest()
        if not bcrypt.checkpw(password.encode(),user.password.encode()):

            return HttpResponseBadRequest()
        return JsonResponse({
            'user':
                {'user_id':user.id,
                 'user_name':user.name,
                 'email':user.email},
            'token': gen_token(user.id)
        })

    except Exception as e:
        logging.info(e)
        return HttpResponseBadRequest()

def authenticate(view):
    def wrapper(request:HttpRequest):
        try:
            token = request.META.get('HTTP_JWT')

            if not token:
                return HttpResponse(status=401)
            try:
                print(token)
                pyload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

            except Exception as e:
                logging.info(e)
                return HttpResponse(status=401)
            # if datetime.datetime.now().timestamp() - pyload['timestamp'] > AUTH_EXPIRE:
            #     return HttpResponse(status=401)
            id = pyload.get('user_id')
            user = User.objects.filter(pk=id).get()
            request.user = user
        except Exception as e:
            print(e)
            return HttpResponse(status=401)
        return view(request)

    return wrapper

@authenticate
def test(request:HttpRequest):
    return JsonResponse({'jwt':'pass'})
