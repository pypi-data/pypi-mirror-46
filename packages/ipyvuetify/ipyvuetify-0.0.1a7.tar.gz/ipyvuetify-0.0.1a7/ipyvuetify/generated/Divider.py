from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class Divider(VuetifyWidget):

    _model_name = Unicode('DividerModel').tag(sync=True)

    dark = Bool(None, allow_none=True).tag(sync=True)

    inset = Bool(None, allow_none=True).tag(sync=True)

    light = Bool(None, allow_none=True).tag(sync=True)

    vertical = Bool(None, allow_none=True).tag(sync=True)





__all__ = ['Divider']
