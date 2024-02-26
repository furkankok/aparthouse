from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from apart.models import Apart, ApartBillDetail, ApartCategory, ApartFirm, ApartService, ApartUniversity, City
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
        print(request.POST)
        print(request.FILES)




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
