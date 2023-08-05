from traitlets import (
    Unicode, Enum, Instance, Union, Float, Int, List, Tuple, Dict,
    Undefined, Bool, Any
)
from ipywidgets import Widget, DOMWidget
from ipywidgets.widgets.widget import widget_serialization

from .VuetifyWidget import VuetifyWidget


class ListTileAvatar(VuetifyWidget):

    _model_name = Unicode('ListTileAvatarModel').tag(sync=True)

    color = Unicode(None, allow_none=True).tag(sync=True)

    size = Union([
        Float(),
        Unicode()
    ], default_value=None, allow_none=True).tag(sync=True)

    tile = Bool(None, allow_none=True).tag(sync=True)





__all__ = ['ListTileAvatar']
