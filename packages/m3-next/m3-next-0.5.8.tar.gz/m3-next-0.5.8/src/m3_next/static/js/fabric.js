
function isUnique(value, index, self) {
    return self.indexOf(value) === index;
}

function isObject (value) {
    return value && typeof value === 'object' && value.constructor === Object;
}

function isArray (value) {
    return value && typeof value === 'object' && value.constructor === Array;
}

function findAllxtypes(obj) {
    var result = [];
    if (isObject(obj)) {
        if (obj.xtype) {
            result.push(obj.xtype);
        }
        for (var i in obj) {
            if (obj.hasOwnProperty(i)) {
                if (isObject(obj[i])) {
                    var deepxtypes = findAllxtypes(obj[i]);
                    if (deepxtypes) {
                        result = result.concat(deepxtypes);
                    }
                }
                if (isArray(obj[i])) {
                    for (var j in obj[i]) {
                        var deepxtypes = findAllxtypes(obj[i][j]);
                        if (deepxtypes) {
                            result = result.concat(deepxtypes);
                        }
                    }
                }
            }
        }
    }
    return result;
}


function findAllptypes(obj) {
    var result = [];
    if (isObject(obj)) {
        if (obj.ptypes && isArray(obj.ptypes)) {
            result = result.concat(obj.ptypes);
        }
        for (var i in obj) {
            if (obj.hasOwnProperty(i)) {
                if (isObject(obj[i])) {
                    var deepptypes = findAllptypes(obj[i]);
                    if (deepptypes) {
                        result = result.concat(deepptypes);
                    }
                }
                if (isArray(obj[i])) {
                    for (var j in obj[i]) {
                        var deepptypes = findAllptypes(obj[i][j]);
                        if (deepptypes) {
                            result = result.concat(deepptypes);
                        }
                    }
                }
            }
        }
    }
    return result;
}

/**
 * "Класс" для построения UI
 *
 * @param config
 * @constructor
 */
UI = function (config) {
    var desktop = config['desktop'], // Ссылка на рабочий стол, в контексте которого создаются окна
        storage = config['storage'], // хранилище базовых конфигураций окон
        create = config['create'];       // собственно, формирователь UI

    UI.createWindow = function (cfg, data) {
        var win;

        cfg.listeners = cfg.listeners || {};
        cfg.listeners['getcontext'] = function (cmp) {
            cmp._getContext = function () {
                return data.context;
            }
        };

        win = create(cfg);
        if (Ext.isFunction(win.bind)) {
            win.bind(data);
        }
        desktop.getDesktop().createWindow(win).show();
        return win;
    };

    UI.create = function (data) {
        // словарь параметров должен содержать
        var initialData = data['data'], // - словарь данных для инициализации
            key = data['ui'];           // - key, однозначно идентифицирующий окно в хранилище

        // грузим конфиг и данные из хранилища...
        // TODO: для отделения данных от UI
        //return storage(key, initialData['context'])
        return new Q(data)
            .then(function (result) {
                // данные затем патчим инициализирующими данными
                var data = Ext.apply(result.data || {}, initialData || {});
                // контекст должен браться только из изначальногго запроса
                data.context = initialData.context || {};
                return [result.config, data];
            }).spread(function (cfg, data) {
                // Подтягиваем зависимости
                var xtypes = findAllxtypes(cfg).filter(isUnique),
                    ptypes = findAllptypes(cfg).filter(isUnique),
                    needtypes = xtypes.concat(ptypes);
                return UI.require(needtypes)
                    .then(function () {
                        return [cfg, data]
                    });
            }).spread(UI.createWindow)
            .catch(function (err) {
                console.log(key);
                console.log(err);
                if (err.message) {
                    Ext.Msg.show({
                        title: 'Внимание'
                        , msg: err.message
                        , buttons: Ext.Msg.OK
                        , fn: Ext.emptyFn
                        , animEl: 'elId'
                        , icon: Ext.MessageBox.ERROR
                    });
                } else
                    uiAjaxFailMessage(err, {});
            });
    };
};

/**
 * Загружает JSON AJAX-запросом и кладёт в promise
 * @param cfg
 * @returns {promise|Q.promise}
 */
UI.ajax = function (cfg) {
    var result = Q.defer();

    cfg = Ext.applyIf(cfg, {
        method: 'POST',
        //disableCaching: false,
    });

    Ext.Ajax.request(Ext.applyIf({
        success: function () {
            result.resolve.apply(this, arguments);
        },
        failure: function (response) {
            result.reject(response);
        }
    }, cfg));
    return result.promise;
};

/**
 * Загружает JSON AJAX-запросом и кладёт в promise
 * @param form
 * @param cfg
 * @returns {promise|Q.promise}
 */
UI.submit = function (form, cfg) {
    var result = Q.defer(),

        obj = Ext.applyIf({
            success: function () {
                result.resolve.apply(this, arguments);
            },
            failure: function (response) {
                result.reject(response);
            }
        }, cfg);
    form.getForm().submit(obj);
    return result.promise;
};

UI.showMsg = function (obj) {
    if (obj && obj.message) {
        var result = Q.defer();
        Ext.Msg.show({
            title: 'Внимание',
            msg: obj.message,
            buttons: Ext.Msg.OK,
            fn: function () {
                if (obj.success) {
                    result.resolve(obj);
                } else {
                    result.reject(null);
                }
            },
            icon: (!obj.success) ? Ext.Msg.WARNING : Ext.Msg.Info
        });
        return result.promise;
    } else {
        return obj;
    }
};

UI.evalCode = function (text) {
    var result = Q.defer();
    if (text.substring(0,1) === '{' || text.substring(0,1) === '[') {
        return text;
    }
    if (text.substring(0, 1) === '/') {
        // Сервер сформировал файл для загрузки и вернул путь к нему.
        var iframe = document.getElementById('hiddenDownloader');

        if (iframe === null) {
            iframe = document.createElement('iframe');
            iframe.id = 'hiddenDownloader';
            iframe.style.visibility = 'hidden';
            document.body.appendChild(iframe);
        }
        iframe.src = text;
        return text;
    } else {
        try {
            var eval_result = eval(text);
        } catch (e) {
            Ext.Msg.show({
                title: 'Внимание'
                , msg: 'Произошла непредвиденная ошибка!'
                , buttons: Ext.Msg.OK
                , fn: Ext.emptyFn
                , animEl: 'elId'
                , icon: Ext.MessageBox.WARNING
            });
            throw e;
        }
        if (eval_result && eval_result instanceof Ext.Window &&
            typeof AppDesktop != 'undefined' && AppDesktop) {
            AppDesktop.getDesktop().createWindow(eval_result);
        }
        return eval_result;
    }
    return result.promise;
};

/**
 *
 * @param response
 * @returns {*}
 */
UI.evalResult = function (response) {
    return new Q(response.responseText)
        .then(UI.evalCode)
        .then(function (result){
            if (result === Ext.MessageBox){
                return;
            }
            if (typeof result === 'string' && result.substring(0,1) === '/') {
                // url с файлом для скачивания, он был обработан в evalCode
                return result;
            }
            if (!(result instanceof Ext.Component)) {
                // это может быть JSON или наш объект, который только smart_eval
                // поэтому сперва json, а если не получится - то eval
                try {
                    return JSON.parse(result);
                } catch (e) {
                    var res = smart_eval(result);
                    if (res !== undefined) {
                        return res;
                    } else {
                        return result;
                    }
                }
            } else {
                return result;
            }
        }.bind(this))
        .then(UI.showMsg)
        .then(function (obj) {
            if (obj && obj.code) {
                // TODO: для отделения данных от UI
                //if (obj.code.ui) {
                if (obj.code.config) {
                    return UI.create(obj.code);
                } else {
                    return obj.code;
                }
            } else {
                return obj;
            }
        }.bind(this))
        .catch(function (err) {
            console.log(response.responseText);
            console.log(err);
            if (err.message) {
                Ext.Msg.show({
                    title: 'Внимание'
                    , msg: err.message
                    , buttons: Ext.Msg.OK
                    , fn: Ext.emptyFn
                    , animEl: 'elId'
                    , icon: Ext.MessageBox.ERROR
                });
            } else
                uiAjaxFailMessage(err, {});
        });
};

UI.callAction = function (cfg, scope) {
    if (scope === undefined) scope = this;
    return new Q()
        .then(function () {
            if (scope instanceof Ext.Component) {
                scope.fireEvent('mask', scope, cfg.loadMaskText);
            }
        }.bind(scope))
        .then(UI.ajax.createDelegate(scope, [cfg]))
        .then(function (response) {
            // восстанавливаем специальные символы типа &amp
            // https://code.i-harness.com/en/q/387666
            var elem = document.createElement('textarea');
            elem.innerHTML = response.responseText;
            response.responseText = elem.value;
            return response;
        })
        .then(UI.evalResult)
        .then(cfg.success)
        .catch(cfg.failure)
        .finally(function () {
            if (scope instanceof Ext.Component) {
                scope.fireEvent('unmask', this);
            }
        }.bind(scope))
        .then(function (win) {
            if (win instanceof Ext.Component) {
                scope.fireEvent('mask', scope, cfg.mode, win);
                win.on('close',
                    scope.fireEvent.createDelegate(scope,
                        ['unmask', scope, win]), scope);
            }
            return win;
        }.bind(scope));
};

/**
 * Подгрузка модулей и их зависимостей
 *
 * @param modules
 * @returns {promise|Q.promise}
 */
UI.require = function (modules) {
    var needLoad = [],
        jsLoad,
        result = Q.defer();

    modules.forEach(function (value) {
        if (!Ext.ComponentMgr.isRegistered(value)) {
            needLoad.push(value);
        }
    });

    require(needLoad, function () {
        var requires = [],
            req,
            xtype,
            cls;

        // // Собираем requirements
        // for (var i = 0; i < arguments.length; i++) {
        //     xtype = needLoad[i];
        //     cls = Ext.ComponentMgr.types[xtype];
        //     if (!cls) {
        //         result.reject(new Error(String.format(
        //             'File name "{0}" and xtype in file name not the same!', xtype)));
        //         return;
        //     }
        //
        //     req = cls.prototype.requires;
        //     if (req) {
        //         requires.push(
        //             Q.fcall(UI.require.createDelegate(cls), req)
        //                 .catch(result.reject)
        //         )
        //     }
        // }
        return Q.all(requires).then(result.resolve);
    }, function (err) {
        // Разрегестриуем такой компонент, если его дочерние requirements не загрузились
        delete Ext.ComponentMgr.types[this.xtype];
        return result.reject(err);
    }.createDelegate(this));

    return result.promise;
};

/**
 * Генерирует запрос на сервер по переданному url
 * @param {String} url URL запроса на получение формы
 * @param {Object} desktop Объект типа AppDesktop.getDesktop()
 * @param {Object} параметры запроса
 */
function sendRequest(url, desktop, params){
    var mask = new Ext.LoadMask(document.body, {msg: 'Загрузка...'});
    return new Q()
        .then(mask.show.createDelegate(mask))
        .then(function () {
            return {url: url, params: params, method: 'POST'};
        })
        .then(UI.ajax)
        .then(UI.evalResult)
        .catch(uiAjaxFailMessage)
        .finally(mask.hide.createDelegate(mask));
}

new UI({
    desktop: AppDesktop,
    staticPrefix: '/static',
    storage: function (key, params) {
        // Загрузка конфигов с сервера
        return UI.ajax({
            url: key,
            params: params || {}
        }).then(UI.evalResult);
    },
    create: Ext.create
});