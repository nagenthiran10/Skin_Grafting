from django.urls import path
from evaluation import views

urlpatterns = [


    path('eval_home/',views.eval_home),

    path('eval_register/',views.eval_register),
    path('eval_login/',views.eval_login),
    path('eval_home/',views.eval_home),

    path('monitorreports/', views.eval_req_result),

    path('getkey_eval/<str:project_id>/', views.getkey_eval),
    path('decrypt_data_eval/<str:project_id>/', views.decrypt_data_eval),



    path('eval_scan/',views.eval_scan),
    path('eval_file/',views.eval_file),


    path('calculate_existing/<str:project_id>/',views.calculate_existing),
    path('calculate_proposed/<str:project_id>/',views.calculate_proposed),



    path('eval_logout/',views.eval_logout),


]