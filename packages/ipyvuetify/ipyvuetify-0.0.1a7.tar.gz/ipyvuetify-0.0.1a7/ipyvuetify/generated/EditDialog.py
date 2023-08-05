from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class EditDialog(VuetifyWidget):

    _model_name = Unicode('EditDialogModel').tag(sync=True)

    cancel_text = Any(None, allow_none=True).tag(sync=True)

    dark = Bool(None, allow_none=True).tag(sync=True)

    large = Bool(None, allow_none=True).tag(sync=True)

    lazy = Bool(None, allow_none=True).tag(sync=True)

    light = Bool(None, allow_none=True).tag(sync=True)

    persistent = Bool(None, allow_none=True).tag(sync=True)

    return_value = Any(None, allow_none=True).tag(sync=True)

    save_text = Any(None, allow_none=True).tag(sync=True)

    transition = Unicode(None, allow_none=True).tag(sync=True)





__all__ = ['EditDialog']
