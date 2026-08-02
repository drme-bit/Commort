import UserAvatar from "@/app/components/user-avatar";
import MortyAvatar from "@/app/components/morty-avatar";
import ScorePill from "@/app/components/score-pill";
import type { ScoredComment } from "@/lib/api";

function ytVideoId(url: string): string | null {
  try {
    const u = new URL(url);
    if (u.hostname === "youtu.be") return u.pathname.slice(1) || null;
    const v = u.searchParams.get("v");
    return v && v.length === 11 ? v : null;
  } catch {
    return null;
  }
}

function PostPreview({ url, title }: { url: string; title: string }) {
  const videoId = ytVideoId(url);
  return (
    <a className="comment-post" href={url} target="_blank" rel="noreferrer">
      <span className="comment-post__thumb">
        {videoId ? (
          <img
            src={`https://i.ytimg.com/vi/${videoId}/mqdefault.jpg`}
            alt={title || "YouTube video"}
            width={120}
            height={68}
            loading="lazy"
          />
        ) : (
          <span className="comment-post__thumb--fallback">yt</span>
        )}
      </span>
      <span className="comment-post__body">
        <span className="comment-post__label">on video</span>
        <span className="comment-post__title">{title || "YouTube"}</span>
      </span>
    </a>
  );
}

export default function CommentCard({ item }: { item: ScoredComment }) {
  const { comment, verdict } = item;

  return (
    <article className="comment-card">
      <PostPreview url={comment.post_url} title={comment.post_title} />

      <div className="comment-head">
        <UserAvatar src={comment.author_avatar} name={comment.author} size={34} />
        <div className="comment-user">
          <span className="comment-author">{comment.author}</span>
          <span className="comment-meta">
            {comment.score} likes · {new Date(item.fetched_at).toLocaleDateString()}
          </span>
        </div>
      </div>

      <p className="comment-text">{comment.text}</p>

      <div className="morty">
        <MortyAvatar size={32} />
        <div className="morty-body">
          <span className="morty-name">morty</span>
          <p className="morty-reaction">“{verdict?.assessment ?? "no verdict yet"}”</p>
        </div>
        <ScorePill score={verdict?.score ?? 0} label="grade" />
      </div>
    </article>
  );
}
