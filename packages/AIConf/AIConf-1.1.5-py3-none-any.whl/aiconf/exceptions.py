from aiconf.aiconf import fqcn


class MalformattedConfigException(Exception):
    pass


class ConstructorLogicException(Exception):
    def __init__(self, cls, msg):
        super().__init__(f"{fqcn(cls)}: {msg}")
