import logging
import os
import time
from datetime import date

from dotenv import load_dotenv

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.domain.comment import Comment
from src.domain.ports import CommentFetcher

logger = logging.getLogger("commort.youtube")


class YoutubeSource(CommentFetcher):
    source = "youtube"

    def __init__(
        self,
        search_queries: list[str] = None,
        use_trending: bool = True,
        video_cache_ttl: int = 3600,
    ):
        load_dotenv()
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = build("youtube", "v3", developerKey=self.api_key)
        self.search_queries = search_queries or ["funny fails", "memes compilation"]
        self.use_trending = use_trending
        self._cache: dict[str, tuple[float, list[str]]] = {}
        self._cache_ttl = video_cache_ttl
        self._quota_hit = False

    def _get_video_ids(self, videos_per_query: int = 5) -> list[str]:
        video_ids: list[str] = []

        if self.use_trending:
            video_ids += self._cached("trending", lambda: self.get_trending_video_ids(max_results=videos_per_query))

        for query in self.search_queries:
            key = f"search:{query}:{date.today()}"
            video_ids += self._cached(key, lambda q=query: self.search_video_ids(q, max_results=videos_per_query))

        return list(set(video_ids))

    def _cached(self, key: str, loader) -> list[str]:
        now = time.time()
        cached = self._cache.get(key)
        if cached and now - cached[0] < self._cache_ttl:
            return cached[1]

        if self._quota_hit:
            return cached[1] if cached else []

        try:
            ids = loader()
        except HttpError as exc:
            logger.warning("youtube api error for %s: %s", key, exc.reason or exc)
            self._quota_hit = True
            return cached[1] if cached else []

        self._cache[key] = (now, ids)
        return ids

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
                author_avatar=top.get("authorProfileImageUrl", ""),
                post_title=f"video:{video_id}",
                post_url=f"https://youtube.com/watch?v={video_id}",
            ))
        return comments

    def fetch(self, limit: int = 20) -> list[Comment]:
        comments: list[Comment] = []

        for video_id in self._get_video_ids():
            try:
                comments += self.fetch_comments(video_id, limit)
            except HttpError as exc:
                logger.warning("comments error for %s: %s", video_id, exc.reason or exc)
                continue

        return comments
