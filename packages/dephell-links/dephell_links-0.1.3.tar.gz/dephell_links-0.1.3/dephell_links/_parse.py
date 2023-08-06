# app
from ._path import DirLink, FileLink
from ._unknown import UnknownLink
from ._url import URLLink
from ._vcs import VCSLink


_links = (
    URLLink,
    DirLink,
    FileLink,
    VCSLink,
)


def parse_link(link: str):
    if not link:
        return None
    for parser in _links:
        parsed = parser.parse(link)  # type: ignore
        if parsed is not None:
            return parsed
    return UnknownLink(link)
