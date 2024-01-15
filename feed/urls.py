from django.urls import path
from . import views
urlpatterns=[
    path('', views.feed, name='home' ),
    path('add_ingridients', views.add_ingridient, name='add_ingridient'),
    path('feed_store', views.feed_store, name='feed_store'),
    path('delete/<int:id>', views.delete, name='delete'),
    path('edit/<int:id>', views.edit, name='edit'),




]