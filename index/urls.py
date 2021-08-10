from django import urls
from .views import home

urlpatterns = [
    urls.path("", home, name="home")
]
