"""TwitterProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from twitterapp import views
from django.conf.urls import url,include
from allauth.account import views as auth_views



urlpatterns = [
    url(r"^$", auth_views.LoginView.as_view()),

    path('admin/', admin.site.urls),
    url(r'^home/$', views.HomePage.as_view(), name='home'),
    url(r'^save_topic/$', views.HomePage.as_view()),
    url(r'^accounts/', include('allauth.urls')),


    # Topics related paths
    path('topics/', views.TopicView.as_view(), name='topics'),
    path('topics/new', views.TopicFormView.as_view(), name='new_topic'),
    path('topic/<int:topic_id>/show', views.TopicConversationView.as_view(), name='show_topic'),
    path('topics/all_topics', views.AllTopicView.as_view(), name='all_topics'),
    path("topics/<int:pk>/delete", views.delete_topic, name='delete_topic'),

    # Comments related paths
    path('comments/new', views.CommentView.as_view(), name='new_comment'),
    path("comments/<int:pk>/delete", views.delete_comment, name='delete_comment'),



    path("subscribe/<int:pk>/topic", views.subscribe_topic, name='subscribe_topic'),
    path('unsubscribe/<int:pk>', views.unsubscribe_topic, name='unsubscribe_topic'),



]
