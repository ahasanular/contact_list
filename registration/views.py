class UserSignUp(CreateAPIView):
    permission_classes = []

    def post(self, request):
        result = {}
        try:
            data = request.data

            if 'full_name' not in data or data['full_name'] == '':
                return Response("Full name can not be null.")
            if 'email' not in data or data['email'] == '':
                return Response("Email can not be null.")
            if 'password' not in data or data['password'] == '':
                return Response("Password can not be null.")

            user = User.objects.filter(email=data['email']).first()

            if user:
                return Response("You have account")

            if not user:
                user = User()
                user.username = data['full_name']
                user.first_name = data['full_name']
                user.email = data['email']
                user.password = make_password(data['password'])
                user.save()
                app_user = AppUser()
                app_user.user = user
                app_user.full_name = data['full_name']
                app_user.email = data['email']
                app_user.save()
