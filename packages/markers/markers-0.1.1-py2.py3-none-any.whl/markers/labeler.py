import ipywidgets as widgets # type: ignore
from traitlets import Unicode, Dict, List # type: ignore

from .label import Label

def noop(*args): pass

class MissingCycle(Exception): pass

@widgets.register
class Labeler(widgets.DOMWidget):
    """A data labeling widget to be used with Markers.ai."""
    _view_name = Unicode('AnnotationView').tag(sync=True)
    _model_name = Unicode('AnnotationModel').tag(sync=True)
    _view_module = Unicode('markers').tag(sync=True)
    _model_module = Unicode('markers').tag(sync=True)
    _view_module_version = Unicode('^0.1.0').tag(sync=True)
    _model_module_version = Unicode('^0.1.0').tag(sync=True)

    document = Dict({}).tag(sync=True)
    fragment_classes = List([]).tag(sync=True)
    document_classes = List([]).tag(sync=True)
    metadata = Dict({}).tag(sync=True)

    def __init__(self, project, cycle, **kwargs):
        if not cycle:
            raise MissingCycle('Labeler cannot be created without a cycle.')

        self.cycle = cycle
        super(Labeler, self).__init__(**kwargs)

        self.project = project
        self.document_classes = project.document_classes
        self.fragment_classes = project.fragment_classes
        self.skipped_tasks = []
        self.current_task = None

        self.on_msg(self._handle_message)

        self._load_next_document()

    def _handle_message(self, _, content, buffers):
        handlers = {
            'close_widget': self._handle_close,
            'save_label': self._handle_save_label,
            'skip_document': self._handle_skip_document
        }
        handler = handlers.get(content['event'], noop)
        handler(content.get('data', None))

    def _handle_close(self, *args):
        self.close()

    def _handle_save_label(self, data):
        new_label = Label.create_from_labeler(
            self.document,
            data['label']['name'],
            data['label']['id'],
            self.project,
            data['annotations']
        )
        self.cycle.add_label(self.current_task, new_label)

        self._load_next_document()

    def _handle_skip_document(self, *args):
        self.skipped_tasks.append(self.current_task.id)
        self._load_next_document()

    def _load_next_document(self):
        try:
            [self.current_task, task_index] = self.cycle.next_task(skipped_tasks=self.skipped_tasks)
            self.document = self.current_task.document.serialize()

            self.metadata = {
                'task_progress': task_index + 1,
                'task_count': len(self.cycle.tasks)
            }
        except IndexError as e:
            self.metadata = {
                'status': 'complete'
            }
