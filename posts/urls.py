from django.urls import path
from . import views
app_name = 'posts'

urlpatterns = [
    path('<int:post_pk>/comments/<int:comment_pk>/delete/', views.comments_delete, name='comments_delete'),
    path('<int:post_pk>/comments', views.comments_create, name='comments_create'),
    path('<int:post_pk>/delete/', views.delete, name='delete'),
    path('<int:post_pk>/update/', views.update, name='update'),
    path('<int:post_pk>/', views.detail, name='detail'),
    path('create/', views.create, name='create'),
    path('', views.list, name='list'),
    ]