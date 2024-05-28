from django.urls import path
from . import views

urlpatterns = [
    path('index/',views.index,name='index'),
    path('ticket_reports/',views.ticket_reports,name='ticket_reports'),
    path('dashboard_ticket_details/<str:tkt_id>',views.dashboard_ticket_details,name='dashboard_ticket_details'),
    path('dashboard_customer_details/<str:tkt_id>',views.dashboard_customer_details,name='dashboard_customer_details'),
    
    path('ticket_list/',views.ticket_list,name='ticket_list'),
    path('accepted_ticket_list/',views.accepted_ticket_list,name='accepted_ticket_list'),
    path('declined_ticket_list/',views.declined_ticket_list,name='declined_ticket_list'),
    path('all_ticket_list',views.all_ticket_list,name="all_ticket_list"),
    path('ticket_details/<str:tkt_id>/', views.ticket_details, name='ticket_details'),
    path('customer_details/<str:tkt_id>/', views.customer_details,name='customer_details'),
    
    path('accept_ticket/<str:ticket_id>/', views.accept_ticket, name='accept_ticket'),
    path('decline_ticket/<str:ticket_id>/', views.decline_ticket, name='decline_ticket'),
    path('errorpage/',views.errorpage,name='errorpage'),

    path('display_ticket_list/',views.display_ticket_list,name='display_ticket_list'),
    path('receive_image/',views.receive_image,name='receive_image'),

    path('send_status/<str:ticket_id>/',views.send_status,name='send_status'),

    path('track_package/<str:awb_no>/',views.track_package,name='track_package'),
    path('track/',views.track,name='track'),
    path('profile/',views.profile,name='profile'),
    path('download-excel/', views.download_excel, name='download_excel'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    path('search_ticket/', views.search_ticket, name='search_ticket'),

]