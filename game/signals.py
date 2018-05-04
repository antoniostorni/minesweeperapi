# Signal to create grid structure on creating the grid model
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Grid


@receiver(post_save, sender=Grid)
def set_last_message(sender, instance, created, **kwargs):
    if created:
        Grid.build_grid_squares_structure(instance)


