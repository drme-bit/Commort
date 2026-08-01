# base commort source class
from src.fetcher.sources.CommortSourceBase import CommortSource, Comment

# env
import os
from dotenv import load_dotenv

# google api
from googleapiclient.discovery import build


class YoutubeSource(CommortSource):
    source = "youtube"

    def __init__(self, search_queries: list[str] = None, use_trending: bool = True):
        load_dotenv()
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.search_queries = search_queries or ["funny fails", "memes compilation"]
        self.use_trending = use_trending

    def get_trending_video_ids(self, region_code: str = "US", max_results: int = 10) -> list[str]:
        response = self.youtube.videos().list(
            part="id",
            chart="mostPopular",
            videoCategoryId="23",  # Comedy
            regionCode=region_code,
            maxResults=max_results,
        ).execute()

        return [item["id"] for item in response.get("items", [])]

    def search_video_ids(self, query: str, max_results: int = 10) -> list[str]:
        response = self.youtube.search().list(
            part="id",
            q=query,
            type="video",
            order="viewCount",
            maxResults=max_results,
        ).execute()

        return [item["id"]["videoId"] for item in response.get("items", [])]

    def _get_video_ids(self, videos_per_query: int = 5) -> list[str]:
        video_ids = []

        if self.use_trending:
            video_ids += self.get_trending_video_ids(max_results=videos_per_query)

        for query in self.search_queries:
            video_ids += self.search_video_ids(query, max_results=videos_per_query)

        return list(set(video_ids))

    def fetch_comments(self, video_id: str, limit: int = 20) -> list[Comment]:
        response = self.youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            order="relevance",
            maxResults=limit,
            textFormat="plainText",
        ).execute()

        comments = []
        for item in response.get("items", []):
            top = item["snippet"]["topLevelComment"]["snippet"]
            comments.append(Comment(
                id=item["id"],
                source=self.source,
                text=top["textDisplay"],
                score=top["likeCount"],
                author=top["authorDisplayName"],
                author_id=top.get("authorChannelId", {}).get("value", ""),
                post_title=f"video:{video_id}",
                post_url=f"https://youtube.com/watch?v={video_id}",
            ))
        return comments

    def fetch(self, limit: int = 20) -> list[Comment]:
        comments: list[Comment] = []

        for video_id in self._get_video_ids():
            comments += self.fetch_comments(video_id, limit)

        return comments