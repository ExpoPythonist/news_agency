from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginAPIView.as_view(), name='login'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('stories/', views.NewsStoryView.as_view(), name='stories'),
    path('stories/<uuid:pk>/', views.NewsStoryDeleteView.as_view(), name='stories_delete'),

    path('directory/', views.DirectoryAPIView.as_view(), name='directory'),

]
