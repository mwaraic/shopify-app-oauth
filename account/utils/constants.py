from django.conf import settings


class ShopifyOauth:
    API_KEY = '11586c8a379d8f2c402f412a29578a69'
    SECRET_KEY = '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'
    SCOPES = (
        "read_orders,write_orders,read_customers,write_customers,"
        "read_products,write_products,read_content,write_content,"
        "read_price_rules,write_price_rules,read_themes,write_themes"
    )
    ACCESS_MODE = "per_user"
    REDIRECT_ENDPOINT = "/oauth/shopify/authorize"
    ACCESS_TOKEN_HEADER = "X-Shopify-Access-Token"
    ACCESS_TOKEN_ENDPOINT = "/admin/oauth/access_token"
    AUTHORIZE_ENDPOINT = "/admin/oauth/authorize"
    SHOP_DETAILS_ENDPOINT = f"/admin/api/2021-04/shop.json"

SHOPIFY_API_VERSION = "2021-04"