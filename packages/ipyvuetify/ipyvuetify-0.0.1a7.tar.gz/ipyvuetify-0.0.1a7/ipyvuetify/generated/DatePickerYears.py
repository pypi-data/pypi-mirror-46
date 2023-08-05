from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class DatePickerYears(VuetifyWidget):

    _model_name = Unicode('DatePickerYearsModel').tag(sync=True)

    color = Unicode(None, allow_none=True).tag(sync=True)

    locale = Unicode(None, allow_none=True).tag(sync=True)

    max = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    min = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    readonly = Bool(None, allow_none=True).tag(sync=True)

    value = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)





__all__ = ['DatePickerYears']
