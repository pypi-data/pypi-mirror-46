from django.utils.translation import ugettext as _
from requests.exceptions import HTTPError
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.serializers import ValidationError
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend
from social_django.utils import load_strategy, load_backend

from drf_jwt_util.views import create_jwt_response

from .serializers import SocialSerializer


class InvalidBackendException(Exception):
    pass


class SocialLoginView(GenericAPIView):
    serializer_class = SocialSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)
        try:
            backend = load_backend(strategy=strategy, name=provider,
                                   redirect_uri=None)
        except MissingBackend:
            raise ValidationError({"provider": _("invalid provider")})
        try:
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get('access_token')
                user = backend.do_auth(access_token)
            else:
                raise InvalidBackendException
        except HTTPError:
            raise ValidationError({"backend error"})
        except InvalidBackendException:
            raise ValidationError({"provider": _("invalid provider")})
        return create_jwt_response(request, user, statuscode=status.HTTP_200_OK)
