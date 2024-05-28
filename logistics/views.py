import requests
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from ticketapp.models import ManifestResponse,PickupRequest,CustomerAddress,CustomerDetails,ShipmentLog
from datetime import datetime

def access_token():
    # Endpoint URL for generating authentication token
    token_generation_url = "http://stageusermanagementapi.xbees.in/api/auth/generateToken"
    
    # Request body containing username, password, and secret key
    payload = {
        "username": "admin@revtitan.com",
        "password": "Admin@123",
        "secretkey": "6f382a9d19dc3cd226f3d74707f5feb9cba2a5e09560a40f135c7c176a042c9c"
    }
    
    # Set headers
    headers = {
        "Content-Type": "application/json",
    }
    
    # Make POST request to generate token
    response = requests.post(token_generation_url, headers=headers, data=json.dumps(payload))
    
    # Check if request was successful
    if response.status_code == 200:
        # Extract token from response JSON
        token = response.json().get("token")
        return token  # Return only the token string
    else:
        # Handle error response
        error_message = response.json().get("error", "Failed to generate token")
        return None

@api_view(['GET','POST'])  
def send_manifest_details(request,ticket_id):
    # URL for sending manifest details
    ticket = get_object_or_404(PickupRequest, id=ticket_id)
    customer_details = get_object_or_404(CustomerDetails,ticket_id=ticket_id)
    customer_address = get_object_or_404(CustomerAddress,customer_details=customer_details)
    manifest_url = "http://api.staging.shipmentmanifestation.xbees.in/shipmentmanifestation/reverse"
    token = access_token()
    #print(token)
    #print(customer_details.customer_name,customer_details.customer_mobile_no,customer_details.customer_email_id,customer_address.house_no,customer_address.address_line_1,customer_address.address_line_2,customer_address.landmark,customer_address.state,customer_address.pincode)
    
    payload = {
            "AirWayBillNO":"" ,
            "OrderNo": ticket.ticket_id,
            "BusinessAccountName": "Titan Reverse",
            "ProductID": ticket.variant_no,
            "Quantity": "1",
            "ProductName": ticket.product_name,
            "Instruction": "",
            "IsCommercialProperty": "",
            "CollectibleAmount": "",
            "ProductMRP": "142.50",
            "DropDetails": {
            "Addresses": [{
            "Type": "Primary",
            "Name": "Titan",
            "Address": "Electronic City",
            "City": "Bengaluru",
            "State": "Karnataka",
            "PinCode": "639004",
            "EmailID": "",
            "Landmark": ""
            }],
            "ContactDetails": [{
            "Type": "Primary",
            "PhoneNo": "8123456789"
            }],
            "IsGenSecurityCode": "",
            "SecurityCode": "",
            "IsGeoFencingEnabled": "",
            "Longitude": "",
            "Latitude": "",
            "RadiusLocation": "",
            "MidPoint": "",
            "MinThresholdRadius": "",
            "MaxThresholdRadius": ""
            },
            "PickupDetails": {
            "Addresses": [{
            "Type": "Primary",
            "Name": customer_details.customer_name,
            "Address": customer_address.address_line_1,
            "City": "",
            "State": customer_address.state,
            "PinCode": customer_address.pincode,
            "EmailID": "",
            "Landmark": ""
            }],
            "ContactDetails": [{
            "Type": "Primary",
            "VirtualNumber": "",
            "PhoneNo": customer_details.customer_mobile_no,
            }],
            "IsPickupPriority":"",
            "PriorityRemarks":"",
            "PickupSlotsDate": "",
            "IsGenSecurityCode": "",
            "SecurityCode": "",
            "IsGeoFencingEnabled": "",
            "Longitude": "",
            "Latitude": "",
            "RadiusLocation": "",
            "MidPoint": "",
            "MinThresholdRadius": "",
            "MaxThresholdRadius": ""
            },
            "PackageDetails": {
            "Dimensions": {
            "Length": "",
            "Width": "",
            "Height": ""
            },
            "Weight": {
            "BillableWeight": "",
            "VolWeight": "",
            "PhyWeight": ""
            }
            },
            "QCTemplateDetails": {
            "TemplateId": "",
            "TemplateCategory": ""
            },
            "TextCapture": [{
            "Label": "",
            "Type": "",
            "ValueToCheck": ""
            }],
            "PickupProductImage": [{
            "ImageUrl": "",
            "TextToShow": ""
            }],
            "CaptureImageRule": {
            "MinImage": "",
            "MaxImage": ""
            },
            "HelpContent": {
            "Description": "",
            "URL": "",
            "IsMandatory": ""
            },
            "GSTMultiSellerInfo": [{
            "InvoiceNumber": "",
            "InvoiceDate": "",
            "InvoiceValue": "",
            "ProductUniqueID": "",
            "IsSellerRegUnderGST": "",
            "BuyerGSTRegNumber": "",
            "SellerName": "Titan",
            "SellerGSTRegNumber": "",
            "SellerAddress": "Test Park, Bengaluru",
            "SupplySellerStatePlace": "",
            "SellerPincode": 454245,
            "EBNExpiryDate": "",
            "EWayBillSrNumber": "",
            "HSNDetails": [{
            "HSNCode": "1234",
            "ProductCategory": "Cases Covers",
            "ProductDesc": "Product Desc",
            "SGSTAmount": "",
            "CGSTAmount": "",
            "IGSTAmount": "",
            "GSTTaxTotal": "",
            "TaxableValue": "",
            "Discount": "",
            "GSTTaxRateCGSTN": "",
            "GSTTaxRateSGSTN": "",
            "GSTTAXRateIGSTN": ""
            }]
            }]
            }
    
    # Set headers including the token
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",  # Include the obtained token here
        "versionnumber": "v1",
        "token": token,
    }
    
    # Make POST request to send manifest details
    response = requests.post(manifest_url, data=json.dumps(payload), headers=headers)
    
     # Parse the response JSON
    response_data = response.json()
    print(response_data)
    
    # Extract required fields
    awb_no = response_data.get("AWBNo")
    return_code = response_data.get("ReturnCode")
    return_message = response_data.get("ReturnMessage")
    
    
    # Check if a record with the same ticket_id exists
    existing_response = ManifestResponse.objects.filter(ticket_id=ticket.ticket_id).first()

    # If a record exists, update it; otherwise, create a new record
    if existing_response:
        existing_response.awb_number = awb_no
        existing_response.return_code = return_code
        existing_response.return_message = return_message
        existing_response.save()
    else:
        manifest_response = ManifestResponse.objects.create(
            ticket_id=ticket.ticket_id,
            awb_number=awb_no,
            return_code=return_code,
            return_message=return_message
        )
    
    # Handle the response code and return appropriate response
    if return_code == 100:
        return Response({"message": "Manifest details sent successfully", "AWBNo": awb_no})
    else:
        return Response({"error": return_message, "AWBNo": awb_no}, status=400)


@api_view(['GET','POST'])
def get_bulk_reverse_manifest_status(request,awb_no):
    # API URL
    api_url = "http://api.staging.shipmenttracking.xbees.in/GetReverseShipmentAuditLog"

    # Get AWB numbers from request data
    token = access_token()
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}",  # Include the obtained token here
        "versionnumber": "v1",
        "token": token,
    }
    # Construct the request JSON
    payload = {
        "AWBNumber": awb_no
    }

    # Make POST request to the API
    response = requests.post(api_url, data=json.dumps(payload),headers=headers)
    response_data = response.json()
    print(response_data)
    return_code = response_data.get("ReturnCode")
    return_message = response_data.get("ReturnMessage")
    shipment_log_details = response_data.get("ShipmentLogDetails", [])

    for log_detail in shipment_log_details:
        shipment_status_datetime = datetime.strptime(log_detail.get("ShipmentStatusDateTime"), '%d-%m-%Y %H:%M:%S')
        existing_log = ShipmentLog.objects.filter(awb_number=awb_no, shipment_status_datetime=shipment_status_datetime).first()

        if existing_log:
            # Update existing record
            existing_log.awb_number = awb_no
            existing_log.shipment_status = log_detail.get("ShipmentStatus")
            existing_log.shipment_status_datetime = shipment_status_datetime
            existing_log.description = log_detail.get("Description")
            existing_log.hub_location = log_detail.get("HubLocation")
            existing_log.city = log_detail.get("City")
            existing_log.state = log_detail.get("State")
            existing_log.process = log_detail.get("Process")
            existing_log.save()
        else:
            # Create new record
            ShipmentLog.objects.create(
                awb_number=awb_no,
                shipment_status=log_detail.get("ShipmentStatus"),
                shipment_status_datetime=shipment_status_datetime,
                description=log_detail.get("Description"),
                hub_location=log_detail.get("HubLocation"),
                city=log_detail.get("City"),
                state=log_detail.get("State"),
                process=log_detail.get("Process")
            )
    if return_code == 100:
        return Response({"message": "Got the tracking details successully"})
    else:
        return Response({"error": return_message}, status=400)
