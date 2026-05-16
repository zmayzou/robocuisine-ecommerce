from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import PromotionCode, Giveaway, Participant


class PromotionListView(View):

    def get(self, request):

        promotion_codes = PromotionCode.objects.filter(
            is_active=True
        )

        giveaways = Giveaway.objects.filter(
            is_active=True
        )

        context = {
            'promotion_codes': promotion_codes,
            'giveaways': giveaways
        }

        return render(
            request,
            'promotions/list.html',
            context
        )


class ParticipateGiveawayView(LoginRequiredMixin, View):

    def get(self, request, giveaway_id):

        giveaway = get_object_or_404(
            Giveaway,
            id=giveaway_id,
            is_active=True
        )

        participant, created = Participant.objects.get_or_create(
            user=request.user,
            giveaway=giveaway,
            defaults={
                'full_name': request.user.get_full_name() or request.user.username,
                'email': request.user.email,
                'phone': ''
            }
        )

        if created:
            messages.success(
                request,
                "Participation enregistrée avec succès. Vous participez maintenant au giveaway."
            )
        else:
            messages.warning(
                request,
                "Vous avez déjà participé à ce giveaway."
            )

        return redirect('promotion_list')