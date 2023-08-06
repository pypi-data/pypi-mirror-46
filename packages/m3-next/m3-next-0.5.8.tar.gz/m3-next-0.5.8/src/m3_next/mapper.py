import inspect


suppress_if_empty = lambda x: True if not x else False
suppress_if_None = lambda x: True if x is None else False


def deepgetattr(obj, attr, default=None):
    if '.' in attr:
        first_attr = attr.split('.')[0]
        other_attr = '.'.join(attr.split('.')[1:])
        if hasattr(obj, first_attr):
            val = deepgetattr(getattr(obj, first_attr), other_attr, default)
        else:
            val = None
    else:
        val = getattr(obj, attr, default)
    return val


def getter(attr, default=None, suppress_if=None, pregetter=None):
    def get_attr(obj=None):
        if obj is None:
            return default
        else:
            if pregetter and callable(pregetter):
                value = pregetter(obj, attr)
            else:
                value = deepgetattr(obj, attr)
            if callable(suppress_if):
                suppress = suppress_if(value)
            else:
                if suppress_if is not None:
                    suppress = value == suppress_if
                else:
                    suppress = suppress_if_empty(value)
            if not suppress:
                # иногда это может быть метод - вызовем его
                if callable(value):
                    return value()
                else:
                    return value
            else:
                return None
    return get_attr


class ComponentMapper(object):
    def __init__(self):
        # словарь зарегистрированных компонентов
        self._registry = {}

    def reg(self, clazz, mapping):
        # регистрация класса и его маппинга
        self._registry[clazz] = mapping

    def get(self, clazz):
        return self._registry.get(clazz)

    def hierarchy(self, clazz):
        result = {}
        # получим классы предки у текущего компонента
        # в цикле пойдем по возрастанию и будем забирать атрибуты и значения
        for clazz in reversed(inspect.getmro(clazz)):
            mapping = self.get(clazz)
            # если маппинга нет, то попробуем подтянуть из класса
            if not mapping:
                if hasattr(clazz, 'xtype'):
                    result['xtype'] = getattr(clazz, 'xtype')
                if hasattr(clazz, 'js_attrs'):
                    mapping = getattr(clazz, 'js_attrs')
                    if callable(mapping):
                        mapping = mapping()

            if mapping:
                result.update(mapping)
        return result

    def get_config(self, component):
        # получение конфига компонента
        config = {}
        mapping = self.hierarchy(component.__class__)
        if mapping:
            # пробежимся по зарегистрированным атрибутам
            for k, v in mapping.items():
                if k == '':
                    if hasattr(v, '__call__'):
                        value = v(component)
                    else:
                        value = getattr(component, v)
                    config = self.get_config(value)
                    continue
                obj = config
                # если в ключе есть точка - значит надо объединить
                # с другими атрибутами
                if '.' in k:
                    for attr in k.split('.')[:-1]:
                        if attr not in obj:
                            obj[attr] = {}
                        obj = obj[attr]
                    k = k.split('.')[-1]

                # если в качестве значения строка и ключ не xtype,
                # то это тоже геттер
                if isinstance(v, str) and k != 'xtype':
                    v = getter(v)
                # если значение вызываемое - значит там функция
                if hasattr(v, '__call__'):
                    default = v()
                    value = v(component)
                    if value is None and value != default:
                        obj[k] = default
                    elif value != default:
                        obj[k] = value
                else:
                    if v is None:
                        if k in obj:
                            del obj[k]
                    else:
                        obj[k] = v

        # Для контролов, которые еще используют extra
        if hasattr(component, 'extra') and isinstance(component.extra, dict):
            config.update(component.extra)
        return config

    def get_data(self, component):
        # получение словаря данных
        return {}


mapper = ComponentMapper()


def reg_js_mapping(clazz, mapping):
    mapper.reg(clazz, mapping)


def lazy_hierarchy_mapping(clazz):
    def get():
        return mapper.hierarchy(clazz)
    return get


def get_ui_config(component):
    if isinstance(component, dict):
        return component
    return mapper.get_config(component)