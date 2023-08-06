# -*- coding: utf-8 -*-
from django.utils.translation import ugettext_lazy as _

from cms.plugin_pool import plugin_pool
from cms.plugin_base import CMSPluginBase

from .models import AnimateOnScroll_Element, AnimateOnScroll_Anchor
from .forms import AnimateOnScroll_Element_Form

class AnimateOnScroll_Anchor_Plugin(CMSPluginBase):
    model = AnimateOnScroll_Anchor
    name = _('AnimateOnScroll - Anchor')
    module = _('Animate On Scroll')
    render_template = 'djangocms_animate_on_scroll/aos_anchor.html'

    fieldsets = (
        (None, {
            'fields': (
                'id_name',
            )
        }),
    )


plugin_pool.register_plugin(AnimateOnScroll_Anchor_Plugin)


class AnimateOnScroll_Element_Plugin(CMSPluginBase):
    model = AnimateOnScroll_Element
    name = _('AnimateOnScroll - Element')
    module = _('Animate On Scroll')
    render_template = 'djangocms_animate_on_scroll/aos_element.html'
    allow_children = True
    form = AnimateOnScroll_Element_Form

    fieldsets = (
        (None, {
            'fields': (
                'aos_animation',
                'aos_easing',
            )
        }),
        (_('AOS Anchor settings'), {
            'fields': (
                'aos_anchor_placement',
                'aos_anchor',
            ),
        }),
        (_('AOS Advanced settings'), {
            'classes': ('collapse',),
            'fields': (
                ('aos_offset',
                 'aos_duration',
                 'aos_delay',
                 'aos_once'),
            ),
        }),
        (_('Advanced Element settings'), {
            'classes': ('collapse',),
            'fields': (
                'id_name',
                 'additional_classes',
                 'attributes',
            ),
        }),
    )


plugin_pool.register_plugin(AnimateOnScroll_Element_Plugin)
