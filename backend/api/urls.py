# urls.py

from django.urls import path
from .views import client_registration, freelancer_registration,client_login,freelancer_login,client_profile
from django.contrib.auth.views import LogoutView


urlpatterns = [
   path('client/register/',client_registration,name='client_registration') ,
   path('freelancer/register/',freelancer_registration,name='freelancer_registration'),
   path('client/login/',client_login,name= 'client_login'),
   path('freelancer/login/',freelancer_login,name= 'freelancer_login'),
   path('client/logout/', LogoutView.as_view(), name='client-logout'),
   path('freelancer/logout/', LogoutView.as_view(), name='freelancer-logout'),
   path('client/profile/', client_profile , name='client-profile')
    
]
