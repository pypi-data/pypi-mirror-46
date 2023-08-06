from typing import Dict, Optional
from uuid import uuid4

class Document:
    @classmethod
    def deserialize(cls, doc):
        return cls(doc.get('id', None), doc['externalId'], doc['contents'], doc.get('metadata', {}))

    def __init__(self, id, external_id, contents, metadata={}):
        self.id: str = id
        self.external_id: str = external_id
        self.contents: str = contents
        self.metadata: Dict = metadata

    def serialize(self):
        return {
            'id': self.id,
            'external_id': self.external_id,
            'contents': self.contents,
            'metadata': self.metadata
        }
