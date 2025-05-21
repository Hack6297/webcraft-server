SECRET_KEY = 'test'
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = ['channels']
ASGI_APPLICATION = 'webcraft.asgi.application'
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }
}
