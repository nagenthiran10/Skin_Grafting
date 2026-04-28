from django.conf import settings
from django.urls import path
from admins import views
from django.conf.urls.static import static


urlpatterns = [

    # home page......................

    path('', views.home, name='home'),

    # Admin login and logout.......................

    path('adminlogin/', views.adminlogin, name='adminlogin'),
    path('logout/', views.logout, name='logout'),

    # admin home..........................

    path('adminhome/', views.adminhome, name='adminhome'),

    # admin requirements...................................................

    path('requirements/', views.requirements, name='requirements'),

    # admin approve tables for all modules...............................

    path('exfoapprove/', views.exfoapprove, name='exfoapprove'),
    path('bioapprove/', views.bioapprove, name='bioapprove'),
    path('dermatoapprove/', views.dermatoapprove, name='dermatoapprove'),
    path('monitorapprove/', views.monitorapprove, name='monitorapprove'),
    path('evalapprove/', views.evalapprove, name='evalapprove'),

    # admin manage tables for all modules...............................

    path('exfomanage/', views.exfomanage, name='exfomanage'),
    path('biomanage/', views.biomanage, name='biomanage'),
    path('dermatomanage/', views.dermatomanage, name='dermatomanage'),
    path('monitormanage/', views.monitormanage, name='monitormanage'),
    path('evalmanage/', views.evalmanage, name='evalmanage'),

    # manage status...............................................

    path('managestatus/', views.managestatus, name='managestatus'),

    # admin approve and reject.......................................

    path('approve/<int:id>/', views.approve, name='approve'),
    path('reject/<int:id>/', views.reject, name='reject'),

    # generate report .............................................

    path('final_report/<str:project_id>/', views.final_report, name='final_report'),

]
urlpatterns += static(settings.MEDIA_URL,document_root=settings
                      .MEDIA_ROOT)