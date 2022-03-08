from django.urls import path

from wechat_api import views

urlpatterns = [

    path('login/', views.LoginView.as_view()),
    path('message/', views.messageCode.as_view())
]
