from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class StepperStep(VuetifyWidget):

    _model_name = Unicode('StepperStepModel').tag(sync=True)

    color = Unicode(None, allow_none=True).tag(sync=True)

    complete = Bool(None, allow_none=True).tag(sync=True)

    complete_icon = Unicode(None, allow_none=True).tag(sync=True)

    edit_icon = Unicode(None, allow_none=True).tag(sync=True)

    editable = Bool(None, allow_none=True).tag(sync=True)

    error_icon = Unicode(None, allow_none=True).tag(sync=True)

    rules = List(Any(), default_value=None, allow_none=True).tag(sync=True)

    step = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)





__all__ = ['StepperStep']
