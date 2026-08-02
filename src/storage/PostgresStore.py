from datetime import datetime

from sqlalchemy import (
    Index,
    String,
    Text,
    desc,
    func,
    select,
    text,
    update,
)
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, aliased, mapped_column

from src.domain.comment import Comment
from src.domain.ports import CommentStore
from src.domain.scoring import adaptive_score
from src.domain.verdict import MeeseeksVerdict
from src.service.views import comment_view, user_view

MIGRATIONS = [
    "ALTER TABLE comments ADD COLUMN IF NOT EXISTS funny INTEGER",
    "ALTER TABLE comments ADD COLUMN IF NOT EXISTS wit INTEGER",
    "ALTER TABLE comments ADD COLUMN IF NOT EXISTS creativity INTEGER",
    "ALTER TABLE comments ADD COLUMN IF NOT EXISTS cringe INTEGER",
    "ALTER TABLE comments ADD COLUMN IF NOT EXISTS intelligence INTEGER",
    "ALTER TABLE comments ADD COLUMN IF NOT EXISTS adaptive_score INTEGER",
    "ALTER TABLE comments ADD COLUMN IF NOT EXISTS author_avatar TEXT",
]


class Base(DeclarativeBase):
    pass


class CommentModel(Base):
    __tablename__ = "comments"
    __table_args__ = (
        Index(
            "idx_comments_unscored",
            "fetched_at",
            postgresql_where=text("meeseeks_score IS NULL"),
        ),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    source: Mapped[str] = mapped_column(String)
    text: Mapped[str] = mapped_column(Text)
    score: Mapped[int] = mapped_column(default=0)
    author: Mapped[str] = mapped_column(String)
    author_id: Mapped[str] = mapped_column(String, default="")
    author_avatar: Mapped[str] = mapped_column(String, default="")
    post_title: Mapped[str] = mapped_column(String, default="")
    post_url: Mapped[str] = mapped_column(String, default="")
    fetched_at: Mapped[datetime] = mapped_column(server_default=func.now())
    meeseeks_score: Mapped[int | None]
    funny: Mapped[int | None]
    wit: Mapped[int | None]
    creativity: Mapped[int | None]
    cringe: Mapped[int | None]
    intelligence: Mapped[int | None]
    adaptive_score: Mapped[int | None]
    reaction: Mapped[str | None]
    scored_at: Mapped[datetime | None]


def _to_comment(m: CommentModel) -> Comment:
    return Comment(
        id=m.id,
        source=m.source,
        text=m.text,
        score=m.score,
        author=m.author,
        author_id=m.author_id,
        author_avatar=m.author_avatar,
        post_title=m.post_title,
        post_url=m.post_url,
    )


def _to_verdict(m: CommentModel) -> MeeseeksVerdict:
    return MeeseeksVerdict(
        funny=m.funny or 5,
        wit=m.wit or 5,
        creativity=m.creativity or 5,
        cringe=m.cringe or 5,
        intelligence=m.intelligence or 5,
        reaction=m.reaction or "",
    )


class PostgresStore(CommentStore):
    def __init__(self, dsn: str):
        if dsn.startswith("postgresql://"):
            dsn = dsn.replace("postgresql://", "postgresql+asyncpg://", 1)
        self._engine = create_async_engine(dsn)
        self._session_factory = async_sessionmaker(self._engine, expire_on_commit=False)

    async def connect(self) -> None:
        async with self._engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
            for stmt in MIGRATIONS:
                await conn.execute(text(stmt))

    async def close(self) -> None:
        await self._engine.dispose()

    async def upsert_comments(self, comments: list[Comment]) -> list[Comment]:
        if not comments:
            return []

        values = [
            {
                "id": c.id,
                "source": c.source,
                "text": c.text,
                "score": c.score,
                "author": c.author,
                "author_id": c.author_id,
                "author_avatar": c.author_avatar,
                "post_title": c.post_title,
                "post_url": c.post_url,
            }
            for c in comments
        ]

        async with self._session_factory() as session:
            existing = set(
                (
                    await session.execute(
                        select(CommentModel.id).where(CommentModel.id.in_([c.id for c in comments]))
                    )
                ).scalars()
            )
            new_ids = [c.id for c in comments if c.id not in existing]

            stmt = insert(CommentModel).values(values)
            stmt = stmt.on_conflict_do_update(
                index_elements=[CommentModel.id],
                set_={
                    "score": stmt.excluded.score,
                    "author_avatar": stmt.excluded.author_avatar,
                },
            )
            await session.execute(stmt)
            await session.commit()

        return [c for c in comments if c.id in new_ids]

    async def list_unscored(self, limit: int = 20) -> list[Comment]:
        async with self._session_factory() as session:
            models = (
                await session.execute(
                    select(CommentModel)
                    .where(CommentModel.meeseeks_score.is_(None))
                    .order_by(CommentModel.fetched_at)
                    .limit(limit)
                )
            ).scalars().all()
            return [_to_comment(m) for m in models]

    async def mark_scored(self, comment: Comment, verdict: MeeseeksVerdict) -> None:
        async with self._session_factory() as session:
            await session.execute(
                update(CommentModel)
                .where(CommentModel.id == comment.id)
                .values(
                    meeseeks_score=verdict.humor_score,
                    funny=verdict.funny,
                    wit=verdict.wit,
                    creativity=verdict.creativity,
                    cringe=verdict.cringe,
                    intelligence=verdict.intelligence,
                    adaptive_score=adaptive_score(comment, verdict),
                    reaction=verdict.reaction,
                    scored_at=func.now(),
                )
            )
            await session.commit()

    async def list_comments(self, limit: int = 20, scored_only: bool = False) -> list[dict]:
        stmt = select(CommentModel)
        if scored_only:
            stmt = stmt.where(CommentModel.meeseeks_score.isnot(None))
        stmt = stmt.order_by(CommentModel.fetched_at.desc()).limit(limit)

        async with self._session_factory() as session:
            models = (await session.execute(stmt)).scalars().all()
            return [comment_view(_to_comment(m), _to_verdict(m) if m.meeseeks_score is not None else None, m.fetched_at, m.scored_at) for m in models]

    async def leaderboard(self, limit: int = 10) -> list[dict]:
        async with self._session_factory() as session:
            rows = await self._leaderboard_rows(session, limit=limit)
            return [user_view(dict(r)) for r in rows]

    async def get_user(self, key: str) -> dict | None:
        async with self._session_factory() as session:
            rows = await self._leaderboard_rows(session, limit=1, key=key)
            return user_view(dict(rows[0])) if rows else None

    @staticmethod
    async def _leaderboard_rows(session, limit: int, key: str | None = None):
        c2 = aliased(CommentModel)
        best_reaction = (
            select(c2.reaction)
            .where(c2.author_id == CommentModel.author_id)
            .order_by(c2.meeseeks_score.desc(), c2.scored_at.desc())
            .limit(1)
            .correlate(CommentModel)
            .scalar_subquery()
        )

        stmt = (
            select(
                CommentModel.author_id.label("author_id"),
                CommentModel.author.label("username"),
                func.max(CommentModel.author_avatar).label("author_avatar"),
                func.sum(CommentModel.meeseeks_score).label("total_score"),
                func.count().label("comments_count"),
                func.round(func.avg(CommentModel.meeseeks_score), 2).label("avg_score"),
                func.max(CommentModel.meeseeks_score).label("best_score"),
                best_reaction.label("best_reaction"),
            )
            .where(CommentModel.meeseeks_score.isnot(None))
            .group_by(CommentModel.author_id, CommentModel.author)
            .order_by(desc("total_score"), desc("best_score"))
            .limit(limit)
        )

        if key:
            stmt = stmt.where(
                (CommentModel.author_id == key) | (CommentModel.author == key)
            )
        result = await session.execute(stmt)
        return result.mappings().all()
