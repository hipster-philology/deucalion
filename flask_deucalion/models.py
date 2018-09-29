"""

"""

from typing import List, Optional, Union
from .formats import Formats, JsonLd, Hydra
from flask import current_app, url_for


class Author(str):
    def __new__(cls, name: Union[str, "Author"], lod=None):
        if isinstance(name, Author):
            return name
        o = str.__new__(Author, name)
        o.lod = None
        if lod:
            o.lod = lod
        return o

    def export(self, mimetype: str) -> Union[dict, str]:
        if Formats[mimetype] == JsonLd:
            if self.lod:
                return {
                    "@id": self.lod,
                    "@label": str(self)
                }
            return str(self)


class Description(str):
    def __new__(cls, value: Union[str, "Description"], lang=None):
        if isinstance(value, Description):
            return value
        o = str.__new__(Description, value)
        o.lang = None
        if lang:
            o.lang = lang
        return o

    def export(self, mimetype):
        if Formats[mimetype] == JsonLd:
            if self.lang:
                return {
                    "@value": str(self),
                    "@language": self.lang
                }
            return str(self)
        elif mimetype == Hydra:
            return str(self)


_str_description = Union[str, Description]


class Model:
    def __init__(
        self,
        identifier: str,
        language_code: str,
        model_path: str,
        title: str= None,
        authors: Optional[List[Author]]= None,
        redirect: Optional["Model"]= None,
        descriptions: Union[None, _str_description, List[_str_description]]= None,
        sources: List= None
    ):
        # Minimal settings
        self.identifier = identifier
        self.language_code = language_code
        self.model_path = model_path
        self.title = title or "Model {} for {}".format(
            identifier, language_code
        )

        # Authors and credits settings
        self.authors = []
        if authors:
            self.authors.extend(authors)

        self.descriptions = []
        if descriptions:
            if isinstance(descriptions, list):
                self.descriptions.extend([
                    Description(desc)
                    for desc in descriptions
                ])
            else:
                self.descriptions.append(Description(descriptions))

        # Old model that redirects to a new one
        self.redirect = redirect

    def export(self, mimetype):
        with current_app.app_context():
            if Formats[mimetype] == JsonLd:
                single_desc = "Unavailable"
                if len(self.descriptions):
                    single_desc = self.descriptions[0]

                data = {
                    "@id": url_for("deucalion.api_model_get", model_id=self.identifier, _external=True),
                    "title": self.title,
                    "@type": "Collection",
                    "description": single_desc,
                    "dc:language": self.language_code,
                    "dc:creator": [
                        author.export(mimetype)
                        for author in self.authors
                    ],
                    "dc:description": [
                        description.export(mimetype)
                        for description in self.descriptions
                    ]
                }
                return data

