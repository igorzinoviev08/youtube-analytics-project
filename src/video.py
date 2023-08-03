from src.channel import Channel


class Video:
    def __init__(self, video_id: str) -> None:
        self.video_id = video_id
        try:

            youtube = Channel.get_service().videos().list(part='snippet,statistics', id=self.video_id).execute()
            video_data = youtube.get('items')[0]
        except IndexError:
            print('невозможно получить данные')
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

        else:
            self.title = video_data.get('snippet').get('title')
            self.url = f'https://www.youtube.com/watch?v={self.video_id}'
            self.view_count = video_data.get('statistics').get('viewCount')
            self.like_count = video_data.get('statistics').get('likeCount')

    def __str__(self) -> str:
        return self.title


class PLVideo(Video):
    def __init__(self, video_id: str, playlist_id: str) -> None:
        self.playlist_id = playlist_id
        super().__init__(video_id)
