
from typing import List, Optional, Union

from ytmusicapi import YTMusic

from helpers import Message
from models.ytmusic_song import YoutubeLikedSongModel, YoutubeLikedSongsModel


class YoutubeMusicApi:
    def __init__(self, is_oauth: Optional[bool] = True) -> None:

        if is_oauth:
            self.ytmusic = YTMusic('oauth.json')
        else:
            self.ytmusic = YTMusic('headers.json')

    def fetch_liked_songs(self) -> Union[List[YoutubeLikedSongModel], None]:
        try:
            tracks = YoutubeLikedSongsModel(**self.ytmusic.get_liked_songs(
                996))

            return tracks["tracks"]

        except Exception as e:
            print(e)
            Message.error(
                "Failed to authenticate with Youtube, please check your credentials.")
