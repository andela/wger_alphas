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
from django.http import HttpResponseForbidden
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy, ugettext as _
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from wger.nutrition.forms import MealItemForm
from wger.nutrition.models import Meal, MealItem
from wger.utils.generic_views import (
    WgerFormMixin,
    WgerDeleteMixin
)


logger = logging.getLogger(__name__)


class MealItemDeleteView(WgerDeleteMixin, LoginRequiredMixin, DeleteView):
    '''
    Generic view to delete a meal item
    '''
    model = MealItem
    fields = ('amount',)
    messages = ugettext_lazy('Successfully deleted')
    form_action_urlname = 'nutrition:meal_item:delete'

    def get_context_data(self, **kwargs):
        context = super(MealItemDeleteView, self).get_context_data(**kwargs)
        context['form_action'] = reverse(
            'nutrition:meal_item:delete', kwargs={'pk': self.object.id})
        context['title'] = _(u"Delete '{0}'?").format(self.object)

        return context

    def get_success_url(self):
        return reverse(
            'nutrition:plan:view', kwargs={'id': self.object.meal.plan_id})


class MealItemCreateView(WgerFormMixin, CreateView):
    '''
    Generic view to create a new meal item
    '''

    model = MealItem
    form_class = MealItemForm
    template_name = 'meal_item/edit.html'

    def dispatch(self, request, *args, **kwargs):
        '''
        Check that the user owns the meal
        '''
        meal = get_object_or_404(Meal, pk=kwargs['meal_id'])
        if meal.plan.user == request.user:
            self.meal = meal
            return super(MealItemCreateView, self).dispatch(
                request, *args, **kwargs)
        else:
            return HttpResponseForbidden()

    def get_success_url(self):
        return reverse('nutrition:plan:view', kwargs={'id': self.meal.plan.id})

    def get_context_data(self, **kwargs):
        '''
        Send some additional data to the template
        '''
        context = super(MealItemCreateView, self).get_context_data(**kwargs)
        context['form_action'] = reverse('nutrition:meal_item:add',
                                         kwargs={'meal_id': self.meal.id})
        context['ingredient_searchfield'] = self.request.POST.get(
            'ingredient_searchfield', '')
        return context

    def form_valid(self, form):
        '''
        Manually set the corresponding meal
        '''
        form.instance.meal = self.meal
        form.instance.order = 1
        return super(MealItemCreateView, self).form_valid(form)


class MealItemEditView(WgerFormMixin, UpdateView):
    '''
    Generic view to update an existing meal item
    '''

    model = MealItem
    form_class = MealItemForm
    title = ugettext_lazy('Edit meal item')
    form_action_urlname = 'nutrition:meal_item:edit'
    template_name = 'meal_item/edit.html'

    def get_success_url(self):
        return reverse(
            'nutrition:plan:view', kwargs={'id': self.object.meal.plan.id})

    def get_context_data(self, **kwargs):
        '''
        Send some additional data to the template
        '''
        context = super(MealItemEditView, self).get_context_data(**kwargs)
        context['ingredient_searchfield'] = self.object.ingredient.name
        return context
