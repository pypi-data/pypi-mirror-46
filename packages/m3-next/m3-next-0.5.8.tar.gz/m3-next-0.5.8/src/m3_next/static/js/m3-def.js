// сохраним старый конструктор, чтобы вызывать в оверрайде
var oldM3WindowConstructor = Ext.m3.Window.prototype.constructor;

Ext.define('Ext.m3.Window', {
    override: 'Ext.m3.Window',
    xtype: 'm3-window',
    // сюда можно добавлять функции и контекст, который будет доступен для
    // "старых" обработчиков
    handlerContext: {},

    constructor: function (baseConfig, params) {
        // Поиск хендлера для кнопок и других компонент
        this.listeners['gethandler'] = this.findHandler;
        // отложенные обработчики - это те, которые не нашлись при первом
        // вызове события gethandler, но после инициализации окна сделаем
        // еще один поиск и сами вызовем установку хэндлера
        this.delayHandlers = [];
        params = params || baseConfig.params || {};
        params.contextJson = params.contextJson || {};

        // добавим в хэндлер win - по-старинке
        this.handlerContext.win = this;

        oldM3WindowConstructor.call(this, baseConfig, params);

        this.addEvents(
            /**
             * Событие назначения маски на окно, всплывает из дочерних компонент
             * Параметры:
             *  this - ссылка на окно
             *  cmp - ссылка на компонент, который послал событие
             *  maskText - текст, который должен отобразиться при маскировании
             *  win - ссылка на дочернее окно
             */
            'mask',

            /**
             * Событие снятия маски с окна, всплывает из дочерних компонент
             * Параметры:
             *  this - ссылка на окно
             *  cmp - ссылка на компонент, который послал событие
             *  win - ссылка на дочернее окно
             */
            'unmask',

            /**
             * Событие, которое всплывает от компонентов внутри вызова функции getContext()
             * и возвращает вызов связанной функции, подписка происходит внутри fabric.js
             */
            'gethandler'
        );

        var loadMask = new Ext.LoadMask(this.getEl(), {msg: 'Загрузка...'}),
            loadMaskCount = 0;
        this.on('mask', function (cmp, maskText, win) {
            loadMask.msgOrig = loadMask.msg;
            loadMask.msgClsOrig = loadMask.msgCls;
            if (maskText){
                loadMask.msg = maskText;
                loadMask.msgCls = 'x-mask';
            }
            if (loadMaskCount === 0) {
                loadMask.show();
            }
            loadMaskCount++;

            if (win instanceof Ext.m3.Window) {
                this.on('activate', win.activate, win);
            }

        }, this);

        this.on('unmask', function (cmp, win) {
            loadMaskCount--;
            if (loadMaskCount <= 0) {
                loadMask.hide();
                if (win instanceof Ext.m3.Window) {
                    this.un('activate', win.activate, win);
                }
            }
            loadMask.msg = loadMask.msgOrig;
            loadMask.msgCls = loadMask.msgClsOrig;
        }, this);
        this.init();
        // повторно разошлем сообщения об отложенных обработчиках
        Ext.each(this.delayHandlers, function(item){
            this.findHandler(item.cmp, item.handlerStr, item.callback, true);
        }, this);
    },

    init: function() {
        // отложенная инициализация. после создания всех плагинов
    },

    findHandler: function (cmp, handlerStr, callback, notDelay) {
        var handlerFunct,
            handler = handlerStr.trim();
        if (Ext.isFunction(this[handler])) {
            handlerFunct = this[handler].createDelegate(this);
        } else {
            try {
                // для "старых" обработчиков теперь можно оставлять хэндлеры
                // вида "function(){createNewDocumentClick(111)}" но
                // потребуется добавить эту функцию в handlerContext этого
                // окна. это можно сделать в конструкторе класса
                handlerFunct = new Function("context",
                    "with (context) { return " + handler+" }").bind(
                        this, this.handlerContext)();
            } catch (e) {
                // на первый раз запишем в отложенные хэндлеры
                if (!notDelay) {
                    this.delayHandlers.push({
                        cmp: cmp,
                        handlerStr: handlerStr,
                        callback: callback
                    });
                } else {
                    console.log(handler);
                    console.log(e);
                    Ext.Msg.show({
                        title: 'Внимание! Произошла непредвиденная ошибка!'
                        , msg: e.message
                        , buttons: Ext.Msg.OK
                        , fn: Ext.emptyFn
                        , animEl: 'elId'
                        , icon: Ext.MessageBox.ERROR
                    });
                }
                //throw e;
            }
        }
        if (handlerFunct) {
            if (callback) {
                callback(handlerFunct);
            } else {
                cmp.handler = handlerFunct;
            }
            return false;
        }
    },

    /**
     * Поиск элемента по itemId
     * @param itemId - что нужно искать
     * @returns {*} Нашедшийся элемент
     */
    findByItemId: function(itemId){
        var containers = [
            this,
            this.getTopToolbar(),
            this.getBottomToolbar(),
            this.getFooterToolbar()
        ];
        var result;
        Ext.each(containers, function(cont) {
            if (cont) {
                var res = cont.find('itemId', itemId)[0];
                if (res) {
                    result = res;
                    return false;
                }
            }
        }, this);
        return result;
    },

    bind: Ext.emptyFn,

    /**
     * Блокировка окна от изменений. Вызывает каскадно setBlocked
     * @param blocked - признак блокировки bool
     * @param exclude - список itemId элементов исключаемых из блокирования
     */
    setBlocked: function(blocked, exclude) {
        var me = this,
            containers = [
                this,
                this.getTopToolbar(),
                this.getBottomToolbar(),
                this.getFooterToolbar()
            ];
        Ext.each(containers, function(cont) {
            if (cont) {
                cont.cascade(function (item) {
                    if (me != item) {
                        item.setBlocked(blocked, exclude || []);
                    }
                });
            }
        });
    },

    /**
     * Выводит окно на передний план
     */
    activate: function () {
        this.toFront();
    },
});


/**
 * Окно на базе Ext.m3.Window, которое включает такие вещи, как:
 * 1) Submit формы, если она есть;
 * 2) Навешивание функции на изменение поля, в связи с чем обновляется заголовок
 * окна;
 * 3) Если поля формы были изменены, то по-умолчанию задается вопрос "Вы
 * действительно хотите отказаться от внесенных измений";
 */
// сохраним старый инициализатор, чтобы вызывать в оверрайде
var oldM3EditWindowInitComponent = Ext.m3.EditWindow.prototype.initComponent;

Ext.define('Ext.m3.EditWindow', {
    override: 'Ext.m3.EditWindow',

    initComponent: function () {
        oldM3EditWindowInitComponent.call(this);
        // найдем форму по formItemId
        if (this.formItemId) {
            var form = this.findByItemId(this.formItemId);
            if (form) {
                this.formId = form.id;
            }
        }
        if (this.formId) {
            this.form = this.getForm();
        }
    },

    /**
     * Функция превращения вложенных объектов в плоские атрибуты
     * Было:
     * {
     *   name: 'asdasd',
     *   subobject: {
     *     id: 12,
     *     name: 'sdfsdfe'
     *   }
     * }
     * Станет:
     * {
     *   name: 'asdasd',
     *   subobject.id: 12,
     *   subobject.name: 'sdfsdfe'
     * }
     * @param values исходный объект
     */
    plainValues: function (values) {
        var plainValues = {};
        var form = this.getForm();

        function plain(values, prefix) {
            var field, id, value;
            if (prefix != '') {
                prefix = prefix + '.';
            }
            for (id in values) {
                if (!Ext.isFunction(values[id])) {
                    value = values[id];
                    if (Ext.isObject(value)) {
                        // если уже есть поле на форме с таким именем
                        // то не надо дальше раскладывать
                        if (form.findField(prefix + id)) {
                            plainValues[prefix + id] = value;
                        } else {
                            plain(value, prefix + id);
                        }
                    } else {
                        plainValues[prefix+id] = value;
                    }
                }
            }
        }
        plain(values, '');
        return plainValues;
    },

    bind: function (data) {
        this.getForm().setValues(this.plainValues(data.model));
    }
});

Ext.reg('m3-window', Ext.m3.Window);
Ext.reg('m3-editwindow', Ext.m3.EditWindow);

Ext.reg('sm-cell', Ext.grid.CellSelectionModel);
Ext.reg('sm-checkbox', Ext.grid.CheckboxSelectionModel);
Ext.reg('sm-row', Ext.grid.RowSelectionModel);

Ext.reg('view-grouping', Ext.grid.GroupingView);

Ext.reg('gridcolumn', Ext.grid.Column);

Ext.define('Ext.m3.MultigrouppingGrid', {
    extend: 'Ext.m3.MultiGroupingGridPanel',
    xtype: 'm3-grouppinggrid',
    bubbleEvents: [
        'gethandler',
        'mask',
        'unmask',
        'getcontext'
    ],
    constructor: function (cfg) {
        var params = cfg.params || {};
        if (params.menus == undefined) {
            params.menus = {
                contextMenu: params.contextMenu,
                rowContextMenu: params.rowContextMenu,
            };
        }
        // запомним колонки и рендереры
        var renderers = {};
        if (cfg.columns) {
            //var needFilterPlugin = false;
            Ext.each(cfg.columns, function (col) {
                if (typeof col.renderer === 'string') {
                    renderers[col.dataIndex] = col.renderer;
                }
            });
        }

        Ext.m3.MultigrouppingGrid.superclass.constructor.call(this, cfg, params);
        // собственный обработчик назначения handler для грида
        this.addEvents(
             'gethandler'
        );
        this.on('gethandler', this.findHandler);
        // укажем владельцем грид, чтобы события поднимались выше
        if (this.topToolbar) {
            this.topToolbar.ownerCt = this;
            // для кнопок на тулбаре надо сделать назначение обработчиков,
            // т.к. они сами не назначатся при создании
            if (this.topToolbar.items)
                this.topToolbar.items.each(this.setButtonHandler, this);
        }
        // Теперь назначим рендереры колонкам
        var gridColumns = this.colModel;
        if (gridColumns) {
            Ext.each(gridColumns.config, function (col) {
                var colRenderer = renderers[col.dataIndex];
                if (typeof colRenderer === 'string') {
                    this.fireEvent('gethandler', col, colRenderer,
                        function (newHandler) {
                            if (newHandler) {
                                gridColumns.setRenderer(col.id, newHandler);
                            }
                        }.bind(col));
                }
            }, this);
        }
    },

    findHandler: function (cmp, handler, callback) {
        var handlerFunct;
        if (Ext.isFunction(this[handler])) {
            handlerFunct = this[handler].createDelegate(this);
        }
        if (handlerFunct) {
            if (callback) {
                callback(handlerFunct);
            } else {
                cmp.handler = handlerFunct;
            }
            return false;
        }
    },

    setButtonHandler: function(button) {
        if (!button) return;
        if (typeof button.handler === 'string') {
            this.fireEvent('gethandler', button, button.handler,
                function (newHandler) {
                    if (newHandler) {
                        button.setHandler(newHandler, button);
                    }
                }.bind(button)
            );
        }
        if (button.menu) {
            if (button.menu.items.each) {
                button.menu.items.each(this.setButtonHandler, this);
            } else {
                Ext.each(button.menu.items, this.setButtonHandler, this);
            }
        }
        // обработаем listeners и заменим текст на функции
        if (button.initialConfig.listeners) {
            for (var key in button.initialConfig.listeners) {
                if (button.initialConfig.listeners.hasOwnProperty(key)) {
                    var oldhandler = button.initialConfig.listeners[key];
                    if(typeof oldhandler === 'string') {
                        this.fireEvent('gethandler', button, oldhandler,
                            function (newHandler) {
                                if (newHandler) {
                                    button.removeListener(key, oldhandler, button);
                                    button.addListener(key, newHandler, button);
                                }
                            }.bind(this)
                        );
                    }
                }
            }
        }
        if (button.menu) {
            this.setButtonHandler(button.menu);
        }
    },

    topBarNew: function(){
        this.onNewRecord();
    },
    topBarEdit: function (){
        this.onEditRecord();
    },
    topBarDelete: function (){
        this.onDeleteRecord();
    },

    /**
     * Переписанный вариант, чтобы использовался новый подход
	 * Нажатие на кнопку "Новый"
	 */
	onNewRecord: function (){
		assert(this.actionNewUrl, 'actionNewUrl is not define');
        var baseConf = this.getMainContext();

        // Если контекст замусорен и уже содержит чей-то id, то вместо создания элемента
        // может открыться редактирование, поэтому удаляем его от греха подальше.
        delete baseConf[this.rowIdName];

		var req = {
			url: this.actionNewUrl,
			params: baseConf,
			success: this.newRecord.createDelegate(this),
            failure: uiAjaxFailMessage
		};

		if (this.fireEvent('beforenewrequest', this, req)) {
            UI.callAction(req, this);
		}
	},

    /**
     * Переписанный вариант, чтобы использовался новый подход
	 * Нажатие на кнопку "Редактировать"
	 */
	onEditRecord: function (){
		assert(this.actionEditUrl, 'actionEditUrl is not define');
		assert(this.rowIdName, 'rowIdName is not define');
		// выходим, если кнопка редактирования заблокирована
        // т.к. этот же обработчик висит на двойном клике
        if (this.getTopToolbar().getComponent("button_edit").disabled) {
            return;
        }

	    if (this.getSelectionModel().hasSelection()) {
			var baseConf = this.getSelectionContext(this.localEdit);
			var mask = new Ext.LoadMask(this.body);
                        var disableState = this.getToolbarsState();
			var req = {
				url: this.actionEditUrl,
				params: baseConf,
				success: this.editRecord.createDelegate(this),
                failure: uiAjaxFailMessage,
			};

			if (this.fireEvent('beforeeditrequest', this, req)) {
                UI.callAction(req, this);
			}
    	} else {
            Ext.Msg.show({
                title: 'Редактирование',
                msg: 'Элемент не выбран',
                buttons: Ext.Msg.OK,
                icon: Ext.MessageBox.INFO
            });
        }
	},
    /**
     * Показ и подписка на сообщения в дочерних окнах
     * @param {Object} win Окно
     */
    newRecord: function (win) {
        if (this.fireEvent('afternewrequest', this, win) && win instanceof Ext.Component) {
            win.on('closed_ok', function (data) {
                if (this.fireEvent('rowadded', this, data)) {
                    // если локальное редактирование
                    if (this.localEdit) {
                        // то на самом деле нам пришла строка грида
                        var obj = Ext.decode(data),
                            record = new Ext.data.Record(obj.data),
                            store = this.getStore(),
                            sm = this.getSelectionModel();

                        record.json = obj.data;

                        store.add(record);
                        sm.selectRecords([record]);
                    } else {
                        this.refreshStore();
                    }
                }
            }, this);
        }
        return win;
    },
	editRecord: function (win) {
        if (this.fireEvent('aftereditrequest', this, win) && win instanceof Ext.Component) {
            win.on('closed_ok', function (data) {
                if (this.fireEvent('rowedited', this, data)) {
                    // если локальное редактирование
                    if (this.localEdit) {
                        // то на самом деле нам пришла строка грида
                        var obj = Ext.decode(data),
                            record = new Ext.data.Record(obj.data),
                            store = this.getStore(),
                            sm = this.getSelectionModel();

                        record.json = obj.data;
                        if (sm.hasSelection()) {
                            // пока только для режима выделения строк
                            if (sm instanceof Ext.grid.RowSelectionModel) {
                                var rec = sm.getSelected(),
                                    index = store.indexOf(rec);

                                store.remove(rec);
                                if (index < 0) {
                                    index = 0;
                                }
                                store.insert(index, record);
                                sm.selectRow(index);
                            }
                        }
                    } else {
                        this.refreshStore();
                    }
                }
            }, this);
        }
        return win;
    },
    /**
     * Хендлер на удаление записи
     * @param {Object} res json-ответ
     */
    deleteRecord: function (res) {
        if (this.fireEvent('rowdeleted', this, res)) {
            // если локальное редактирование
            if (this.localEdit) {
                // проверка на ошибки уровня приложения
                if (!res.success) {
                    return;
                }
                var store = this.getStore(),

                // и надо ее заменить в сторе
                    sm = this.getSelectionModel();

                if (sm.hasSelection()) {
                    // только для режима выделения строк
                    if (sm instanceof Ext.grid.RowSelectionModel) {
                        var rec = sm.getSelections();
                        store.remove(rec);
                    }
                }
            } else {
                this.refreshStore();
            }
        }
    },
    findByItemId: function(itemId){
        var containers = [
            this.topToolbar,
        ];
        var result;
        Ext.each(containers, function(cont) {
            if (cont) {
                var res = cont.find('itemId', itemId)[0];
                if (res) {
                    result = res;
                    return false;
                }
            }
        }, this);
        return result;
    },
});


Ext.define('Ext.m3.Store', {
    extend: 'Ext.m3.LiveStore',
    xtype: 'm3-live-store',

    constructor: function (config) {

        config.reader = new Ext.m3.LiveStoreReader({
            fields: config.fields,
            id: config.idProperty,
            root: config.root,
            totalProperty: config.totalProperty
        });

        this.callParent(arguments);
    }
});

// Ext.define('Ext.m3.LiveStoreReader', {
//     extend: 'Ext.ux.grid.livegrid.JsonReader',
//
//     readRecords: function (o) {
//         var intercept = Ext.m3.LiveStoreReader.superclass.readRecords.call(this, o);
//         // сохраним итоговую строку для дальнейшей обработки
//         if (o) {
//             intercept.totalRow = o.totalRow;
//         }
//         return intercept;
//     }
// });

Ext.reg('sm-live-checkbox', Ext.ux.grid.livegrid.CheckboxSelectionModel);
Ext.reg('sm-live-row', Ext.ux.grid.livegrid.RowSelectionModel);

Ext.preg('multisorting', Ext.ux.grid.MultiSorting);
Ext.preg('headerfilters', Ext3.ux.grid.GridHeaderFilters);
Ext.preg('multigroupsummary', Ext3.ux.grid.MultiGroupingSummary);
Ext.preg('celltooltips', Ext.ux.plugins.grid.CellToolTips);


Ext.define('Ext.m3.SelectField', {
    extend: 'Ext.m3.AdvancedComboBox',
    xtype: 'm3-selectfield',
    constructor: function (cfg) {
        var params = cfg.params || {actions: {}};
        Ext.m3.SelectField.superclass.constructor.call(this, cfg, params);
        // Значения по-умолчанию
        if (params.defaultRecord &&
            // Проверка на пустоту объекта
            Object.getOwnPropertyNames(params.defaultRecord).length !== 0) {
            this.setRecord(new Ext.data.Record(params.defaultRecord));
        } else {
            if (this.defaultValue && this.defaultText) {
                this.addRecordToStore(this.defaultValue, this.defaultText);
            }
        }
    }
});

Ext.define('Ext.m3.DateField', {
    extend: 'Ext.m3.AdvancedDataField',
    xtype: 'm3-datefield',
    constructor: function (cfg) {
        var params = cfg.params || {};
        Ext.m3.DateField.superclass.constructor.call(this, cfg, params);
    }
});


Ext.define('Ext.m3.TimeField', {
    extend: 'Ext.ux.form.AdvTimeField',
    xtype: 'm3-timefield',
    constructor: function (cfg) {
        var params = cfg.params || {};
        Ext.m3.TimeField.superclass.constructor.call(this, cfg, params);
    }
});

Ext.define('Ext.Component', {
    override: 'Ext.Component',
    initComponent: function () {
        this.bubbleEvents.push('gethandler');
        if(this.ptypes){
            // добавим расширений
            if(!this.plugins){
                this.plugins = [];
            }
            this.plugins = this.plugins.concat(this.ptypes);
        }

        if(this.listeners){
            this.on(this.listeners);
            delete this.listeners;
        }
        this.enableBubble(this.bubbleEvents);
        // обработаем listeners и заменим текст на функции
        if (this.initialConfig.listeners) {
            for (var key in this.initialConfig.listeners) {
                if (this.initialConfig.listeners.hasOwnProperty(key)) {
                    var oldhandler = this.initialConfig.listeners[key];
                    if(typeof oldhandler === 'string') {
                        this.fireEvent('gethandler', this, oldhandler,
                            function (newHandler) {
                                if (newHandler) {
                                    this.removeListener(key, oldhandler, this);
                                    this.addListener(key, newHandler, this);
                                }
                            }.bind(this)
                        );
                    }
                }
            }
        }
    }
});

