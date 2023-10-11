from typing import Optional, TypedDict


class _AddedSongPayloadModel(TypedDict):
    librarySongId: int
    songId: int


class AddLibrarySongInputModel(TypedDict):
    songId: int


class AddLibrarySongModel(TypedDict):
    addedSong: _AddedSongPayloadModel
