
class Module:
    """Module Class"""

    def __init__(self, iotex) -> None:
        self.iotex = iotex

    @classmethod
    def attach(cls, target, module_name: str = None) -> None:
        if not module_name:
            module_name = cls.__name__.lower()

        if hasattr(target, module_name):
            raise AttributeError(
                "Cannot set {0} module named '{1}'.  The object "
                "already has an attribute with that name".format(
                    target,
                    module_name,
                )
            )

        if isinstance(target, Module):
            iotex = target.iotex
        else:
            iotex = target

        setattr(target, module_name, cls(iotex))
