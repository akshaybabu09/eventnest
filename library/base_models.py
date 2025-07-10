from django.db import models


class TimeStampedModel(models.Model):
    """
        Base model from which all other models should inherit.
        It adds the following fields to the model:
        - created_at: The date and time when the object was created
        - updated_at: The date and time when the object was last updated
        - is_active: A boolean indicating whether the object is active or not
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
