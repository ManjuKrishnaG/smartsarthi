from django.contrib import admin
from . models import PickupRequest,CustomerAddress,CustomerDetails,ManifestResponse,ShipmentLog,ArchivedPickupRequest

# Register your models here.

admin.site.register(PickupRequest)
admin.site.register(CustomerAddress)
admin.site.register(CustomerDetails)
admin.site.register(ManifestResponse)
admin.site.register(ShipmentLog)
admin.site.register(ArchivedPickupRequest)