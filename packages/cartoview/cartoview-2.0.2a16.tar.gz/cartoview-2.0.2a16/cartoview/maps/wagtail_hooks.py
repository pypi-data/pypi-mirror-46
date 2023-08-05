from django.conf.urls import re_path
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from wagtail.contrib.modeladmin.helpers import ButtonHelper
from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register
from wagtail.core import hooks

from .models import Map
from .views import wagtail_create_map, wagtail_edit_map


class MapButtonHelper(ButtonHelper):

    # Define classes for our button, here we can set an icon for example
    view_button_classnames = ['button-small', 'icon', 'icon-site']

    def add_button(self, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []
        classnames = self.add_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        return {
            'url': reverse('wagtail_create_map'),
            'label': _('Create a New %s') % self.verbose_name,
            'classname': cn,
            'title': _('Create a New %s') % self.verbose_name,
        }

    def edit_button(self, pk, classnames_add=None, classnames_exclude=None):
        if classnames_add is None:
            classnames_add = []
        if classnames_exclude is None:
            classnames_exclude = []
        classnames = self.edit_button_classnames + classnames_add
        cn = self.finalise_classname(classnames, classnames_exclude)
        return {
            'url': reverse('wagtail_edit_map', kwargs={"map_id": pk}),
            'label': _('Edit'),
            'classname': cn,
            'title': _('Edit this %s') % self.verbose_name,
        }


@hooks.register('register_admin_urls')
def register_admin_urls():
    return [
        re_path(r'^viewer/$', wagtail_create_map, name="wagtail_create_map"),
        re_path(r"^viewer/(?P<map_id>[\d]+)$",
                wagtail_edit_map, name='wagtail_edit_map'),
    ]


class MapModelAdmin(ModelAdmin):
    model = Map
    menu_label = 'Maps'
    menu_icon = 'site'
    menu_order = 200
    add_to_settings_menu = False
    exclude_from_explorer = False
    list_display = ('title', 'projection', 'created_at',
                    'owner')
    list_filter = ('title', 'projection', 'created_at', 'owner__username')
    # search_fields = ('title',)
    button_helper_class = MapButtonHelper


modeladmin_register(MapModelAdmin)
