from django.db import models
from django.utils import timezone

# Create your models here.

class UserInfo(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    email_token_used = models.BooleanField(default=False)

    forget_password_token = models.CharField(max_length=100, null=True, blank=True)
    forget_password_token_used = models.BooleanField(default=False)
    
    create_time = models.DateTimeField(default=timezone.now)


class ApartComment(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    apart = models.ForeignKey('apart.Apart', on_delete=models.CASCADE)
    comment = models.TextField()

    is_approved = models.BooleanField(default=False)

    create_time = models.DateTimeField(default=timezone.now)

    def to_dict(self):
        return {
            'id': self.id,
            'user': self.user.username[:3] + "*****" + self.user.username[-3:],
            'apart': self.apart.id,
            'comment': self.comment,
            'create_time': self.create_time
        }