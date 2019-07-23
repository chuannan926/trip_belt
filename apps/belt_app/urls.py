from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index), 
    url(r'^process_reg$',views.process_reg),
    url(r'^process_log$',views.process_log),
    url(r'^dashboard$', views.dashboard),
    url(r'^logout$', views.logout),


    url(r'^trips/new$', views.new),
    url(r'^process_new_trip$', views.process_new_trip),

    url(r'^trip/(?P<trip_id>\d+)/remove$', views.remove_trip),
    url(r'^trip/(?P<trip_id>\d+)$', views.view_trip),


    url(r'^edit/(?P<trip_id>\d+)$', views.view_edit_trip), 
    url(r'^process_edit_trip/(?P<trip_id>\d+)$', views.process_edit_trip),

    
]