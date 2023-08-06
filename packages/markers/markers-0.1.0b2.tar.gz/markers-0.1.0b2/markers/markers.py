from .project import Project
from .api import Api

class Markers:
    def __init__(self, api_key: str = None, api_url: str = 'https://app.markers.ai'):
        """ api_key should be associated with both project AND user """
        self._api = Api(api_key, api_url)

    def load_project(self, project_id):
        project_data = self._api.get(f'projects/{project_id}')
        project = Project(self._api, project_id, project_data)
        return project
