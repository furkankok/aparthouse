from django.db import models

# Create your models here.


class ApartUniversity(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    country = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)
    image = models.ImageField(upload_to='university_images/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

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
    name = models.CharField(max_length=255)
    icon = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon
        }


class ApartServiceCategory(models.Model):
    name = models.CharField(max_length=255)
    icon = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon
        }

class ApartService(models.Model):
    name = models.CharField(max_length=255)
    icon = models.TextField(null=True, blank=True)
    category = models.ForeignKey(ApartServiceCategory, on_delete=models.CASCADE, related_name='services')

    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "icon": self.icon,
            "category": self.category.id
        }


class ApartBillDetail(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }


class Apart(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(null=True, blank=True)
    phone = models.CharField(max_length=255, null=True, blank=True)
    category = models.ForeignKey(ApartCategory, on_delete=models.CASCADE, related_name='aparts', null=True, blank=True)

    info = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    lat = models.FloatField(null=True, blank=True)
    lon = models.FloatField(null=True, blank=True)

    universitys = models.ManyToManyField(ApartUniversity, related_name='aparts')
    services = models.ManyToManyField(ApartService, related_name='aparts')
    bills = models.ManyToManyField(ApartBillDetail, related_name='aparts')




class ApartImage(models.Model):
    image = models.ImageField(upload_to='apart_images/')
    apart = models.ForeignKey(Apart, on_delete=models.CASCADE, related_name='images')

    created_at = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        return {
            "id": self.id,
            "image": self.image.url,
            "apart": self.apart.id
        }

# yorumlar ....







