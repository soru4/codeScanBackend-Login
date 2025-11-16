from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import AuthenticationCode
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.core.exceptions import ValidationError, ObjectDoesNotExist
import json
import random


SENDER_EMAIL = "codescanappcs12001@gmail.com" 


@csrf_exempt #(very secure, very good)
def currentUser(request):
    if request.user.is_authenticated:
        return JsonResponse({'username': request.user.username,'email': request.user.email})
    return JsonResponse({'error': 'No one is logged in right now. '}, status=401)



@csrf_exempt
def login_view(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('pass')
        
        if not all([username, password]):
            return JsonResponse({'error': 'Missing username or password. you didnt write in a username or passWord before sending the request'}, status=400)

        user = authenticate(request, username=username, password=password)
        
        if user is not None:

            login(request, user) 
            
            random_number = random.randint(100000, 999999)
            
            AuthenticationCode.objects.update_or_create(user=user, defaults={'code': random_number})
            
             send_mail("Login Verification Code Scan", f"Hello {user.username} \n \n Here is your email verification code: \n {random_number}\nDo not share this code\n DO NOT REPLY", SENDER_EMAIL, [user.email])
            
            return JsonResponse({'email': user.email, 'message': 'Logged in. Proceed to verification.', 'username' : request.user.username})
        else:
            return JsonResponse({'error': 'Invalid credentials. Your Username and/ Or password are not in the system. '}, status=401)
            
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
    except Exception as e:
        print(f"Login error: {e}")
        return JsonResponse({'error': 'An unexpected server error occurred.'}, status=500)



@csrf_exempt
def register(request):
    try:
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('pass')
        email = data.get('email')

        if not all([username, password, email]):
             return JsonResponse({'error': 'Missing required fields.'}, status=400)
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        login(request, user)
        
        random_number = random.randint(100000, 999999)
        
        AuthenticationCode.objects.update_or_create(user=user, defaults={'code': random_number})
        
        send_mail("Sign Up Verification Code Scan", f"Hello {user.username} \n \n Welcome to Code Scan! \n\n Here is your email verification code: \n\n {random_number}\n\nDo not share this code\n DO NOT REPLY", SENDER_EMAIL, [user.email])
        
        return JsonResponse({'success': 'True', 'message': 'Account created and logged in. YAY everything works!', 'username' : request.user.username})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
    except IntegrityError:
        return JsonResponse({'error': 'Username or Email already exists.'}, status=409)
    except Exception as e:
        print(f"Registration error: {e}")
        return JsonResponse({'error': 'An unexpected server error occurred.'}, status=500)


@csrf_exempt
def emailVerification(request):
    if not request.user.is_authenticated:
        return JsonResponse({'success': 'false', 'error': 'Not logged in.'}, status=401)
        
    try:
        data = json.loads(request.body)
        code = data.get('code')
        
        code_object = AuthenticationCode.objects.get(user=request.user, code=code)
        
        code_object.delete() 
        return JsonResponse({'success': 'true', 'message': 'Email verified.'})

    except json.JSONDecodeError:
        return JsonResponse({'success': 'false', 'error': 'Invalid JSON format.'}, status=400)
    except AuthenticationCode.DoesNotExist:
     
        logout(request)
        return JsonResponse({'success': 'false', 'error': 'Invalid code. type in the right code next time'}, status=403)
    except Exception as e:
        print(f"Verification error: {e}")
        return JsonResponse({'success': 'false', 'error': 'error occurred.'}, status=500)


@csrf_exempt
def leave(request):
    logout(request)
    return JsonResponse({"successful": "yes", 'message': 'Logged out.'})


@csrf_exempt
def sendEmail(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        
        user = User.objects.get(email__iexact=email)
        
        random_number = random.randint(100000, 999999)
        
        AuthenticationCode.objects.update_or_create(
            user=user, 
            defaults={'code': random_number}
        )
        
     
        send_mail(
           "Password Reset Code Scan", 
          f"Hello {user.username} \n \n Here is your password reset code: \n\n {random_number}\n\nDo not share this code\n DO NOT REPLY", 
             SENDER_EMAIL, 
             [user.email]
         )
        
        return JsonResponse({"success": True, 'message': 'Code sent.'})
        
    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON format.'}, status=400)
    except User.DoesNotExist:
        return JsonResponse({"success": True, 'message': 'Code sent.'}) 
    except Exception as e:
        print(f"Send email error: {e}")
        return JsonResponse({'success': False, 'error': 'An error occurred. (Idk when this would trigger ever)'}, status=500)



@csrf_exempt
def resetPass(request):
    try:
        data = json.loads(request.body)
        email = data.get('email')
        code = data.get('code')
        password = data.get('pass')

        user = User.objects.get(email__iexact=email)

        code_object = AuthenticationCode.objects.get(user=user, code=code)
        
        code_object.delete() 

        user.set_password(password)
        user.save()
       
        send_mail( "Password Change Code Scan", f"Hello {user.username} \n \n Your Code Scan account password was just changed. If this was not you, then thats an issue. \n DO NOT REPLY", SENDER_EMAIL, [user.email])
        
        return JsonResponse({"success": "true", 'message': 'Password reset successful.'})

    except json.JSONDecodeError:
        return JsonResponse({'success': 'false', 'error': 'Invalid JSON format.'}, status=400)
    except User.DoesNotExist:
        return JsonResponse({"success": "false", 'error': 'Email not found.'}, status=404)
    except AuthenticationCode.DoesNotExist:
        return JsonResponse({"success": "false", 'error': 'Invalid or expired code.'}, status=403)
    except Exception as e:
        print(f"Reset password error: {e}")

        return JsonResponse({'success': 'false', 'error': 'An unexpected server error occurred.'}, status=500)
