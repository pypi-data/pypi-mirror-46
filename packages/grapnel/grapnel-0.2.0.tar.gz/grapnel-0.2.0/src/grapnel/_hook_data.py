from typing import Any


class BaseHookData(object):
    pass


class ValueChangedHookData(BaseHookData):
    @property
    def original_value(self) -> Any:
        return self._original_value

    @property
    def current_value(self) -> Any:
        return self._current_value

    def __init__(self, original_value: Any, current_value: Any):
        super(ValueChangedHookData, self).__init__()

        self._original_value = original_value
        self._current_value = current_value
