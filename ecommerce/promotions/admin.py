from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import PromotionCode, Giveaway, Participant


@admin.register(PromotionCode)
class PromotionCodeAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'code',
        'discount_percentage',
        'start_date',
        'end_date',
        'is_active'
    ]

    list_filter = [
        'is_active',
        'start_date',
        'end_date'
    ]

    search_fields = [
        'code'
    ]


class ParticipantInline(admin.TabularInline):
    model = Participant
    extra = 0


@admin.register(Giveaway)
class GiveawayAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'title',
        'start_date',
        'end_date',
        'is_active'
    ]

    list_filter = [
        'is_active',
        'start_date',
        'end_date'
    ]

    search_fields = [
        'title'
    ]

    inlines = [ParticipantInline]


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'full_name',
        'email',
        'phone',
        'giveaway',
        'participation_date'
    ]

    search_fields = [
        'full_name',
        'email',
        'phone'
    ]