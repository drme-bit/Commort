import UserAvatar from "@/app/components/user-avatar";
import MortyAvatar from "@/app/components/morty-avatar";
import ScorePill from "@/app/components/score-pill";
import type { ScoredComment } from "@/lib/api";

export default function CommentCard({ item }: { item: ScoredComment }) {
  const { comment, verdict } = item;

  return (
    <div className="row comment-card">
      <UserAvatar src={comment.author_avatar} name={comment.author} size={38} />
      <div className="main">
        <div className="comment-head">
          <span className="comment-author">{comment.author}</span>
          <span className="comment-meta">
            <a href={comment.post_url} target="_blank" rel="noreferrer">
              {comment.post_title}
            </a>
          </span>
          <ScorePill score={comment.score} label="likes" />
        </div>
        <p className="comment-text">{comment.text}</p>
        <div className="morty">
          <MortyAvatar size={30} />
          <div className="morty-body">
            <span className="morty-name">morty</span>
            <p className="morty-reaction">{verdict.assessment}</p>
          </div>
          <ScorePill score={verdict.score} label="grade" />
        </div>
      </div>
    </div>
  );
}
