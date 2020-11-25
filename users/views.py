import json
import re
import jwt
import bcrypt

from django.views import View
from django.http import JsonResponse
from django.conf import settings

from .utils import login_decorator
from .models import User

class UserView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            email_check = re.compile('^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$')

            if not re.match(email_check, data['email']):
                return JsonResponse({'message' : 'INVALID_EMAIL'}, status=400)

            if len(data['password']) < 6:
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message' : 'EXIST_EMAIL'}, status=400)

            password         = data['password'].encode('utf-8')
            hashed_password  = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')

            User.objects.create(
                name      = data['name'],
                email     = data['email'],
                password  = hashed_password)
            return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
        except (AttributeError, TypeError):
            return JsonResponse({'message' : 'PASSWORD_MUST_BE_STRING_TYPE'}, status=400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message' : 'REQUEST_IS_NONE'}, status=400)

    @login_decorator
    def patch(self, request):
        data     = json.loads(request.body)
        user     = User.objects.get(id=request.user.id)
        context  = {}

        if data.get('imageURL',None):
            user.profile_image   = data['imageURL']
            context['imageURL']  = user.profile_image

        if data.get('password',None):
            if len(data['password']) < 6:
                return JsonResponse({'message' : 'INVALID_PASSWORD'}, status=400)
            password         = data['password'].encode('utf-8')
            hashed_password  = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf-8')
            user.password    = hashed_password
            context['password'] = 'SUCCESS'

        if data.get('name',None):
            user.name        = data['name']
            context['name']  = user.name

        user.save()
        return JsonResponse(context, status=200)

    @login_decorator
    def get(self, request):
        user = User.objects.get(id=request.user.id)
        context = {
            'id'        : user.id,
            'name'      : user.name,
            'email'     : user.email,
            'imageURL'  : user.profile_image
        }
        return JsonResponse(context, status=200)

    @login_decorator
    def delete(self, request):
        user = User.objects.get(id=request.user.id).delete()
        return JsonResponse({'message' : 'SUCCESS'}, status=204)

class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            if 'email' not in data or 'password' not in data:
                return JsonResponse({'message' : 'KEY_ERROR'}, status=400)
              
            if not User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message' : 'EMAIL_ERROR'}, status=400)
            user = User.objects.get(email=data['email'])

            if not bcrypt.checkpw(data['password'].encode('utf-8'),user.password.encode('utf-8')):
                return JsonResponse({'message' : 'WRONG_PASSWORD'}, status=400)
            SECRET        = settings.SECRET_KEY
            access_token  = jwt.encode({'id':user.id},SECRET, algorithm='HS256')
            access_token  = access_token.decode('utf-8')
            return JsonResponse({'token':access_token}, status=200)

        except (AttributeError, TypeError):
            return JsonResponse({'message' : 'ALL_KEY_TYPE_MUST_BE_STRING'}, status=400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'message' : 'REQUEST_IS_NONE'}, status=400)
