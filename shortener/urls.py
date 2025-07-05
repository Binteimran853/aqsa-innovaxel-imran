from django.urls import path,include,re_path

from .views import (
    CreateShortURL,
    RetrieveOriginalURLView,
    UpdateShortURL,
    DeleteShortURL,
    GetStats,home,RedirectToOriginal
)

urlpatterns = [
    path('',home,name="home"),
    path('shorten/', CreateShortURL.as_view()),
    path('retrieve/', RetrieveOriginalURLView.as_view(), name='retrieve_url'),
    path('shorten/<str:shortCode>/stats/', GetStats.as_view(), name='GetStats'),             # GET
 
path('shorten/update/', UpdateShortURL.as_view(), name='update_url'),


# urls.py
 path('shorten/<str:shortCode>/delete/', DeleteShortURL.as_view(), name='delete_short_url'),

     # DELETE
    re_path(r'^(?P<shortCode>[a-zA-Z0-9]{6})/$', RedirectToOriginal.as_view(), name='redirect'),


]
