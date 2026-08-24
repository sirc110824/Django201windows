from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from sorl.thumbnail import ImageField

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="profile"

    )
    image = ImageField(upload_to='profiles')
    background_image = ImageField(upload_to='backgrounds/', blank=True, null=True)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """create a new profile() object when a Django User is created"""
    if created:
        Profile.objects.create(user=instance)

class Follow(models.Model):
    follower = models.ForeignKey(
        User,
        related_name="following",
        on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User,
        related_name="followers",
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ("follower", "following")