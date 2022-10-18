from django.contrib.auth.models import User
from rest_framework import serializers
from account.utils.constants import ShopifyOauth
from account.utils.helpers import  search_string_match, verify_hash_signature


class ShopifyOauthSerializer(serializers.Serializer):
    code = serializers.CharField(required=False)
    hmac = serializers.CharField(required=True)
    host = serializers.CharField(required=False)
    shop = serializers.CharField(required=True)
    timestamp = serializers.CharField(required=True)
    session = serializers.CharField(required=False)

    def check_signature(self, attrs):
        secret = ShopifyOauth.SECRET_KEY
        hmac = attrs.pop('hmac')
        line = '&'.join([
                        '%s=%s' % (key, value)
                        for key, value in sorted(attrs.items())
                        ])
        is_verified = verify_hash_signature(secret, line, hmac)
        if not is_verified:
            raise serializers.DjangoValidationError(
                {'signature': ["Signature is not valid"]}
            )
        return attrs

    def validate_shop_url(self, shop_url):
        shop_name_regex = search_string_match(r'[^.\s]+\.myshopify\.com', shop_url)
        if shop_name_regex != shop_url:
            raise serializers.DjangoValidationError(
                {'shop_name': ["Shop name does not end with 'myshopify.com'"]}
            )
        return shop_url


class ShopifyUserCreationSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    full_name = serializers.CharField(required=True, max_length=255)
    shop_name = serializers.CharField(required=True, max_length=255)
    token = serializers.CharField(required=True, max_length=255)

    def create(self, validated_data):
        user, _created = User.objects.get_or_create(
            email=validated_data['email'],
        )
        if _created:
            user.username = validated_data['email']
            password = User.objects.make_random_password(length=10)
            user.is_active = True
            user.set_password(password)
            user.first_name = validated_data['full_name']
            user.save()

        return user