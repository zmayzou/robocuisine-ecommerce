from django.urls import path

from .views import PromotionListView, ParticipateGiveawayView


urlpatterns = [
    path('', PromotionListView.as_view(), name='promotion_list'),

    path(
        'giveaway/<int:giveaway_id>/participate/',
        ParticipateGiveawayView.as_view(),
        name='participate_giveaway'
    ),
]