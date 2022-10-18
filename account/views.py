from django.http.response import HttpResponseRedirect
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


from account.serializers import ShopifyOauthSerializer, ShopifyUserCreationSerializer
from account.utils.constants import ShopifyOauth
from account.utils.oauth_client import ShopifyOauthClient


class ShopifyOauthRedirectAPIView(GenericAPIView):
    """Redirects to Shopify to confirm permissions
    """
    permission_classes = [AllowAny]
    serializer_class = ShopifyOauthSerializer

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)
        if serializer.is_valid(raise_exception=True):
            oauth_client = ShopifyOauthClient(shop_name=request.query_params['shop'])
            redirect_url = oauth_client.build_oauth_redirect_url(request.build_absolute_uri())
        return HttpResponseRedirect(redirect_to=redirect_url)


class ShopifyUserCreationAPIView(GenericAPIView):
    """Creates new user for Shopify Public App
    """
    permission_classes = [AllowAny]
    serializer_class = ShopifyOauthSerializer

    def get(self, request):
        serializer = self.get_serializer(data=request.query_params)

        return HttpResponseRedirect(redirect_to='http://localhost:8000/accounts/shopify/login/?shop=birds-eye-global&process=login&next=%2Fsignup')
                