from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )
    
    def __str__(self):
        return self.user.username
 
    
# Create a profile for each new user.
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        # We want to follow our own profile to see our own musings and rediculousness
        # user_profile = Profile(user=instance, follows=[instance])
        
        user_profile = Profile(user=instance)
        user_profile.save()
        
        # Implementation 01: Using .set() for adding single objects to many-to-many relationships
        # user_profile.follows.set([instance.profile.id])
        
        # Implementation 02: Using .add() for adding single objects to many-to-many relationships
        user_profile.follows.add(instance.profile)
        user_profile.save()
        
# Previous method without using the decorator @receiver
# post_save.connect(create_profile, sender=User)


class Dweet(models.Model):
    user = models.ForeignKey(
        User, related_name="dweets", on_delete=models.DO_NOTHING
    )
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)


    # Option 02
    # We can set our ordering in our model class.
    # This will be the default ordering for the object, for use
    # when obtaining lists of objects. 
    # class Meta:
    #     ordering = ['-created_at']


    def __str__(self):
        return (
            f"{self.user} "
            f"({self.created_at:%Y-%m-%d %H:%M}): "
            f"{self.body[:30]}..."
        )
