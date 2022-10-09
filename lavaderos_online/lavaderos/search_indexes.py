from haystack import indexes
from lavaderos.models import *

class LavaderoIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    nombre = indexes.CharField(model_attr='nombre')
    direccion = indexes.CharField(model_attr='direccion')
    estado = indexes.CharField(model_attr='estado')
    id = indexes.CharField(model_attr='id')

    def get_model(self):
        return Lavadero

    def index_queryset(self, using=None):
        return self.get_model().objects.exclude(estado='I')