from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class StepperContent(VuetifyWidget):

    _model_name = Unicode('StepperContentModel').tag(sync=True)

    step = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)





__all__ = ['StepperContent']
