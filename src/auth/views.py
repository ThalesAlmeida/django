from django.conf import settings
from django.contrib.auth import login, logout
from django.http.response import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic.base import View

from requests_oauthlib import OAuth2Session

from auth.backends import EgideAuthBackend


class LoginView(View):
    def get(self, request):
        if not request.user or request.user.is_anonymous:
            oauth = OAuth2Session(token=request.session['access_token'])
            user_data = oauth.get(settings.EGIDE_API, verify=False).json()

            user = EgideAuthBackend(user_data).authenticate(request)
            user.backend = 'auth.backends.EgideAuthBackend'

            login(request, user)
        else:
            user = self.request.user

        # servidor = get_object_or_404(Servidor, cpf=request.POST.get('cpf'))
        return HttpResponseRedirect(reverse_lazy('rh:home'))
        # return HttpResponseRedirect(reverse('rh:pesquisa_cpf'))


class LogoutView(View):
    def get(self, request):
        if request.user and request.user.is_authenticated:
            logout(request)

        return HttpResponseRedirect('{}/logout/?next={}/login'.format(
            settings.EGIDE_URL, settings.RECADASTRAMENTO_URL))
