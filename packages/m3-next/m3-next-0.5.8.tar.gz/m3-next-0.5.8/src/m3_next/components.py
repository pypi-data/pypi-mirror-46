from django.conf import settings
from m3.actions import ActionContext
from m3_ext.ui.base import BaseExtComponent, ExtUIComponent
from m3_ext.ui.containers import (ExtToolBar, ExtForm, ExtPanel, ExtTitlePanel,
                                  ExtTabPanel, ExtFieldSet, ExtGrid,
                                  ExtContextMenu, ExtContextMenuItem,
                                  ExtContainer, ExtToolbarMenu,
                                  ExtContainerTable)
from m3_ext.ui.containers.base import BaseExtContainer, BaseExtPanel
from m3_ext.ui.containers.context_menu import ExtContextMenuSeparator
from m3_ext.ui.containers.grids import (
    BaseExtGridColumn, ExtGridBooleanColumn, ExtGridCheckColumn,
    ExtGridNumberColumn, ExtGridDateColumn)
from m3_ext.ui.controls import ExtButton
from m3_ext.ui.fields import (BaseExtField, BaseExtTriggerField, ExtStringField,
    ExtDateField, ExtNumberField, ExtHiddenField, ExtTextArea, ExtCheckBox,
    ExtRadio, ExtComboBox, ExtTimeField, ExtDisplayField, ExtDictSelectField,
    ExtSearchField, ExtMultiSelectField, ExtFileUploadField,
    ExtImageUploadField)
from m3_ext.ui.fields.simple import ExtDateTimeField, ExtAdvTimeField
from m3_ext.ui.misc import ExtJsonStore, ExtDataStore, ExtLabel
from m3_ext.ui.misc.base_store import BaseExtStore
from m3_ext.ui.misc.store import ExtMultiGroupingStore
from m3_ext.ui.panels import ExtMultiGroupinGrid
from m3_ext.ui.windows import ExtWindow, ExtEditWindow
from m3_ext.ui.windows.base import BaseExtWindow

from m3_next.mapper import reg_js_mapping, getter, suppress_if_None


def getter_window_title(obj, attr):
    if attr == 'title':
        if settings.DEBUG:
            # Для облегчения документирования, выводим название класса
            # окна в его заголовке.
            return '%s [%s]' % (obj.title, obj.__class__.__name__)


def getter_form(obj, attr):
    if attr == 'form' and hasattr(obj, attr):
        return obj.form.item_id


def getter_form_url(obj, attr):
    if attr == 'form' and hasattr(obj, attr):
        return obj.form.url


plugins_map = {
    'new Ext3.ux.grid.MultiSorting()': {'ptype': 'multisorting'},
    'new Ext3.ux.grid.GridHeaderFilters()': {'ptype': 'headerfilters'},
    'new Ext3.ux.grid.MultiGroupingSummary()': {'ptype': 'multigroupsummary'},
}


def getter_plugins(obj, attr):
    if attr == 'plugins' and hasattr(obj, attr):
        # преобразуем известные плагины
        res = []
        for pl in obj.plugins:
            res.append(plugins_map.get(pl, pl))
        return res


def getter_renderer(obj, attr):
    if attr == '_column_renderer' and hasattr(obj, attr):
        return obj.render_column_renderer()


def getter_style(obj, attr):
    if attr == 'style' and hasattr(obj, attr):
        result = obj.style
        if 'overflow' not in result:
            # делается для хака IE иначе иногда дочерние элементы ведут себя
            # словно у них задано position: fixed т.е. начинаю неадекватничать
            result['overflow'] = 'hidden'
        return result


def getter_listeners(obj, attr):
    if attr == '_listeners' and hasattr(obj, attr):
        result = obj._listeners
        # значит это ListenerStorage
        if hasattr(result, '_data'):
            result = {k: v for k, v in result._data.items() if v}
        return result


def getter_baseparams(obj, attr):
    if attr == '_base_params' and hasattr(obj, attr):
        if obj.base_params:
            result = obj.base_params
        else:
            result = {}
        # а еще добавим контекст
        if hasattr(obj, 'action_context') and obj.action_context:
            context_dict = dict(
                kv for kv in obj.action_context.__dict__.items()
                if not kv[0].startswith('_') and kv[0] != 'profile'
            )
            result.update(context_dict)
        return result


def getter_items(obj, attr):
    if attr == 'items' and hasattr(obj, attr):
        # выставляем action_context у дочерних элементов
        for item in obj.items:
            if item:
                # объединим личный и общий контексты. личный важнее!
                # поэтому его накатим его первым
                # если у объекта небыло контекста, то будет!
                item.action_context = ActionContext().combine(
                    getattr(item, 'action_context', None)
                ).combine(
                    getattr(obj, 'action_context', None)
                )
        return obj.items


def __hackingsetattr__(self, attr, value):
    # игнорируем присвоение в поле фокусировки
    if attr == 'focused_field':
        super(BaseExtComponent, self).__setattr__(attr, value)
        return
    # если выставляем item_id в первый раз, то запомним его
    if attr == 'item_id' and not hasattr(self, '_original_item_id'):
        self._original_item_id = value
    # компонентам проставляется itemId
    if isinstance(value, BaseExtComponent):
        if not hasattr(value, '_original_item_id'):
            value._original_item_id = None
        value.item_id = attr
    super(BaseExtComponent, self).__setattr__(attr, value)


BaseExtComponent.__setattr__ = __hackingsetattr__


reg_js_mapping(BaseExtComponent, {
    # атрибут конфига: атрибут объекта
    'xtype': None,
    #'plugins': getter('plugins'),
    'itemId': getter('item_id'),
    'listeners': getter('_listeners', pregetter=getter_listeners),
})

reg_js_mapping(ExtUIComponent, {
    'xtype': 'component',
    'style': getter('style'),
    'hidden': getter('hidden'),
    'height': getter('height'),
    'width': getter('width'),
    'x': getter('x'),
    'y': getter('y'),
    'html': getter('html'),
    'region': getter('region'),
    'flex': getter('flex'),
    'name': getter('name'),
    'cls': getter('cls'),
    'maxHeight': getter('max_height'),
    'minHeight': getter('min_height'),
    'maxWidth': getter('max_width'),
    'minWidth': getter('min_width'),
    'autoScroll': getter('auto_scroll'),
    'autoHeight': getter('auto_height'),
    'autoWidth': getter('auto_width'),
    'fieldLabel': getter('label', suppress_if=
        lambda x: True if x is None else False),
    'labelStyle': getter('label_style'),
    'hideLabel': getter('hide_label'),
    'anchor': getter('anchor'),
})

reg_js_mapping(BaseExtContainer, {
    'xtype': 'container',
    'items': getter('items', pregetter=getter_items),
    'split': getter('split'),
    'layout': getter('layout'),
    'baseCls': getter('base_cls'),
    'layoutConfig': getter('layout_config'),
    'labelWidth': getter('label_width'),
    'labelAlign': getter('label_align'),
    'labelPad': getter('label_pad'),
    'collapseMode': getter('collapse_mode'),
    'collapsed': getter('collapsed'),
    'collapsible': getter('collapsible'),
})

reg_js_mapping(ExtContainer, {
    'style': getter('style', pregetter=getter_style)
})

reg_js_mapping(BaseExtPanel, {
    'title': getter('title'),
    'padding': getter('padding'),
    'border': getter('border', suppress_if=1),
    'header': getter('header'),
    'tbar': getter('top_bar'),
    'bbar': getter('bottom_bar'),
    'fbar': getter('footer_bar'),
    'buttonAlign': getter('button_align'),
    'bodyStyle': getter('body_style'),
})


reg_js_mapping(ExtToolBar, {
    'xtype': 'toolbar',
})

reg_js_mapping(ExtToolbarMenu, {
    'xtype': None,
    'menu': getter('menu'),
    'text': getter('text'),
    'iconCls': getter('icon_cls'),
    'tooltip': getter('tooltip_text'),
})

reg_js_mapping(ExtToolBar.Fill, {
    'xtype': 'tbfill',
})

reg_js_mapping(ExtToolBar.Separator, {
    'xtype': 'tbseparator',
})

reg_js_mapping(BaseExtWindow, {
    'xtype': 'm3-window',
    'iconCls': getter('icon_cls'),
    'title': getter('title', pregetter=getter_window_title),
    'items': getter('items', pregetter=getter_items),
    'tbar': getter('top_bar'),
    'bbar': getter('bottom_bar'),
    'fbar': getter('footer_bar'),
    'modal': getter('modal'),
    'height': getter('height'),
    'width': getter('width'),
    'maximizable': getter('maximizable'),
    'maximized': getter('maximized'),
    'minimizable': getter('minimizable'),
    'minimized': getter('minimized'),
    'closable': getter('closable'),
    'resizable': getter('resizable'),
    'draggable': getter('draggable'),
    'keys': getter('keys', []),
    'buttons': getter('buttons'),
    'helpTopic': getter('help_topic'),
    'buttonAlign': getter('button_align'),
    'bodyStyle': getter('body_style'),
    'padding': getter('padding'),
    'split': getter('split'),
    'layout': getter('layout'),
    'baseCls': getter('base_cls'),
    'layoutConfig': getter('layout_config'),
    'labelWidth': getter('label_width'),
    'labelAlign': getter('label_align'),
    'labelPad': getter('label_pad'),
    'collapseMode': getter('collapse_mode'),
    'collapsed': getter('collapsed'),
    'collapsible': getter('collapsible'),
    'params.contextJson': getter('action_context'),
})

reg_js_mapping(ExtWindow, {
    'xtype': 'm3-window',
    'iconCls': getter('icon_cls'),
    'title': getter('title', pregetter=getter_window_title),
    'tbar': getter('top_bar'),
    'bbar': getter('bottom_bar'),
    'fbar': getter('footer_bar'),
    'modal': getter('modal'),
    'height': getter('height'),
    'width': getter('width'),
    'maximizable': getter('maximizable'),
    'maximized': getter('maximized'),
    'minimizable': getter('minimizable'),
    'minimized': getter('minimized'),
    'closable': getter('closable'),
    'resizable': getter('resizable'),
    'draggable': getter('draggable'),
    'keys': getter('keys', []),
    'buttons': getter('buttons'),
    'helpTopic': getter('help_topic'),
    'buttonAlign': getter('button_align'),
    'bodyStyle': getter('body_style'),
    'padding': getter('padding'),
    'split': getter('split'),
    'layout': getter('layout'),
    'baseCls': getter('base_cls'),
    'layoutConfig': getter('layout_config'),
    'labelWidth': getter('label_width'),
    'labelAlign': getter('label_align'),
    'labelPad': getter('label_pad'),
    'collapseMode': getter('collapse_mode'),
    'collapsed': getter('collapsed'),
    'collapsible': getter('collapsible'),
})

reg_js_mapping(ExtButton, {
    'xtype': 'm3-button',
    'text': getter('text'),
    'icon': getter('icon'),
    'menu': getter('menu'),
    'margins': getter('margins'),
    'disabled': getter('disabled'),
    'handler': getter('handler'),
    'iconCls': getter('icon_cls'),
    'tooltip': getter('tooltip_text'),
    'enableToggle': getter('enable_toggle'),
    'toggleGroup': getter('toggle_group'),
    'allowDepress': getter('allow_depress'),
    'tabIndex': getter('tab_index'),
})

reg_js_mapping(ExtForm, {
    'xtype': 'form',
    'url': getter('url'),
    'fileUpload': getter('file_upload'),
    'baseCls': getter('base_cls', 'x-plain'),
    'padding': getter('padding'),
})

reg_js_mapping(ExtPanel, {
    'xtype': 'panel',
    'floatable': getter('floatable'),
    'bodyBorder': getter('body_border'),
    'bodyCssClass': getter('body_cls'),
    'baseCls': getter('base_cls'),
    'autoLoad': getter('auto_load'),
    'autoScroll': getter('auto_scroll'),
    'titleCollapse': getter('title_collapse'),
})

reg_js_mapping(ExtTitlePanel, {
    'xtype': 'm3-title-panel',
    'titleItems': getter('title_items'),
})

reg_js_mapping(ExtTabPanel, {
    'xtype': 'tabpanel',
    'plain': getter('plain'),
    'activeTab': getter('active_tab', suppress_if=-1),
    'enableTabScroll': getter('enable_tab_scroll'),
    'bodyBorder': getter('body_border'),
    'deferredRender': getter('deferred_render', suppress_if=True),
    'autoWidth': getter('auto_width'),
    'tabPosition': getter('tab_position'),
    'tabs': getter('tabs'),
})

reg_js_mapping(ExtFieldSet, {
    'xtype': 'fieldset',
    'checkboxToggle': getter('checkbox_toggle'),
    'checkboxName': getter('checkbox_name'),
})

reg_js_mapping(BaseExtField, {
    'xtype': 'field',
    'value': getter('value', suppress_if=suppress_if_None),
    'vtype': getter('vtype'),
    'regex': getter('regex'),
    #'plugins': getter('plugins'),
    'tooltip': getter('tooltip'),
    'filterName': getter('filterName'),
    'readOnly': getter('read_only'),
    'allowBlank': getter('allow_blank', suppress_if=True),
    'isEdit': getter('is_edit'),
    'emptyText': getter('empty_text'),
    'minLength': getter('min_length'),
    'maxLength': getter('max_length'),
    'minLengthText': getter('min_length_text'),
    'maxLengthText': getter('max_length_text'),
    'regexText': getter('regex_text'),
    'tabIndex': getter('tab_index'),
    'invalidClass': getter('invalid_class'),
    'invalidText': getter('invalid_text'),
    'autoCreate': getter('auto_create'),
})


reg_js_mapping(BaseExtTriggerField, {
    'xtype': 'field',
    'store': getter('store'),
    'editable': getter('editable'),
    'mode': getter('mode'),
    'resizable': getter('resizable'),
    'displayField': getter('display_field'),
    'valueField': getter('value_field'),
    'hiddenName': getter('hidden_name'),
    'name': getter('hidden_name'),
    'hideTrigger': getter('hide_trigger'),
    'typeAhead': getter('type_ahead'),
    'queryParam': getter('query_param'),
    'pageSize': getter('page_size'),
    'maxHeight': getter('max_heigth_dropdown_list'),
    'minChars': getter('min_chars'),
    'triggerAction': getter('trigger_action'),
    'forceSelection': getter('force_selection'),
    'valueNotFoundText': getter('not_found_text'),
    'loadingText': getter('loading_text'),
    'listWidth': getter('list_width'),
    'tpl': getter('list_tpl'),
    'fields': getter('fields'),
})


reg_js_mapping(ExtStringField, {
    'xtype': 'textfield',
    'enableKeyEvents': getter('enable_key_events'),
    'inputType': getter('input_type'),
    'maskRe': getter('mask_re'),
    'selectOnFocus': getter('select_on_focus'),
    'inputMask': getter('input_mask'),
})

reg_js_mapping(ExtDateField, {
    'xtype': 'm3-datefield',
    'format': getter('format'),
    'editable': getter('editable'),
    'startDay': getter('start_day'),
    'params.hideTriggerToday': getter('hide_today_btn'),
    'enableKeyEvents': getter('enable_key_events'),
    'maxValue': getter('max_value'),
    'minValue': getter('min_value'),
    'autoCreate': None,
})


reg_js_mapping(ExtNumberField, {
    'xtype': 'numberfield',
    'decimalSeparator': getter('decimal_separator'),
    'allowDecimals': getter('allow_decimals'),
    'allowNegative': getter('allow_negative'),
    'decimalPrecision': getter('decimal_precision'),
    'maxText': getter('max_text'),
    'minText': getter('min_text'),
    'selectOnFocus': getter('select_on_focus'),
    'enableKeyEvents': getter('enable_key_events'),
    'maxValue': getter('max_value'),
    'minValue': getter('min_value'),
})


reg_js_mapping(ExtHiddenField, {
    'xtype': 'hidden',
})


reg_js_mapping(ExtTextArea, {
    'xtype': 'textarea',
    'maskRe': getter('mask_re'),
    'autoCreate': getter('auto_create'),
})

reg_js_mapping(ExtCheckBox, {
    'xtype': 'checkbox',
    'checked': getter('checked'),
    'boxLabel': getter('box_label'),
})


reg_js_mapping(ExtRadio, {
    'xtype': 'radio',
    'checked': getter('checked'),
    'boxLabel': getter('box_label'),
})


reg_js_mapping(ExtComboBox, {
    'xtype': 'combo',
})


reg_js_mapping(ExtTimeField, {
    'xtype': 'timefield',
    'format': getter('format'),
    'increment': getter('increment'),
    'maxValue': getter('max_value'),
    'minValue': getter('min_value'),
})


reg_js_mapping(ExtDisplayField, {
    'xtype': 'displayfield',
})


reg_js_mapping(ExtDateTimeField, {
    #'xtype': 'datetimefield',
    'xtype': 'm3-datefield',
})


reg_js_mapping(ExtAdvTimeField, {
    'xtype': 'm3-timefield',
})

reg_js_mapping(ExtDictSelectField, {
    'xtype': 'm3-selectfield',
    'params.hideClearTrigger': getter('hide_clear_trigger'),
    'params.hideEditTrigger': getter('hide_edit_trigger'),
    'params.hideDictSelectTrigger': getter('hide_dict_select_trigger'),
    'minChars': getter('min_chars'),
    'params.askBeforeDeleting': getter('ask_before_deleting'),
    'params.defaultText': getter('default_text'),
    'params.defaultValue': getter('value'),
    'params.defaultRecord': getter('record_value'),
    'params.actions.actionSelectUrl': getter('url'),
    'params.actions.actionEditUrl': getter('edit_url'),
    'autocompleteUrl': getter('autocomplete_url'),
    'store': getter('store'),
    'queryParam': getter('query_param'),
    'valueField': getter('value_field'),
    'displayField': getter('display_field'),
    'params.actions.contextJson': getter('action_context'),
})

reg_js_mapping(ExtSearchField, {
    'xtype': 'm3-search-field',
    'componentItemId': getter('component_item_id'),
    'query_param': getter('query_param'),
    'emptyText': getter('empty_text'),
})

reg_js_mapping(ExtFileUploadField, {
    'xtype': 'file_url',
    'fileUrl': getter('empty_text'),
    'possibleFileExtensions': getter('possible_file_extensions'),
    'prefixUploadField': getter('prefix'),
    'readOnlyButton': getter('read_only'),
})

reg_js_mapping(ExtImageUploadField, {
    'xtype': 'imageuploadfield',
    'thumbnail': getter('thumbnail'),
    'thumbnailSize': getter('thumbnail_size'),
    'prefixThumbnailImg': getter('prefix'),
    'possibleFileExtensions': getter('possible_file_extensions'),
})

reg_js_mapping(ExtMultiSelectField, {
    'xtype': 'm3-multiselect',
    'delimeter': getter('delimeter'),
    'multipleDisplayValue': getter('multiple_display_value'),
    # 'value': getter('value'),
})

reg_js_mapping(ExtEditWindow, {
    'xtype': 'm3-editwindow',
    'formItemId': getter('form', pregetter=getter_form),
    'formUrl': getter('form', pregetter=getter_form_url),
    'dataUrl': getter('data_url'),
})


reg_js_mapping(ExtGrid, {
    'xtype': 'm3-grid',
    'columns': getter('columns'),
    'stateful': getter('stateful'),
    'store': getter('store'),
    'params': getter('params'),
    'sm': getter('sm'),
    'view': getter('view'),
    # 'cm': getter('col_model'),
    'params.plugins': getter('plugins', pregetter=getter_plugins),
    'viewConfig': getter('view_config'),
    'stripeRows': getter('stripe_rows'),
    'columnLines': getter('column_lines'),
    'loadMask': getter('load_mask'),
    'autoExpandColumn': getter('auto_expand_column'),
    'enableDragDrop': getter('drag_drop'),
    'ddGroup': getter('drag_drop_group'),
    'params.contextMenu': getter('handler_contextmenu'),
    'params.rowContextMenu': getter('handler_rowcontextmenu'),
    'params.bandedColumns': getter('banded_columns'),
    'viewConfig.forceFit': getter('force_fit'),
    'viewConfig.showPreview': getter('show_preview'),
    'viewConfig.enableRowBody': getter('enable_row_body'),
    'viewConfig.headerStyle': getter('header_style'),
})

reg_js_mapping(BaseExtGridColumn, {
    'xtype': 'gridcolumn',
    'header': getter('header'),
    'align': getter('align'),
    'width': getter('width'),
    'sortable': getter('sortable'),
    'format': getter('format'),
    'hidden': getter('hidden'),
    'editor': getter('editor'),
    'tooltip': getter('tooltip'),
    'filter': getter('filter'),
    'fixed': getter('fixed'),
    'locked': getter('locked'),
    'colspan': getter('colspan'),
    'hideable': getter('hideable'),
    'groupable': getter('groupable'),
    'css': getter('css'),
    'renderer': getter('_column_renderer', pregetter=getter_renderer),
    'dataIndex': getter('data_index'),
    'menuDisabled': getter('menu_disabled'),
    'summaryType': getter('summary_type'),
    'nameField': getter('name_field'),
})

reg_js_mapping(ExtGridBooleanColumn, {
    'xtype': 'booleancolumn',
    'falseText': getter('text_false'),
    'trueText': getter('text_true'),
    'undefinedText': getter('text_undefined'),
})

reg_js_mapping(ExtGridCheckColumn, {
    'xtype': 'checkcolumn',
})

reg_js_mapping(ExtGridNumberColumn, {
    'xtype': 'numbercolumn',
})

reg_js_mapping(ExtGridDateColumn, {
    'xtype': 'datecolumn',
})

reg_js_mapping(BaseExtStore, {
    'xtype': 'store',
    'url': getter('url'),
    'writer': getter('writer'),
    'root': getter('root'),
    'fields': getter('fields'),
    'autoLoad': getter('auto_load'),
    'autoSave': getter('auto_save'),
    'baseParams': getter('_base_params', pregetter=getter_baseparams),
    'idProperty': getter('id_property'),
    'totalProperty': getter('total_property'),
    'reader': getter('reader'),
})

reg_js_mapping(ExtDataStore, {
    'xtype': 'arraystore',
    'data': getter('data'),
})

reg_js_mapping(ExtJsonStore, {
    'xtype': 'jsonstore',
    'baseParams.start': getter('start'),
    'baseParams.limit': getter('limit'),
    'remoteSort': getter('remote_sort'),
})

reg_js_mapping(ExtContextMenu, {
    'xtype': 'menu',
    'items': getter('items'),
})

reg_js_mapping(ExtContextMenuItem, {
    'xtype': 'm3-menuitem',
    'menu': getter('menu'),
    'text': getter('text'),
    'disabled': getter('disabled'),
    'handler': getter('handler'),
    'iconCls': getter('icon_cls'),
})

reg_js_mapping(ExtContextMenuSeparator, {
    'xtype': 'menuseparator',
})

reg_js_mapping(ExtMultiGroupinGrid, {
    'xtype': 'm3-grouppinggrid',
    'params.groupable': getter('groupable'),
    'params.rowIdName': getter('row_id_name'),
    'params.localEdit': getter('local_edit'),
    'params.actions.newUrl': getter('url_new'),
    'params.actions.editUrl': getter('url_edit'),
    'params.actions.deleteUrl': getter('url_delete'),
    'params.actions.dataUrl': getter('url_data'),
    'params.actions.exportUrl': getter('url_export'),
    'params.actions.contextJson': getter('action_context'),
    'viewConfig.bufferSize': getter('buffer_size'),
    'viewConfig.nearLimit': getter('near_limit'),
    'params.dataIdField': getter('data_id_field'),
    'params.dataDisplayField': getter('data_display_field'),
    'params.displayInfo': getter('display_info'),
    'params.displayMsg': getter('display_message'),
    'params.groupedColumns': getter('grouped'),
    'params.toolbar': getter('_top_bar.items'),
    'tbar': None,
})

reg_js_mapping(ExtMultiGroupingStore, {
    'xtype': 'm3-live-store',
    'bufferSize': getter('bufferSize'),
    'version': getter('version_property'),
    'baseParams.start': None,
    'baseParams.limit': None,
})

reg_js_mapping(ExtLabel, {
    'xtype': 'label',
    'text': getter('text'),
    'icon': getter('icon'),
    'margins': getter('margins'),
    'disabled': getter('disabled'),
})

reg_js_mapping(ExtContainerTable, {
    'xtype': 'container',
    'items': getter('_items'),
})