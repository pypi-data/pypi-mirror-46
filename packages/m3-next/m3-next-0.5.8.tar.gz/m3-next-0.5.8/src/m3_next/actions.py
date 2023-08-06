from functools import wraps

from m3_next.results import DataResult, UIResult


def update_ui_actions(pack_instance, actions=None, allow_redefine=None):
    if actions is None:
        actions = pack_instance.actions

    for act in actions:
        # Сделаем доступным разделение действия на UI
        act.suffixes = ('ui',)
        # заменим исполнителя, на собственный
        act.run = ui_run(act, allow_redefine)


def ui_run(action, allow_redefine=None):
    original_run = action.run

    @wraps(original_run)
    def wrapper(self, *args, **kwargs):
        # проверим что нет суффикса
        suffix = args[1] if len(args) > 1 else None
        # если есть allow_redefine, то вызовем его, чтобы понять,
        # надо ли заменять UI или нет. иногда это надо делать в зависимости от
        # пришедших данных в контектсе
        if allow_redefine is not None:
            if suffix:
                allow = allow_redefine(self, *args[:-1], **kwargs)
            else:
                allow = allow_redefine(self, *args, **kwargs)
        else:
            allow = True
        if allow:
            # TODO: для отделения данных от UI
            # if not suffix and action:
            #     return DataResult(
            #         model={},
            #         ui=action.get_absolute_url() + ":ui",
            #         context=args[0]
            #     )
            if suffix:
                return redefine_ui(original_run(self, *args[:-1], **kwargs))
            else:
                return redefine_ui(original_run(self, *args, **kwargs))
        else:
            return original_run(self, *args, **kwargs)

    return wrapper


def redefine_ui(response):
    # удалим профиль из контекста
    if response.context and 'profile' in response.context.__dict__:
        del response.context.profile

    return UIResult(response.data)