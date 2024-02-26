from django.db import models
# Create your models here.

class RightsSupport(models.Model):
            
    class Meta:
        
        managed = False
                
        default_permissions = ()

        permissions = ( 
            ('yonetici', 'Yönetici'),  
        )


class ApartUniversity(models.Model):

    add_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255, null=True, blank=True)
    city = models.ForeignKey('City', on_delete=models.CASCADE, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='university_images/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city,
            "country": self.country,
            "address": self.address,
            "lat": self.lat,
            "lon": self.lon,
            "image": self.image.url if self.image else None
        }
    



class ApartCategory(models.Model):
    add_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    icon = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon
        }


class ApartServiceCategory(models.Model):
    add_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=255)
    icon = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon
        }

class ApartService(models.Model):
    add_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    icon = models.TextField(null=True, blank=True)
    category = models.ForeignKey(ApartServiceCategory, on_delete=models.CASCADE, related_name='services')

    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "category": self.category.id
        }


class ApartBillDetail(models.Model):
    add_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class City(models.Model):
    add_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, null=True, blank=True, default='Türkiye')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country
        }

class Town(models.Model):
    add_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='towns')

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "city": self.city.id
        }



class ApartFirm(models.Model):
    add_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
    mail = models.EmailField(null=True, blank=True)
    image = models.ImageField(upload_to='firm_images/', null=True, blank=True)
    
    address = models.TextField(null=True, blank=True)

    is_approved = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return self.name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "phone": self.phone,
            "mail": self.mail,
        }


class Apart(models.Model):

    class PriceType(models.TextChoices):
        MONTH = 'Aylık'
        YEAR = 'Yıllık'
        SEASON = 'Sezonluk'

    add_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)

    firma = models.ForeignKey(ApartFirm, on_delete=models.CASCADE, related_name='aparts', null=True, blank=True)

    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(ApartCategory, on_delete=models.CASCADE, related_name='aparts', null=True, blank=True)
    mail = models.EmailField(null=True, blank=True)

    price = models.FloatField(null=True, blank=True)
    price_type = models.CharField(max_length=10, choices=PriceType.choices, null=True, blank=True)


    # price_month = models.FloatField(null=True, blank=True)
    # price_year = models.FloatField(null=True, blank=True)
    # price_season = models.FloatField(null=True, blank=True)

    info = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    town = models.ForeignKey(Town, on_delete=models.CASCADE, related_name='aparts', null=True, blank=True)

    universitys = models.ManyToManyField(ApartUniversity, related_name='aparts')
    services = models.ManyToManyField(ApartService, related_name='aparts')
    bills = models.ManyToManyField(ApartBillDetail, related_name='aparts')

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name



class ApartImage(models.Model):
    add_by = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True)

    image = models.ImageField(upload_to='apart_images/')
    apart = models.ForeignKey(Apart, on_delete=models.CASCADE, related_name='images')

    cover = models.BooleanField(default=False, )

    created_at = models.DateTimeField(auto_now_add=True)

    
    def __str__(self):
        return self.image.name

    def to_dict(self):
        return {
            "id": self.id,
            "image": self.image.url,
            "apart": self.apart.id
        }


class ApartDistance(models.Model):

    university = models.ForeignKey(ApartUniversity, on_delete=models.CASCADE, related_name='distances')
    apart = models.ForeignKey(Apart, on_delete=models.CASCADE, related_name='distances')

    yurume = models.IntegerField(null=True, blank=True)
    otobus = models.IntegerField(null=True, blank=True)
    tramvay = models.IntegerField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.university.name

    def to_dict(self):
        return {
            "id": self.id,
            "university": self.university.to_dict(),
            "yurume": self.yurume,
            "otobus": self.otobus,
            "tramvay": self.tramvay
        }



