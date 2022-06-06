from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('add_post/', views.add_post, name='add_post_form'),
    path('blog/', views.redirect_from_blog, name='redirect-to-main'),
    path('<slug:slug>/', views.post_detail, name='post_detail'),   
]