from django.urls import path 
from . import views 
from django.contrib import admin
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('lobby', views.lobby),
    path('lobby1/<int:pk>/', views.lobby1),
    path('thanks/<int:pk>/', views.ThanksPage),
    path('report/', views.Reporting.as_view()),
    path('member/<int:pk>/', views.Member.as_view()),
    path('', views.Dashboard.as_view()),
    path('GeneratePdf/',views.GeneratePdf.as_view()),
    # path('LiveCapture/',views.LiveCapture),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/',LogoutView.as_view(
                    template_name='registration/logged_out.html',
                    next_page=None),name = 'logout')

]