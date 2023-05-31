from django import forms
import django_filters
from .models import Lead
from enum import Enum

class StarredBooleanFilter(django_filters.BooleanFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['widget'] = forms.Select(
            attrs={'class': 'form-control'},
            choices=[
                ('', 'Tutti'),
                (True, 'Solo preferiti'),
                (False, 'Solo non preferiti')
            ]
        )
        
class ContactedBooleanFilter(django_filters.BooleanFilter):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.extra['widget'] = forms.Select(
            attrs={'class': 'form-control'},
            choices=[
                ('', 'Tutti'),
                (True, 'Solo contattati'),
                (False, 'Solo non contattati')
            ]
        )

class LeadFilter(django_filters.FilterSet):
    city = django_filters.ChoiceFilter(
        choices=[],
        empty_label='Tutte le città',
        label='Città',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    activity_type = django_filters.ChoiceFilter(
        choices=[],
        empty_label='Tutte le attività',
        label='Attività',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    star = StarredBooleanFilter(label='Preferiti')
    
    contacted = ContactedBooleanFilter(label='Contattati')

    def __init__(self, *args, **kwargs):
        leads = kwargs.pop('leads', None)
        super().__init__(*args, **kwargs)
        if leads is not None:
            activity_type = leads.values_list('activity_type', flat=True).distinct().order_by('activity_type')
            cities = leads.values_list('city', flat=True).distinct().order_by('city')
            self.filters['city'].field.choices = [(city, city) for city in cities]
            self.filters['activity_type'].field.choices = [(activity, activity) for activity in activity_type]
        
    class Meta:
        model = Lead
        fields = ['city','activity_type', 'star', 'contacted']
