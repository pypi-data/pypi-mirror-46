

class EasyCoConfig:
    """
    Control behaviour of EasyCo

    :var lower_case_keys: this will create and enforce lowercase keys
    :vartype lower_case_keys: bool

    :var create_optional_keys: when creating a config file this will create optional keys, too
    :vartype create_optional_keys: bool
    """

    def __init__(self):
        self.lower_case_keys: bool = True
        self.create_optional_keys: bool = True


DEFAULT_CONFIGURATION = EasyCoConfig()
