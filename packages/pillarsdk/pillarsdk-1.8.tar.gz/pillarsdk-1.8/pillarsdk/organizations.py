from .resource import List
from .resource import Find


class Organization(List, Find):
    """Organization class wrapping the REST nodes endpoint
    """
    path = "organizations"
