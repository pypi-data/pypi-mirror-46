from gumo.core.injector import injector
from gumo.datastore.infrastructure.entity_key_mapper import EntityKeyMapper

from google.cloud import datastore


class DatastoreMapperMixin:
    _entity_key_mapper = None
    DatastoreEntity = datastore.Entity

    @property
    def entity_key_mapper(self) -> EntityKeyMapper:
        if self._entity_key_mapper is None:
            self._entity_key_mapper = injector.get(EntityKeyMapper)  # type: EntityKeyMapper

        return self._entity_key_mapper
