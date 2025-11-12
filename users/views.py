from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import AuthenticationCode
from django.contrib.auth import logout
import random
from django.views.decorators.csrf import csrf_exempt
import json
from django.contrib.auth.models import User
@csrf_exempt
def currentUser(request):
    response={
        'username': request.user.username,
        'email' : request.user.email,
        }
    return JsonResponse(response)
@csrf_exempt
def login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('pass')
    user = authenticate(request, username = username, password = password)
    login(request, user)
    response={
        'email' : user.email
        }
    random_number = random.randint(100000, 999999)
    c = AuthenticationCode(user = user, code = random_number)
    send_mail("Login Verification Code Scan", f"Hello {user.username} \n \n Here is your email verification code: \n {random_number}\nDo not share this code\n DO NOT REPLY", "codescanappcs12001@gmail.com", [user.email])
    c.save()
    return JsonResponse(response)
@csrf_exempt
def emailVerification(request):
    data = json.loads(request.body)
    code = data.get('code')
    for x in AuthenticationCode.objects.all():
        if x.user == request.user:
            if int(code) == x.code:
                response={'success' : 'true'}
                x.delete()
                return JsonResponse(response)
    logout(request)
    response={'success' : 'false'}
    return JsonResponse(response)


@csrf_exempt
def leave(request):
    logout(request)
    return JsonResponse({"successful" : "yes" })

@csrf_exempt
def register(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('pass')
    email = data.get('email')
    user = User.objects.create_user(username=username,email=email, password=password)
    user.save()
    if user != None:
        login(request, user)
        random_number = random.randint(100000, 999999)
        c = AuthenticationCode(user = user, code = random_number)
        send_mail("Sign Up Verification Code Scan", f"Hello {user.username} \n \n Welcome to Code Scan! \n\n Here is your email verification code: \n\n {random_number}\n\nDo not share this code\n DO NOT REPLY", "codescanappcs12001@gmail.com", [user.email])
        c.save()
    response = {'success' : 'True'}
    return JsonResponse(response)
@csrf_exempt
def resetPass(request):
    data = json.loads(request.body)
    email = data.get('email')
    code = data.get('code')
    password = data.get('pass')
    found = False
    for x in AuthenticationCode.objects.all():
        if x.user == request.user:
            if int(code) == x.code:
                x.delete()
                found = True
                break
    if found == False:
        return JsonResponse({"not found" : "true"})
    for u in User.objects.all():
        if u.email == email:
            u.set_password(password)
            send_mail("Password Change Code Scan", f"Hello {u.username} \n \n Your Code Scan account password was just changed. If this was not you, then thats an issue. \n DO NOT REPLY", "codescanappcs12001@gmail.com", [u.email])
    return JsonResponse({"not found" : "false"})

@csrf_exempt
def sendEmail(request):
    data = json.loads(request.body)
    email = data.get('email')
    for u in User.objects.all():
        if u.email == email:
            random_number = random.randint(100000, 999999)
            c = AuthenticationCode(user = u, code = random_number)
            send_mail("Sign Up Verification Code Scan", f"Hello {u.username} \n \n Welcome to Code Scan! \n\n Here is your email verification code: \n\n {random_number}\n\nDo not share this code\n DO NOT REPLY", "codescanappcs12001@gmail.com", [u.email])
            c.save()

