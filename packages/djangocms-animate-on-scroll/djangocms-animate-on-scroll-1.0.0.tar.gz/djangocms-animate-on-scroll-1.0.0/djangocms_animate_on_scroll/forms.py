from django.forms.models import ModelForm
from django import forms
from .consts import *


class AnimateOnScroll_Element_Form(ModelForm):

    aos_animation = forms.ChoiceField(choices=AOS_ANIMATIONS)

    aos_easing = forms.ChoiceField(choices=AOS_EASING, required=False)

    aos_anchor_placement = forms.ChoiceField(choices=AOS_ANCHOR_PLACEMENT, required=False)