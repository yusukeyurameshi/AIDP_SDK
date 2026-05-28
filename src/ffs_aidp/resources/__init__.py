"""Domain resource clients exposed by :class:`ffs_aidp.AIDPClient`."""

from .catalogs import CatalogsResource
from .clusters import ClustersResource
from .delta_share import DeltaShareResource
from .mlops import MLOpsResource
from .notebooks import NotebooksResource
from .schemas import SchemasResource
from .volumes import VolumesResource
from .workflows import WorkflowsResource
from .workspaces import WorkspacesResource

__all__ = [
    "CatalogsResource",
    "ClustersResource",
    "DeltaShareResource",
    "MLOpsResource",
    "NotebooksResource",
    "SchemasResource",
    "VolumesResource",
    "WorkflowsResource",
    "WorkspacesResource",
]
