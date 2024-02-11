from django.shortcuts import render
from apart.models import Apart, ApartBillDetail, ApartImage, ApartServiceCategory
from oauth2_provider.decorators import protected_resource
from utils import error_response, success_response
from django.http import Http404
from django.conf import settings

@protected_resource()
def apart_detail(request, apart_id):
    apart = Apart.objects.filter(id=apart_id).last()
    if apart is None:
        raise Http404("Apart not found")


    apart_images = ApartImage.objects.filter(apart=apart)

    return success_response(data={
        "id": apart.id,
        "name": apart.name,
        "price": apart.price,
        "category": apart.category.to_dict() if apart.category else None,
        "phone": apart.phone,
        "info": apart.info,
        "address": apart.address,
        "lat": apart.lat,
        "lon": apart.lon,
        "universitys": [university.to_dict() for university in apart.universitys.all()],
        "service_categories": [service_category.to_dict() for service_category in ApartServiceCategory.objects.all()],
        "services": [service.to_dict() for service in apart.services.all()],
        "bill_details": [bill_detail.to_dict() for bill_detail in apart.bills.all()],
        "all_bills": [bill_detail.to_dict() for bill_detail in ApartBillDetail.objects.all()],
        "images": [settings.BACKEND_URL + image.image.url for image in apart_images]
    })







