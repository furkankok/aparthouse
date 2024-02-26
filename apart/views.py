from django.shortcuts import render
from django.core.paginator import Paginator
from apart.models import Apart, ApartBillDetail, ApartDistance, ApartImage, ApartServiceCategory
from oauth2_provider.decorators import protected_resource
from user_preview.models import ApartComment
from utils import error_response, success_response
from django.http import Http404
from django.conf import settings


from hitcount.models import HitCount
from hitcount.views import HitCountMixin

# @protected_resource()
def apart_detail(request, apart_id):
    apart = Apart.objects.filter(id=apart_id).last()
    if apart is None:
        raise Http404("Apart not found")


    apart_images = ApartImage.objects.filter(apart=apart)

    hit_count = HitCount.objects.get_for_object(apart)
    HitCountMixin.hit_count(request, hit_count)
    hit_count.refresh_from_db()

    data = {
        "id": apart.id,
        "name": apart.name,
        "price": apart.price,
        "price_type": apart.price_type,
        "category": apart.category.to_dict() if apart.category else None,
        "phone": apart.phone,
        "mail": apart.mail,
        "info": apart.info,
        "address": apart.address,
        "lat": apart.lat,
        "lon": apart.lon,
        "universitys": [university.to_dict() for university in apart.universitys.all()],
        "service_categories": [service_category.to_dict() for service_category in ApartServiceCategory.objects.all()],
        "services": [service.to_dict() for service in apart.services.all()],
        "bill_details": [bill_detail.to_dict() for bill_detail in apart.bills.all()],
        "all_bills": [bill_detail.to_dict() for bill_detail in ApartBillDetail.objects.all()],
        "images": [settings.BACKEND_URL + image.image.url for image in apart_images],
        "town": None,
        "city": None,
        "hit_count": hit_count.hits,
        "comments": [],
        "distances": []

    }

    if apart.town:
        data["town"] = apart.town.to_dict()
        data["city"] = apart.town.city.to_dict()

    comments = ApartComment.objects.filter(apart=apart, is_approved = True).order_by("-create_time")
    # pagination
    page = request.GET.get("page", 1)
    per_page = 10
    paginate = Paginator(comments, per_page)
    comments = paginate.get_page(page)
    data["comments"] = [comment.to_dict() for comment in comments]


    distances = ApartDistance.objects.filter(apart=apart)
    data["distances"] = [distance.to_dict() for distance in distances]

    return success_response(data=data)


@protected_resource()
def apart_comment(request, apart_id):
    
    apart = Apart.objects.filter(id=apart_id).last()
    if apart is None:
        raise Http404("Apart not found")
    
    user = request.user
    comment = request.POST.get("comment")
    if not comment or comment == "":
        return error_response("Yorum gereklidir.")
    
    apart_comment = ApartComment.objects.filter(user=user, apart=apart).last()
    if apart_comment:
        return error_response("Bu konaklamaya daha önce yorum yapılmıştır.")
    
    apart_comment = ApartComment.objects.create(user=user, apart=apart, comment=comment)

    return success_response()



