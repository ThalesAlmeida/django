import re

from django.conf import settings
from django.http import HttpResponseRedirect

from requests_oauthlib import OAuth2Session

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]


if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class EgideAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if not request.user or request.user.is_anonymous:
            path = request.path_info.lstrip('/')

            # skip for non-required authentication urls
            if not any(m.match(path) for m in EXEMPT_URLS):
                response_code = request.GET.get('code')

                oauth = OAuth2Session(
                    settings.EGIDE_CLIENT_ID,
                    redirect_uri=settings.EGIDE_REDIRECT_URI)

                if response_code:
                    token = oauth.fetch_token(
                        verify=False,
                        code=response_code,
                        token_url=settings.EGIDE_TOKEN_URL,
                        client_secret=settings.EGIDE_CLIENT_SECRET)
                    # raise Exception(token)
                    request.session['access_token'] = token
                else:
                    authorize_url = oauth.authorization_url(
                        settings.EGIDE_AUTHORIZE_URL)[0]
                    # raise Exception(authorize_url)
                    return HttpResponseRedirect(authorize_url)

        return self.get_response(request)
