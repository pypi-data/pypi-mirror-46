# -*- coding: utf-8 -*-
"""
Enables the user to add style plugin that displays a html tag with
the provided settings from the style plugin.
"""
from __future__ import unicode_literals

from cms.models import CMSPlugin
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext_lazy as _
from djangocms_attributes_field.fields import AttributesField
from django.utils.text import slugify
from django.db.models.deletion import SET_NULL
import json


@python_2_unicode_compatible
class AnimateOnScroll_Anchor(CMSPlugin):
    id_name = models.CharField(
        verbose_name=_('ID name'),
        max_length=255,
    )
    def __str__(self):
        return self.id_name

    def clean(self):
        valid_id_name = slugify(self.id_name)
        self.id_name = valid_id_name


@python_2_unicode_compatible
class AnimateOnScroll_Element(CMSPlugin):

    # AOS Standard
    # --------------------------------
    aos_animation = models.CharField(verbose_name=_('AOS Animation'),
                                        max_length=255,
                                        help_text=_('Script will trigger "animation_name" animation on this element, if you scroll to it.'))

    aos_easing = models.CharField(verbose_name=_('Anchor Easing'),
                                    blank=True,
                                    max_length=255,
                                    help_text=_('Choose timing function to ease elements in different ways'))

    # AOS Anchors
    # --------------------------------
    aos_anchor_placement = models.CharField(verbose_name=_('Anchor Placement'),
                                            blank=True,
                                            max_length=255,
                                            help_text=_(
                                                'Anchor placement - which one position of element on the screen should trigger animation'))

    aos_anchor = models.ForeignKey(AnimateOnScroll_Anchor,
                                    verbose_name=_("Animate On Scroll Anchor"),
                                    related_name="aos_anchor",
                                    blank=True,
                                    null=True,
                                    help_text=_('Anchor element, whose offset will be counted to trigger animation instead of actual elements offset'),
                                    on_delete=SET_NULL)

    # AOS Advanced
    # --------------------------------
    aos_offset = models.IntegerField(verbose_name=_('Offset'),
                                     default=120,
                                     help_text=_('Change offset to trigger animations sooner or later (px)'))
    aos_duration = models.IntegerField(verbose_name=_('Duration'),
                                       default=400,
                                       help_text=_('*Duration of animation (ms)'))
    aos_delay = models.IntegerField(verbose_name=_('Delay'),
                                    default=0,
                                    help_text=_('Delay animation (ms)'))
    aos_once = models.BooleanField(verbose_name=_('Once'),
                                   default=False,
                                   help_text=_('Choose wheter animation should fire once, or every time you scroll up/down to element'))


    # Default id/classes/attributes
    # --------------------------------
    id_name = models.CharField(
        verbose_name=_('ID name'),
        blank=True,
        max_length=255,
    )
    additional_classes = models.CharField(
        verbose_name=_('Additional classes'),
        blank=True,
        max_length=255,
        help_text=_('Additional comma separated list of classes '
            'to be added to the element e.g. "row, column-12, clearfix".'),
    )
    attributes = AttributesField(
        verbose_name=_('Attributes'),
        blank=True,
        excluded_keys=['class', 'id', 'style'],
    )

    def get_aos_once(self):
        return json.dumps(self.aos_once)

    def get_additional_classes(self):
        return ' '.join(item.strip() for item in self.additional_classes.split(',') if item.strip())


    def __str__(self):
        return ('%s - ' % self.aos_animation) + self.aos_anchor_placement + self.id_name or str(self.pk)
