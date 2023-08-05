from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class DatePickerHeader(VuetifyWidget):

    _model_name = Unicode('DatePickerHeaderModel').tag(sync=True)

    color = Unicode(None, allow_none=True).tag(sync=True)

    dark = Bool(None, allow_none=True).tag(sync=True)

    disabled = Bool(None, allow_none=True).tag(sync=True)

    light = Bool(None, allow_none=True).tag(sync=True)

    locale = Unicode(None, allow_none=True).tag(sync=True)

    max = Unicode(None, allow_none=True).tag(sync=True)

    min = Unicode(None, allow_none=True).tag(sync=True)

    next_icon = Unicode(None, allow_none=True).tag(sync=True)

    prev_icon = Unicode(None, allow_none=True).tag(sync=True)

    readonly = Bool(None, allow_none=True).tag(sync=True)

    value = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)





__all__ = ['DatePickerHeader']
