from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.dashboard),
    url(r'^wish_items/create$', views.createItem),
    url(r'^wish_items/created$', views.create),
    url(r'^wish_items/show/(?P<item_id>\d+)$', views.showItem),
    url(r'^wish_items/(?P<item_id>\d+)/join$', views.joinItem),
    url(r'^wish_items/(?P<item_id>\d+)/removefromlist$', views.itemRemoved),
    url(r'^wish_items/(?P<item_id>\d+)/delete$', views.itemDelete),
    url(r'^logout$', views.logout),
   
]