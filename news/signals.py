""" Signals for the MostOdd News application. """


# Import Django's built-in signal for saving models
from django.db.models.signals import post_save

# Register the signal receiver
from django.dispatch import receiver

# Import Django's Group model
from django.contrib.auth.models import Group

# Import the CustomUser model
from .models import CustomUser


# ---------------------------------------------------------
# Automatically assign a new user to the correct Django Group
# ---------------------------------------------------------
@receiver(post_save, sender=CustomUser)
def assign_user_to_group(sender, instance, created, **kwargs):
    """
    Automatically add a newly created user to the
    appropriate Django Group based on their role.
    """

    # Only run when a new user is created
    if created:

        # Get or create the Reader group
        if instance.role == "reader":
            group, created = Group.objects.get_or_create(name="Reader")
            instance.groups.add(group)

        # Get or create the Journalist group
        elif instance.role == "journalist":
            group, created = Group.objects.get_or_create(name="Journalist")
            instance.groups.add(group)

        # Get or create the Editor group
        elif instance.role == "editor":
            group, created = Group.objects.get_or_create(name="Editor")
            instance.groups.add(group)