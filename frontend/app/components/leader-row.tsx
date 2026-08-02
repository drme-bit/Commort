import UserAvatar from "@/app/components/user-avatar";
import type { UserRow } from "@/lib/api";

export default function LeaderRow({ user, rank }: { user: UserRow; rank: number }) {
  return (
    <div className="row leader-row">
      <span className={`rank${rank <= 3 ? " rank--top" : ""}`}>{rank}</span>
      <UserAvatar src={user.author_avatar} name={user.username} />
      <div className="main">
        <div className="name">{user.username}</div>
        {user.best_assessment ? (
          <div className="reaction">“{user.best_assessment}”</div>
        ) : (
          <div className="reaction">no verdict yet</div>
        )}
      </div>
      <span className="count">{user.comments_count} com</span>
      <span className="score">{user.total_score}</span>
    </div>
  );
}
