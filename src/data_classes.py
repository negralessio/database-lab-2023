""" Module that handles the Data Access Object (DAO) / Data Classes """
from dataclasses import dataclass
from datetime import datetime
from typing import List, Union


@dataclass
class Headline:
    main: str
    social: str


@dataclass
class Author:
    abbreviation: Union[str, None]
    departments: List[str]
    names: List[str]


@dataclass
class Article:
    date_created: Union[str, datetime]
    date_published: Union[str, datetime]
    breadcrumbs: List[str]
    id: str
    channel: str
    comments_enabled: bool
    date_modified: Union[str, datetime]
    headline: Union[dict, Headline]
    intro: str
    author: Union[dict, Author]
    text: str
    topics: List[str]
    subchannel: str
    url: str

    def __post_init__(self):
        self.date_created = datetime.fromisoformat(self.date_created)
        self.date_published = datetime.fromisoformat(self.date_published)
        self.date_modified = datetime.fromisoformat(self.date_modified)

        self.headline = Headline(**self.headline)
        self.author = Author(**self.author)



