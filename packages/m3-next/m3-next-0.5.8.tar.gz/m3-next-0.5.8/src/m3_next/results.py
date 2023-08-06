import datetime

from django.utils.html import escapejs
from django.utils.safestring import SafeText
from m3 import M3JSONEncoder
from m3.actions import (ActionContext, urls)
from m3.actions.results import PreJsonResult

from m3_next.mapper import get_ui_config


class DataResult(PreJsonResult):
    """
    Результат запроса, возвращающий объект данных
    и доп.настройки для виджета лтображения
    """

    def __init__(self, model, ui, context=None, data=None):
        """
        :model object: объект данных
        :ui string: ключ, идентифицирующий виджет для отображения
        :context object: объект контекста выполнения запроса
        :data dict: доп.данные для инициализации виджета
        """
        data = data or {}
        data['model'] = model
        data['context'] = context or {}
        if data['context'] and 'profile' in data['context'].__dict__:
            del data['context'].profile
        super(DataResult, self).__init__({
            'success': True,
            'code': {
                'data': data,
                'ui': ui,
            }
        })


class UIResult(PreJsonResult):
    """
    Результат, возвращающий виджет в виде конфигурации и данных
    """

    def __init__(self, ui):
        """
        :ui object: либо dict с config+data, либо ExtComponent
        """
        if isinstance(ui, dict):
            assert set(ui.keys()) == set(('config', 'data'))
            code = ui
        else:
            code = {
                'config': ui,
                'data': {}  #ui._data,
            }
        super(UIResult, self).__init__({
            'success': True,
            'code': code
        })
        self.encoder_clz = UIJsonEncoder


class UIJsonEncoder(M3JSONEncoder):
    """
    JSONEncoder, совместимый с клиентским рендерингом
    """

    def default(self, obj):
        if isinstance(obj, ActionContext):
            return dict(
                kv for kv in obj.__dict__.items()
                if not kv[0].startswith('_') and kv[0] != 'profile'
            )
        # для обратной совместимости - выставление некоторых параметров
        # перед рендером (похожее уже делает make_compatible и pregetter)
        # но искать по всему коду - сложно
        if hasattr(obj, 'pre_render'):
            obj.pre_render()

        obj = self.make_compatible(obj)

        cfg = get_ui_config(obj)
        if cfg:
            return cfg
        return super(UIJsonEncoder, self).default(obj)

    @staticmethod
    def make_compatible(obj):
        # TODO: obj.setdefault - нельзя использовать
        # так как будет перекрыто первоначальное значение

        class_name = obj.__class__.__name__

        # ExtContainerTable - это хелпер-класс
        # Для получения extjs-конфига нужно вызвать метод render
        if class_name == 'ExtContainerTable':
            obj.render()
            return obj

            # Проверяются наследники класса BaseExtTriggerField
        # и из fields проставляются fields в store
        elif hasattr(obj, 'store') and hasattr(obj, 'fields'):

            if not getattr(obj.store, 'fields', None):
                fields = obj.fields
                if obj.display_field not in obj.fields:
                    fields = [obj.store.id_property, obj.display_field] + obj.fields
                obj.store.fields = fields

            # if hasattr(obj, 'pack') and obj.pack:
            #     assert isinstance(obj.pack, str) or hasattr(obj.pack, '__bases__'), (
            #         'Argument %s must be a basestring or class' % obj.pack)
            #     pack = ControllerCache.find_pack(obj.pack)
            #     assert pack, 'Pack %s not found in ControllerCache' % pack
            #
            #     # url формы выбора
            #     if not getattr(obj, 'url', None):
            #         if isinstance(pack, ExtMultiSelectField):
            #             obj.url = pack.get_multi_select_url()
            #         else:
            #             obj.url = pack.get_select_url()
            #
            #     # url формы редактирования элемента
            #     if not getattr(obj, 'edit_url', None):
            #         obj.edit_url = pack.get_edit_url()
            #
            #     # url автокомплита и данных
            #     if not getattr(obj, 'autocomplete_url', None):
            #         obj.autocomplete_url = pack.get_autocomplete_url()

        # Для гридов
        elif hasattr(obj, 'columns') and hasattr(obj, 'store'):

            if not getattr(obj.store, 'fields', None):
                fields = [obj.store.id_property] + [
                    col.data_index for col in obj.columns
                    if hasattr(col, 'data_index')]
                obj.store.fields = fields
                # запишем контекст в стор
                obj.store.action_context = obj.action_context

            # для ObjectGrid и ExtMultiGroupinGrid надо проставлять url из
            # экшенов
            has_grid_top_bar = hasattr(obj, 'GridTopBar')
            has_live_grid_top_bar = hasattr(obj, 'LiveGridTopBar')
            if has_grid_top_bar or has_live_grid_top_bar:

                _set_action_url(obj, 'url_new', 'action_new')
                _set_action_url(obj, 'url_edit', 'action_edit')
                _set_action_url(obj, 'url_delete', 'action_delete')
                _set_action_url(obj, 'url_data', 'action_data')
                _set_action_url(obj, 'url_export', 'action_export')

                if has_grid_top_bar:

                    # Настройка постраничного просмотра
                    if obj.allow_paging:
                        obj.paging_bar.page_size = obj.limit
                        obj.bottom_bar = obj.paging_bar

                        if hasattr(obj.store, 'limit'):
                            obj.store.limit = obj.limit

                # store надо обязательно проставить url
                if hasattr(obj, 'url_data'):
                    obj.store.url = getattr(obj, 'url_data')

                # уберем кнопки с гридов, если нет соответствующих экшенов
                def remove(button_name):
                    top_bar = obj.top_bar if has_grid_top_bar else obj._top_bar
                    button = getattr(top_bar, button_name, None)

                    if button and button in top_bar.items:
                        top_bar.items.remove(button)

                if not hasattr(obj, 'url_new') or not obj.url_new:
                    remove('button_new')

                if not hasattr(obj, 'url_edit') or not obj.url_edit:
                    remove('button_edit')

                if not hasattr(obj, 'url_delete') or not obj.url_delete:
                    remove('button_delete')

                if not hasattr(obj, 'url_export') or not obj.url_export:
                    remove('button_export')

        # Для object-tree
        elif hasattr(obj, 'columns') and hasattr(obj, 'row_id_name'):
            _set_action_url(obj, 'url_new', 'action_new')
            _set_action_url(obj, 'url_edit', 'action_edit')
            _set_action_url(obj, 'url_delete', 'action_delete')
            _set_action_url(obj, 'url', 'action_data')

        # для BaseExtTriggerField, нужно поменять режим если указан DataStore
        # if (hasattr(obj, 'store') and hasattr(obj, 'hide_trigger')
        #         and obj.store and obj.store.xtype == 'arraystore'):
        #     obj.mode = 'local'

        # Поля
        if hasattr(obj, 'invalid_class'):
            if getattr(obj, 'read_only', None):
                grey_cls = 'm3-grey-field'
                if getattr(obj, 'cls', None):
                    obj.cls += ' %s' % grey_cls
                obj.cls = grey_cls

            if hasattr(obj, 'regex') and obj.regex:
                obj.regex = '/%s/' % obj.regex

            # if hasattr(obj, 'value'):
            #     # значения типа date и datetime не надо эскейпить
            #     if not isinstance(obj.value, datetime.date):
            #         obj.value = escapejs(obj.value)

        # адресный компонент
        if class_name == 'ExtAddrComponent':
            kladr_pack = urls.get_pack_instance('KLADRPack')
            if kladr_pack:
                obj.get_addr_url = kladr_pack.get_addr_action.absolute_url() if kladr_pack.get_addr_action else ''
                obj.kladr_url = kladr_pack.get_places_action.absolute_url() if kladr_pack.get_places_action else ''
                obj.street_url = kladr_pack.get_streets_action.absolute_url() if kladr_pack.get_streets_action else ''

        return obj


def _set_action_url(obj, url, action):
    """
    Проставляет в объект url если его нет и он есть в соответсвующем экшене
    """
    if getattr(obj, action, None) and not getattr(obj, url, None):
        setattr(obj, url, urls.get_url(getattr(obj, action)))