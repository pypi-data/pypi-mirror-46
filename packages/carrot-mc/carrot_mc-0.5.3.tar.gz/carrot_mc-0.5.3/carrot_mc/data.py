import json

def object_to_dict_nested(obj):
    if isinstance(obj, Automappable):
        d = {}
        for k, v in vars(obj).items():
            if isinstance(v, Autoproperty):
                d[k] = object_to_dict_nested(v.value)
        return d
    elif isinstance(obj, dict):
        return obj
    elif isinstance(obj, list):
        return [object_to_dict_nested(o) for o in obj]
    else:
        return obj


class Autoproperty(object):
    def __init__(self, prop_type, default_value=None, is_list=False):
        self.prop_type = prop_type
        self.default_value = default_value
        self.value = default_value
        self.is_list = is_list


class Automappable(object):
    def to_dict(self):
        return object_to_dict_nested(self)

    @classmethod
    def from_dict(cls, obj):
        instance = cls()

        for k, v in vars(instance).items():
            if isinstance(v, Autoproperty):
                try:
                    value = obj[k]
                except:
                    value = v.default_value

                if value and issubclass(v.prop_type, Automappable):
                    if v.is_list:
                        value = [v.prop_type.from_dict(vv) for vv in value]
                    else:
                        value = v.prop_type.from_dict(value)

                setattr(instance, k, value)

        return instance

    def __getattribute__(self, name):
        attr = super().__getattribute__(name)
        if isinstance(attr, Autoproperty):
            return attr.value
        else:
            return attr

    def __setattr__(self, name, value):
        if isinstance(value, Autoproperty):
            super().__setattr__(name, value)
            return

        try:
            attr = super().__getattribute__(name)
            if isinstance(attr, Autoproperty):
                attr.value = value
            else:
                super().__setattr__(name, value)
        except AttributeError:
            super().__setattr__(name, value)

    def __repr__(self):
        return json.dumps(self.to_dict())