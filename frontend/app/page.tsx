import { api } from "@/lib/api";
import Hero from "@/app/components/hero";
import PageHead from "@/app/components/page-head";
import Stagger from "@/app/components/stagger";
import CommentCard from "@/app/components/comment-card";
import { Offline, Empty } from "@/app/components/state";

export const dynamic = "force-dynamic";

export default async function HomePage() {
  const { data, error } = await api.comments(30);

  return (
    <section>
      <Hero comments={data?.slice(0, 6) ?? []} error={error} />

      <PageHead
        title="Latest comments"
        sub="What Morty just watched and judged."
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
