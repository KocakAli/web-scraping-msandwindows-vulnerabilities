from django.urls import path

from . import views

urlpatterns = [

    path('',views.index, name='index'),
    path('order/<str:order>/',views.index, name='index'),
    path('vulns/',views.get_microsoft_vulns, name='get_microsoft_vulns'),
    path('vulns/<int:id>/',views.vuln_detail, name='vuln_detail'),
    path('years/',views.vulnerabilites_years, name='vulnerabilites_years'),
    path('delete/',views.delete_vulns, name='del'),
    

]