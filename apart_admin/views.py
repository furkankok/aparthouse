from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apart.models import Apart, ApartBillDetail, ApartCategory, ApartDistance, ApartFirm, ApartImage, ApartService, ApartUniversity, City, Town
from django.utils import timezone
from django.http import JsonResponse

@login_required
def index(request):
    apart_firms = ApartFirm.objects.filter(add_by=request.user, deleted_at__isnull=True)
    return render(request, 'apart_admin/index.html', {
        'apart_firms': apart_firms
    })

@login_required
def firma_ekle(request):

    if request.method == 'POST':
        ApartFirm.objects.create(
            name = request.POST['name'],
            phone = request.POST['phone'],
            mail = request.POST['mail'],
            image = request.FILES['image'],
            address = request.POST['address'],
            add_by = request.user
        )

        messages.success(request, 'Firma başarıyla eklendi.')

        return redirect('index')

    return render(request, 'apart_admin/firma_ekle.html')


@login_required
def firma_duzenle(request, firm_id):
    firm = ApartFirm.objects.filter(id=firm_id, add_by=request.user).first()
    if not firm:
        messages.error(request, 'Firma bulunamadı.')
        return redirect('index')
    
    if request.method == 'POST':
        firm.name = request.POST['name']
        firm.phone = request.POST['phone']
        firm.mail = request.POST['mail']
        if 'image' in request.FILES:
            firm.image = request.FILES['image']
        firm.address = request.POST['address']
        firm.is_approved = False
        firm.save()

        messages.success(request, 'Firma başarıyla düzenlendi.')

        return redirect('index')

    return render(request, 'apart_admin/firma_duzenle.html', {
        'firm': firm
    })

@login_required
def firma_sil(request, firm_id):
    firm = ApartFirm.objects.filter(id=firm_id, add_by=request.user).first()
    if not firm:
        messages.error(request, 'Firma bulunamadı.')
        return redirect('index')
    
    firm.deleted_at = timezone.now()
    firm.save()

    messages.success(request, 'Firma başarıyla silindi.')

    return redirect('index')

@login_required
def apart_ekle(request, firm_id):
    firm = ApartFirm.objects.filter(id=firm_id, add_by=request.user).first()
    if not firm:
        messages.error(request, 'Firma bulunamadı.')
        return redirect('index')

    if request.method == 'POST':
        category = ApartCategory.objects.filter(id=request.POST['apart-category']).first()
        towm = Town.objects.filter(id=request.POST['town']).first()
        services = request.POST.getlist('services')
        bills = request.POST.getlist('bills')

        services = ApartService.objects.filter(id__in=services)
        bills = ApartBillDetail.objects.filter(id__in=bills)

        # apart = Apart(
        #     add_by = request.user,
        #     firma = firm,
        #     name = request.POST['name'],
        #     category = category,
        #     price = request.POST['price'],
        #     price_type = request.POST['price-type'],
        #     info = request.POST['apart-aciklama'],
        #     address = request.POST['apart-adres'],
        #     lat = request.POST['apart-lat'],
        #     lon = request.POST['apart-lng'],
        #     town = towm,
        # )
        if request.POST.get('apart_id'):
            apart = Apart.objects.filter(id=request.POST.get('apart_id')).first()
            if not apart:
                messages.error(request, 'Apart bulunamadı.')
                return redirect('index')
        else:
            apart = Apart()

        apart.add_by = request.user
        apart.firma = firm
        apart.name = request.POST['name']
        apart.category = category
        apart.price = request.POST['price']
        apart.price_type = request.POST['price-type']
        apart.info = request.POST['apart-aciklama']
        apart.address = request.POST['apart-adres']
        apart.lat = request.POST['apart-lat']
        apart.lon = request.POST['apart-lng']
        apart.town = towm
        apart.save()
        apart.services.set(services)
        apart.bills.set(bills)


        apart.save()

        for image in request.FILES.getlist('files'):
            ApartImage.objects.create(
                add_by = request.user,
                apart = apart,
                image = image
            )
        
        
        for index, university_id in enumerate(request.POST.getlist('university_id')):
            distance = ApartDistance(
                apart = apart,
                university_id = university_id,
                yurume = request.POST.getlist('yurume')[index],
                otobus = request.POST.getlist('otobus')[index],
                tramvay = request.POST.getlist('tramway')[index]
            )

            distance.save()



    categories = ApartCategory.objects.all()

    price_types = Apart.PriceType.choices
    citys = City.objects.all()

    services = ApartService.objects.all()
    bills = ApartBillDetail.objects.all()

    return render(request, 'apart_admin/apart_ekle.html', {
        'firm': firm,
        'categories': categories,
        'price_types': price_types,
        'citys': citys,
        'services': services,
        'bills': bills
    })

@login_required
def get_town(request):
    city_id = request.GET.get('city_id')
    city = City.objects.filter(id=city_id).first()
    if not city:
        return JsonResponse({
            'status': 'error',
            'message': 'İl bulunamadı.'
        })

    towns = city.towns.all()
    universitys = ApartUniversity.objects.filter(city=city)

    return JsonResponse({
        'status': 'ok',
        'towns': list(towns.values('id', 'name')),
        'universitys': list(universitys.values('id', 'name'))
    })


@login_required
def apartlar(request, firm_id):
    firm_id = ApartFirm.objects.filter(id=firm_id, add_by=request.user).first()
    if not firm_id:
        messages.error(request, 'Firma bulunamadı.')
        return redirect('index')
    
    apartlar = Apart.objects.filter(firma=firm_id, deleted_at__isnull=True)
    for apart in apartlar:
        img = apart.images.filter(cover=True).last()
        if not img:
            img = apart.images.first()
        setattr(apart, 'image', img)

    return render(request, 'apart_admin/apartlar.html', { 'apartlar': apartlar, "firma": firm_id })


@login_required
def apart_duzenle(request, firm_id, apart_id):
    firm = ApartFirm.objects.filter(id=firm_id, add_by=request.user).first()
    if not firm:
        messages.error(request, 'Firma bulunamadı.')
        return redirect('index')
    
    apart = Apart.objects.filter(id=apart_id, firma=firm, deleted_at__isnull=True).first()
    if not apart:
        messages.error(request, 'Apart bulunamadı.')
        return redirect('index')
    categories = ApartCategory.objects.all()

    price_types = Apart.PriceType.choices
    citys = City.objects.all()

    services = ApartService.objects.all()
    bills = ApartBillDetail.objects.all()
    
    return render(request, 'apart_admin/apart_ekle.html', { 
        'apart': apart,
        'firm': firm,
        'categories': categories,
        'price_types': price_types,
        'citys': citys,
        'services': services,
        'bills': bills 
    })







