from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class RowExpandTransition(VuetifyWidget):

    _model_name = Unicode('RowExpandTransitionModel').tag(sync=True)

    mode = Unicode(None, allow_none=True).tag(sync=True)





__all__ = ['RowExpandTransition']
