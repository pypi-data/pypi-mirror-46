from typing import List, Optional, Dict

from .label import Label
from .document import Document

class Task:
    def __init__(self, id, is_complete, document):
        self.id = id
        self.is_complete = is_complete
        self.document = Document.deserialize(document)
        self.labels = []

    @classmethod
    def deserialize(cls, response):
        task = cls(response['id'], response['isComplete'], response['document'])
        for label_obj in response['labels']:
            label = Label.deserialize_from_task(task, label_obj)
            task.labels.append(label)
        return task
