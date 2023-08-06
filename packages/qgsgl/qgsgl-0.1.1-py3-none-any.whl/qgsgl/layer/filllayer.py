from .base import BaseLayer
from ..utils import get_rgba
from qgis.core import QgsSimpleFillSymbolLayer


class FillLayer(BaseLayer):

    SUPPORTED_SYMBOL_LAYER = (QgsSimpleFillSymbolLayer)

    def __init__(self, qgis_symbol_layer, **kwargs):
        self.opacity = kwargs.get('opacity', 1)
        super().__init__(qgis_symbol_layer)

    @classmethod
    def supports_symbol_layer(cls, symbol_layer):
        return isinstance(symbol_layer, cls.SUPPORTED_SYMBOL_LAYER)

    def get_paint_properties(self):
        return {
            'fill-color': get_rgba(self.qgis_symbol_layer.color()),
            'fill-opacity': self.opacity
        }

    def get_layout_properties(self):
        pass

    def get_type(self):
        return 'fill'
