
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

from rh.models import Servidor


class EgideAuthBackend(ModelBackend):

    def __create_user(self):
        try:
            user = User.objects.get(username=self.user_data['username'])

            user.email = self.user_data['email']
            user.save()
        except User.DoesNotExist:
            user = User.objects.create_user(
                username=self.user_data['username'],
                email=self.user_data['email'])

        return user

    def __create_servidor(self, user):
        servidor, criado = Servidor.objects.get_or_create(cpf=self.user_data['cpf'], user=user)

        return servidor

    def authenticate(self, request, username=None, password=None, **kwargs):

        user = self.__create_user()
        self.__create_servidor(user)

        return user

    def __init__(self, user_data=None, *args, **kwargs):
        super(EgideAuthBackend, self).__init__(*args, **kwargs)
        self.user_data = user_data
