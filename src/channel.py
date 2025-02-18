import json
import os

from googleapiclient.discovery import build
from functools import total_ordering


@total_ordering
class Channel:
    """Класс для ютуб-канала"""
    api_key: str = os.getenv("YT_API_KEY")

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""

        self.channel_id = channel_id
        self.youtube = self.get_service().channels().list(id=self.channel_id,
                                                          part='snippet,statistics').execute()
        self.title = self.youtube['items'][0]['snippet']['title']
        self.description = self.youtube['items'][0]['snippet']['description']
        self.url = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = int(self.youtube['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(self.youtube['items'][0]['statistics']['videoCount'])
        self.view_count = int(self.youtube['items'][0]['statistics']['viewCount'])

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        print(json.dumps(self.youtube, indent=2, ensure_ascii=False))

    @classmethod
    def get_service(cls):
        return build('youtube', 'v3', developerKey=cls.api_key)

    def to_json(self, file_path):
        channel_data = {
            'name_chanel': self.title,
            'description': self.description,
            'url_channel': self.url,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(file_path, 'w') as fp:
            json.dump(channel_data, fp, indent=2, ensure_ascii=False)
