from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, TypedDict


class Thumbnail(TypedDict):
    url: str
    width: int
    height: int


class Album(TypedDict):
    name: str
    id: Optional[str]


class FeedbackTokens(TypedDict):
    add: str
    remove: str


class LikeStatus(Enum):
    LIKE = "LIKE"


class VideoType(Enum):
    MUSICVIDEOTYPEATV = "MUSIC_VIDEO_TYPE_ATV"
    MUSICVIDEOTYPEOFFICIALSOURCEMUSIC = "MUSIC_VIDEO_TYPE_OFFICIAL_SOURCE_MUSIC"
    MUSICVIDEOTYPEOMV = "MUSIC_VIDEO_TYPE_OMV"
    MUSICVIDEOTYPEUGC = "MUSIC_VIDEO_TYPE_UGC"


class YoutubeLikedSongModel(TypedDict):
    videoId: str
    title: str
    artists: List[Album]
    likeStatus: LikeStatus
    thumbnails: List[Thumbnail]
    isAvailable: bool
    isExplicit: bool
    videoType: VideoType
    duration: str
    durationseconds: int
    album: Optional[Album]
    feedbackTokens: Optional[FeedbackTokens]


class YoutubeLikedSongsModel(TypedDict):
    id: str
    privacy: str
    title: str
    thumbnails: List[Thumbnail]
    description: str
    views: None
    duration: None
    trackCount: int
    related: List[Any]
    tracks: List[YoutubeLikedSongModel]
    duration_seconds: int
