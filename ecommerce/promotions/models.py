from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User


class PromotionCode(models.Model):

    code = models.CharField(
        max_length=50,
        unique=True
    )

    discount_percentage = models.PositiveIntegerField()

    start_date = models.DateField()

    end_date = models.DateField()

    is_active = models.BooleanField(default=True)

    def validate_code(self):
        from django.utils import timezone

        today = timezone.now().date()

        return (
            self.is_active and
            self.start_date <= today <= self.end_date
        )

    def calculate_discount(self, total):
        if self.validate_code():
            return total * self.discount_percentage / 100
        return 0

    def __str__(self):
        return self.code


class Giveaway(models.Model):

    title = models.CharField(max_length=150)

    description = models.TextField()

    start_date = models.DateField()

    end_date = models.DateField()

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def select_winner(self):
        return self.participants.order_by('?').first()

    def __str__(self):
        return self.title


class Participant(models.Model):

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='giveaway_participations'
    )

    giveaway = models.ForeignKey(
        Giveaway,
        on_delete=models.CASCADE,
        related_name='participants'
    )

    full_name = models.CharField(max_length=150)

    email = models.EmailField()

    phone = models.CharField(max_length=20)

    participation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'giveaway')

    def __str__(self):
        return f"{self.full_name} - {self.giveaway.title}"