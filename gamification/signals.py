from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum
from .models import Point, Leaderboard


@receiver(post_save, sender=Point)
def update_leaderboard(sender, instance, created, **kwargs):
    if created:
        leaderboard, _ = Leaderboard.objects.get_or_create(user=instance.user)
        leaderboard.total_points = (
            instance.user.points.aggregate(total=Sum("value"))["total"] or 0
        )
        leaderboard.save()
