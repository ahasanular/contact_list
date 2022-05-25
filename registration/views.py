from django.shortcuts import render
from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils import json
from .models import AppUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import HttpResponseRedirect
import secrets
from threading import Thread
from contact_list.settings import ALLOWED_HOSTS

# Create your views here.
def sign_up(request):
    return render(request, 'sign_up.html')

def verification(request, email, otp):
    return render(request, 'verification.html')

def sign_in(request):
    return render(request, 'sign_in.html')


def sign_out(request):
    response = HttpResponseRedirect('/')
    response.delete_cookie('access')
    response.delete_cookie('user_name')
    return response


# APIs

def send_email(to, subject, body):
    smtp_server='smtp.gmail.com'
    smtp_port='465'
    sender_email='projecttestmail8@gmail.com'
    sender_password='projectTesting'
    server = None
    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.ehlo()  # Can be omitted
        server.login(sender_email, sender_password)
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = to
        msg['Subject'] = subject


        html = """\
        <html>
            <head></head>
            <body>
        """
        html += body
        """
            </body>
        </html>
        """
        msg.attach(MIMEText(html,'html'))
        server.sendmail(
            from_addr=sender_email,
            to_addrs=to,
            msg = msg.as_string())
        print("Mail Send")
    except Exception as ex:
        print(str(ex))
    finally:
        if server != None:
            server.quit()

def send_email_thread(to, subject, body):
    thread = Thread(target=send_email,args=(to, subject, body))
    thread.start()

class UserSignUp(CreateAPIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        result = {}
        try:
            data = request.data
            # data = json.loads(request.body)

            if 'full_name' not in data or data['full_name'] == '':
                return Response("Full name can not be null.")
            if 'email' not in data or data['email'] == '':
                return Response("Email can not be null.")
            if 'password' not in data or data['password'] == '':
                return Response("Password can not be null.")

            username = data['email'].split('@')
            user = User.objects.filter(username=username[0]).first()

            if not user:
                user = User()
                user.username = username[0]

                name = data['full_name'].split(' ')
                user.first_name = name[0]
                if len(name) > 1:
                    name.remove(name[0])
                    name = ' '.join(name)
                    user.last_name = name

                user.email = data['email']
                user.password = make_password(data['password'])
                user.is_active = False

                otp = secrets.token_hex(25)

                app_user = AppUser()
                app_user.user = user
                app_user.full_name = data['full_name']
                app_user.email = data['email']
                app_user.otp = otp

                user.save()
                app_user.save()

                server_root = "https://" + ALLOWED_HOSTS[1] + "/registration/verification/"
                activation_link = server_root + data['email'] + "/" + otp + "/"

                send_email_thread(data['email'], "Verification for " + data['account_type'] + " Sign Up", "To confirm your mail and activate your account please click in this LINK : " + activation_link)

                result['message'] = "Success"
                result['status'] = status.HTTP_200_OK
                return Response(result)

            else:
                if user.is_active:
                    result['message'] = "An Account Exists with this Email !"
                    result['status'] = status.HTTP_208_ALREADY_REPORTED
                    return Response(result)
                else:
                    result['message'] = "Un Active Account Found !"
                    result['email'] = user.email
                    result['status'] = status.HTTP_401_UNAUTHORIZED
                    return Response(result)

        except Exception as ex:
            result['message'] = str(ex)
            result['status'] = status.HTTP_400_BAD_REQUEST
            return Response(result)


class UserSignIn(CreateAPIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        result = {}
        try:
            data = json.loads(request.body)
            print(data)
            if 'email' not in data or data['email']=='':
                result['message']="Email can not be null."
                result['Error']="Email"
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            if 'password' not in data or data['password'] == '':
                result['message'] = "Password can not be null."
                result['Error'] = "Password"
                return Response(result, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(email=data['email']).first()
            if not user:
                result = {
                    'message': 'Please create a account'
                }
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            elif not user.is_active:
                result = {
                    'message': 'Please activate your account'
                }
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            else:
                if not check_password(data['password'], user.password):
                    result['message'] = "Invalid credentials"
                    return Response(result, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    app_user = AppUser.objects.filter(user=user).first()
                    refresh_token = RefreshToken.for_user(user)
                    data = {
                        'user_name': user.username,
                        'slug': app_user.slug,
                        'access': str(refresh_token.access_token),
                        'token': str(refresh_token),
                        'status': status.HTTP_200_OK
                    }
                    return Response(data)
        except Exception as e:
            result = {}
            result['status'] = status.HTTP_400_BAD_REQUEST
            result['message'] = str(e)
            return Response(result)




