import { api } from "@/lib/api";
import PageHead from "@/app/components/page-head";
import Stagger from "@/app/components/stagger";
import CommentCard from "@/app/components/comment-card";
import { Offline, Empty } from "@/app/components/state";

export const dynamic = "force-dynamic";

export default async function CommentsPage() {
  const { data, error } = await api.comments(50);

  return (
    <section>
      <PageHead
        title="Comments"
        sub="What Morty has to say about the internet today."
        badge={data ? `${data.length} scored` : undefined}
      />
      {error ? (
        <Offline baseUrl={api.baseUrl()} error={error} />
      ) : data && data.length > 0 ? (
        <Stagger className="card">
          {data.map((item) => (
            <CommentCard key={item.comment.id} item={item} />
          ))}
        </Stagger>
      ) : (
        <Empty hint="No comments scored yet. Hit /api/comments/score or wait for the poller." />
      )}
    </section>
  );
}
