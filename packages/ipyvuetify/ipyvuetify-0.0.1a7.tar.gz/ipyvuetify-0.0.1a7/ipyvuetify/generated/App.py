from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class App(VuetifyWidget):

    _model_name = Unicode('AppModel').tag(sync=True)

    dark = Bool(None, allow_none=True).tag(sync=True)

    id = Unicode(None, allow_none=True).tag(sync=True)

    light = Bool(None, allow_none=True).tag(sync=True)





__all__ = ['App']
