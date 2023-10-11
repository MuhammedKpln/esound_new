from datetime import date, datetime
from typing import List, TypedDict

# class _ArtistPayloadModel(TypedDict):
#     authorReference: int
#     authorId: str
#     name: str
#     nameRename: str
#     imageUrl: str
#     type: int


class _TracksPayloadModel(TypedDict):
    songLibraryId: int
    addedDate: datetime
    listenDate: datetime
    isOffline: bool
    listenTimes: int
    id: int
    type: int
    ytMusic: int
    explicit: bool
    title: str
    titleRename: str
    trackId: str
    duration: int
    thirdPartyTrackId: str
    authorId: str
    authorType: int
    authorImageUrl: str
    authorName: str
    authorRename: str


class EsoundLibraryModel(TypedDict):
    tracks: List[_TracksPayloadModel]
