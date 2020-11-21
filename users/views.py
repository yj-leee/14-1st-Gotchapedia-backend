import json
import re
import jwt
import bcrypt

from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from django.conf import settings
from .utils import login_decorator
from .models import User

class UserView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            email_check = re.compile('^[a-zA-Z0-9-_]+@[a-zA-Z0-9]+\.[a-zA-Z0-9]+$')
            if not re.match(email_check, data['email']):
                return JsonResponse({'message' : 'EMAIL_ERROR'}, status=400)

            if len(data['password']) < 6:
                return JsonResponse({'message' : 'PASSWORD_ERROR'}, status=400)

            if User.objects.filter(email=data['email']).exists():
                return JsonResponse({'message' : 'EMAIL_ERROR'}, status=400)

            password         = data['password'].encode('utf-8')
            hashed_password  = bcrypt.hashpw(password, bcrypt.gensalt())
            decode_password  = hashed_password.decode('utf-8')

            User.objects.create(
                name      = data['name'],
                email     = data['email'],
                password  = decode_password)
            return JsonResponse({'message' : 'SUCCESS'}, status=200)

        except Exception:
            return JsonResponse({'message' : 'ERROR'}, status=400)

class LoginView(View):
    def post(self, request):
        data = json.loads(request.body)
        try:
            if 'email' not in data:
                return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])
            return JsonResponse({'message' : 'EMAIL_ERROR'}, status=400)

            if bcrypt.checkpw(data['password'].encode('utf-8'),user.password.encode('utf-8')):
                SECRET        = settings.SECRET_KEY
                access_token  = jwt.encode({'id':user.id},SECRET, algorithm='HS256')
                access_token  = access_token.decode('utf-8')
                return JsonResponse({'token':access_token}, status=200)
            return JsonResponse({'message' : 'Login Failed - Wrong Password'}, status=400)

        except Exception:
            return JsonResponse({'message' : 'ERROR'}, status=400)
