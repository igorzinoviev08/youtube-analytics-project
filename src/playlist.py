from src.channel import Channel

import isodate
from datetime import timedelta


class PlayList:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        playlist_videos = Channel.get_service().playlistItems().list(playlistId=playlist_id,
                                                                     part='snippet, contentDetails',
                                                                     maxResults=50,
                                                                     ).execute()
        playlist_data = playlist_videos['items'][0]
        self.title = playlist_data['snippet']['title'].split('.')[0]
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        self.video_response = Channel.get_service().videos().list(part='contentDetails,statistics',
                                                                  id=','.join(video_ids)
                                                                  ).execute()

    @property
    def total_duration(self):
        total_duration = timedelta()
        for video in self.video_response['items']:
            iso_8601_duration = video['contentDetails']['duration']
            total_duration += isodate.parse_duration(iso_8601_duration)
        return total_duration

    def show_best_video(self):
        best_video = max(self.video_response['items'], key=lambda video: video['statistics']['likeCount'])
        return f'https://youtu.be/{best_video["id"]}'
