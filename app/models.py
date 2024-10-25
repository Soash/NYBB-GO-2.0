from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Team(models.Model):
    name = models.CharField(max_length=20)
    score = models.IntegerField(default=0)
    n_score = models.IntegerField(default=0)
    clue = models.IntegerField(default=5)
    quiz_1_status = models.BooleanField(default=False)
    quiz_2_status = models.BooleanField(default=False)
    quiz_3_status = models.BooleanField(default=False)
    quiz_4_status = models.BooleanField(default=False)
    quiz_5_status = models.BooleanField(default=False)
    quiz_6_status = models.BooleanField(default=False)
    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    log = models.TextField(default="", null=True, blank=True)

    def __str__(self):
        return f"Team: {self.name}"
    
    @property
    def duration(self):
        if self.start_time is None or self.end_time is None:
            return "Pending"
        duration = self.end_time - self.start_time
        return f"{duration.total_seconds() / 60} minutes"




@receiver(post_save, sender=User)
def create_team_for_new_user(sender, instance, created, **kwargs):
    if created:
        Team.objects.create(user=instance, name=instance.username)


