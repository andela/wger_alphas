# -*- coding: utf-8 -*-

# This file is part of wger Workout Manager.
#
# wger Workout Manager is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# wger Workout Manager is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
import logging

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy, ugettext as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from django.views.generic import CreateView, UpdateView, DeleteView

from wger.nutrition.forms import MealItemFormSet
from wger.nutrition.models import (NutritionPlan, Meal, MealItem)
from wger.utils.generic_views import (
    WgerFormMixin,
    WgerDeleteMixin
)

logger = logging.getLogger(__name__)


# ************************
# Meal functions
# ************************

class MealCreateView(WgerFormMixin, CreateView):
    '''
    Generic view to add a new meal to a nutrition plan
    '''

    model = Meal
    fields = '__all__'
    title = ugettext_lazy('Add new meal')
    template_name = 'meal/add.html'
    owner_object = {'pk': 'plan_pk', 'class': NutritionPlan}

    def form_valid(self, form):
        plan = get_object_or_404(
            NutritionPlan, pk=self.kwargs['plan_pk'], user=self.request.user)
        form.instance.plan = plan
        form.instance.order = 1
        self.object = form.save()

        context = self.get_context_data()
        meal_item_formset = context['meal_item']
        if meal_item_formset.is_valid():
            for meal_item in meal_item_formset:
                cleaned = meal_item.cleaned_data
                amount = cleaned.get('amount')
                weight_unit = cleaned.get('weight_unit')
                ingredient = cleaned.get('ingredient')
                if weight_unit:
                    meal_item = MealItem(
                        meal=self.object, order=1, amount=amount,
                        weight_unit=weight_unit, ingredient=ingredient)
                else:
                    meal_item = MealItem(
                        ingredient=ingredient, meal=self.object, order=1,
                        amount=amount)
                meal_item.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return self.object.plan.get_absolute_url()

    # Send some additional data to the template
    def get_context_data(self, **kwargs):
        context = super(MealCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['meal_item'] = MealItemFormSet(self.request.POST)
        else:
            context['meal_item'] = MealItemFormSet()

        context['form_action'] = reverse(
            'nutrition:meal:add',
            kwargs={'plan_pk': self.kwargs['plan_pk']})

        return context


class MealEditView(WgerFormMixin, UpdateView):
    '''
    Generic view to update an existing meal
    '''

    model = Meal
    fields = '__all__'
    title = ugettext_lazy('Edit meal')
    form_action_urlname = 'nutrition:meal:edit'

    def get_success_url(self):
        return self.object.plan.get_absolute_url()


class MealDeleteView(WgerDeleteMixin, LoginRequiredMixin, DeleteView):
    '''
    Generic view to delete a meal item
    '''
    model = Meal
    fields = ('time',)
    messages = ugettext_lazy('Successfully deleted')
    form_action_urlname = 'nutrition:meal:delete'

    def get_context_data(self, **kwargs):
        context = super(MealDeleteView, self).get_context_data(**kwargs)
        context['form_action'] = reverse(
            'nutrition:meal:delete', kwargs={'pk': self.object.id})
        context['title'] = _(u"Delete '{0}'?").format(self.object)

        return context

    def get_success_url(self):
        return self.object.plan.get_absolute_url()
