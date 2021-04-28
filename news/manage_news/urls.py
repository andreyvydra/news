from django.urls import path
from . import views

urlpatterns = [
    path('', views.MainView.as_view()),
    path('login', views.LoginView.as_view()),
    path('logout', views.Logout.as_view()),
    path('news', views.AddNewsView.as_view()),
    path('news/<int:news_id>', views.EditNewsView.as_view()),
    path('news_delete/<int:news_id>', views.DeleteNewsView.as_view())
]
