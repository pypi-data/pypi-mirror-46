from IPython.display import display, HTML # type: ignore
from typing import List, Optional, Dict
from uuid import UUID
import pandas as pd

from .cycle import Cycle
from .label import Label


class LabelBatch:
    def __init__(self, project, labels):
        self.project: Project = project
        self.labels: List[Label] = labels

    def __len__(self):
        return len(self.labels)

    @classmethod
    def deserialize(cls, project, response):
        labels = [Label.deserialize(label) for label in response]
        return cls(project, labels)

    def to_df(self):
        df = pd.DataFrame(columns=['document_id', 'label', 'annotations'])
        for label in self.labels:
            df = df.append(label.serialize(format='df', project=self.project), ignore_index=True)
        return df.set_index('document_id')


class Project:
    def __init__(self, api, project_id: UUID, project_data=None):
        self._api = api
        self.id: UUID = project_id
        self._labels: LabelBatch = None
        self.metadata = project_data['metadata'] # TODO-3: obviate need for metadata counts with methods that count the actual relations, eg, so that creating new cycle programatically is reflected in counts
        self.cycle_ids = [cycle['id'] for cycle in project_data['cycles']]

        if project_data:
            self.document_classes: List[Dict] = project_data['documentClasses']
            self.fragment_classes: List[Dict] = project_data['fragmentClasses']
        else:
            self.document_classes: List[Dict] = []
            self.fragment_classes: List[Dict] = []

    def __repr__(self):
        return f'<Project (id="{self.id}", label_count={self.metadata["labelCount"]}, document_count={self.metadata["documentCount"]}, cycle_count={len(self.cycle_ids)})>'

    def create_cycle(self) -> Cycle:
        return Cycle(self)

    def load_cycle(self, cycle_id):
        return Cycle.load(self, cycle_id)

    def label(self, df = None, cycle_id: str = None) -> Cycle:
        # TODO-3: allow passing `index_col` to use instead of df index

        if cycle_id:
            cycle = self.load_cycle(cycle_id)
        elif len(self.cycle_ids) == 1 and self.metadata['documentCount'] == 0:
            cycle = self.load_cycle(self.cycle_ids[0])
        else:
            cycle = Cycle(self)
            self.cycle_ids.append(cycle.id)

        if df is not None:
            cycle.add_documents(from_df=df)
            self.metadata['documentCount'] += len(df) # update project so that we don't continue to think count = 0
            cycle.save()

        cycle.label()

        return cycle

    @property
    def labels(self):
        if not self._labels:
            response = self._api.get(f'projects/{self.id}/labels')
            self._labels = LabelBatch.deserialize(self, response['labels'])
        return self._labels

    def open_app(self):
        s = f'<script type="text/javascript">window.open("{self._api.api_url}/projects/{self.id}")</script>'
        display(HTML(s))