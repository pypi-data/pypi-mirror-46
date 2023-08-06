from typing import List, Dict, Optional
from uuid import uuid4


class Annotation:
    def __init__(self, cls, selected_text, notes=None, raw=None):
        self.cls = cls
        self.selected_text = selected_text
        self.notes = notes
        self.raw = raw

    @classmethod
    def create_from_labeler(cls, project, obj):
        annotation_class = 'unknown'
        for fc in project.fragment_classes:
            if fc['id'] == obj['categoryId']:
                annotation_class = fc['name']

        return cls(annotation_class, obj['selectedText'], raw=obj)

    @classmethod
    def deserialize(cls, obj):
        return cls(obj['annotationCategory'], obj['selectedText'])

    def serialize(self, format='df'):
        if format == 'df':
            return {
                'class': self.cls,
                'selected_text': self.selected_text,
                'notes': self.notes
            }
        elif format == 'api':
            return self.raw
        else:
            raise Exception('Unsupported serialization format.')



class Label:
    @classmethod
    def deserialize_from_task(cls, task, response):
        annotations = [Annotation.deserialize(a) for a in response['contents']['annotations']]
        return cls(
            task.document.id,
            task.document.external_id,
            response['contents']['categoryName'],
            response['contents']['categoryId'],
            annotations,
            id=response['id']
        )

    @classmethod
    def deserialize(cls, label):
        annotations = [Annotation.deserialize(a) for a in label['annotations']]
        return cls(
            label['documentId'], # TODO-1: replace with id
            label['documentId'],
            label['documentCategory'],
            None, # class_id
            annotations=annotations
            # TODO-2: we need to pull id so that it isn't auto-generated
        )

    @classmethod
    def create_from_labeler(cls, document, class_name, class_id, project, annotations=None):
        if not annotations:
            annotations = []
        annotations = [Annotation.create_from_labeler(project, a) for a in annotations]
        return cls(document['id'], document['external_id'], class_name, class_id, annotations)

    def __init__(self, document_id, document_external_id, class_name, class_id, annotations=[], id=uuid4()):
        self.id: str = id
        self.document_id: str = document_id
        self.document_external_id: str = document_external_id
        self.cls: str = class_name
        self.cls_id: str = class_id

        if not annotations:
            annotations = []
        self.annotations: List[Annotation] = annotations # TODO-2: convert away from dict to Annotation class
        # TODO-3: creator information and other metadata, coming from API

    def serialize(self, project=None, format='api'):
        serialized = {
            'annotations': [a.serialize(format=format) for a in self.annotations]
        }

        if format == 'api':
            serialized['document_id'] = self.document_id
            serialized['class'] = self.cls
            serialized['class_id'] = self.cls_id
        elif format == 'df':
            serialized['document_id'] = self.document_external_id
            serialized['label'] = self.cls
        else:
            raise Exception('Unsupported serialization format.')

        return serialized
