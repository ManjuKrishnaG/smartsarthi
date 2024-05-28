from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class PickupRequest(models.Model):
    STATUS_CHOICES = (
        ('Accepted', 'Accepted'),
        ('Declined', 'Declined'),
        ('Open', 'Open'),
    )
                                                               
    ticket_id = models.CharField(max_length=20, unique=True)
    new_ticket_id = models.CharField(max_length=20, unique=True, blank=True, null=True)
    product_name = models.CharField(max_length=255)
    variant_no = models.CharField(max_length=50)
    problem_category = models.CharField(max_length=100)
    problem_description = models.TextField()
    date_of_purchase = models.DateField()
    invoice_copy = models.ImageField(upload_to='attachments',blank=True, null=True)
    video_of_issue = models.FileField(upload_to='attachments',blank=True, null=True)
    front_image = models.ImageField(upload_to='attachments',blank=True, null=True)
    back_image = models.ImageField(upload_to='attachments',blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    remarks = models.TextField(max_length=250, blank=True, null=True)
    locked = models.BooleanField(default=False)
    locked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    locked_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation


    def save(self, *args, **kwargs):
        # Generate a new_ticket_id if it doesn't exist
        if not self.new_ticket_id:
            self.new_ticket_id = self.generate_new_ticket_id()

        if self.locked and not self.locked_at:
            self.locked_at = timezone.now()

        super().save(*args, **kwargs)

    def generate_new_ticket_id(self):
        # Get the original ticket ID
        original_ticket_id = self.ticket_id
        # Append 'SF' to the original ticket ID
        new_ticket_id = f'{original_ticket_id}SF'

        return new_ticket_id
    
    def __str__(self):
        return f"PickupRequest - Ticket ID: {self.ticket_id}, New Ticket ID: {self.new_ticket_id}"
    


class CustomerDetails(models.Model):
    ticket_id = models.OneToOneField(PickupRequest, on_delete=models.CASCADE)
    customer_name = models.CharField(max_length=255)
    customer_mobile_no = models.CharField(max_length=15, null=True)
    customer_email_id = models.EmailField()

    def __str__(self):
        return f"CustomerDetails - Ticket ID: {self.ticket_id}, Customer Name: {self.customer_name}"

class CustomerAddress(models.Model):
    house_no = models.CharField(max_length=10)
    customer_details = models.OneToOneField(CustomerDetails, on_delete=models.CASCADE)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    city =models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)

    def __str__(self):
        return f"CustomerAddress - Ticket ID: {self.customer_details.ticket_id}, Customer Name: {self.customer_details.customer_name}"

class ManifestResponse(models.Model):
    ticket_id = models.CharField(max_length=20)
    awb_number = models.CharField(max_length=20)
    return_code = models.IntegerField()
    return_message = models.CharField(max_length=255)

    def __str__(self):
        return f"ManifestResponse - AWB Number: {self.awb_number}"
    
class ShipmentLog(models.Model):
    awb_number = models.CharField(max_length=20)
    shipment_status = models.CharField(max_length=100)
    shipment_status_datetime = models.DateTimeField()
    description = models.CharField(max_length=100)
    hub_location = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    process = models.CharField(max_length=100)

    def __str__(self):
        return self.awb_number
    
class ArchivedPickupRequest(models.Model):
    ticket_id = models.CharField(max_length=20)  # Remove unique=True
    product_name = models.CharField(max_length=255)
    variant_no = models.CharField(max_length=50)
    problem_category = models.CharField(max_length=100)
    problem_description = models.TextField()
    date_of_purchase = models.DateField()
    invoice_copy = models.TextField(blank=True, null=True)
    video_of_issue = models.TextField(blank=True, null=True)
    front_image = models.TextField(blank=True, null=True)
    back_image = models.TextField(blank=True, null=True)
    
    # Fields from CustomerDetails model
    customer_name = models.CharField(max_length=255)
    customer_mobile_no = models.CharField(max_length=15, null=True)
    customer_email_id = models.EmailField()

    # Fields from CustomerAddress model
    house_no = models.CharField(max_length=10)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True, null=True)
    landmark = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)
    
    remarks = models.TextField(max_length=250, blank=True, null=True)
    created_at = models.DateTimeField()  # Timestamp for creation

    def __str__(self):
        return f"ArchivedPickupRequest - Ticket ID: {self.ticket_id}"