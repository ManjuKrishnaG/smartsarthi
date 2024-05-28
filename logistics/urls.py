from django.urls import path
from . import views

urlpatterns = [
    path('access-token/',views.access_token,name='access-token'),
    path('send_manifest_details/<str:ticket_id>',views.send_manifest_details,name='send_manifest_details'),
    path('get_bulk_reverse_manifest_status/<str:awb_no>',views.get_bulk_reverse_manifest_status,name='get_bulk_reverse_manifest_status'),
]
	