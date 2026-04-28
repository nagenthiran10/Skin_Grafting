from django.urls import path
from monitoring import views

urlpatterns = [
    path('monitor_home/',views.monitor_home),

    path('monitor_login/',views.monitor_login),
    path('monitor_register/',views.monitor_register),

    path('dermatoreports/', views.monitor_req_result),

    path('getkey_monitor/<str:project_id>/', views.getkey_monitor),
    path('decrypt_data_monitor/<str:project_id>/', views.decrypt_data_monitor),


    path('monitorscan/',views.monitorscan),
    path('monitor_calculation/<str:project_id>/',views.monitor_calculation),


    path('monitorfile/',views.monitorfile),


    path('monitor_logout/',views.monitor_logout),

]