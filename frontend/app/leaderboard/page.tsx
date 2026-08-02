import { api } from "@/lib/api";
import PageHead from "@/app/components/page-head";
import Stagger from "@/app/components/stagger";
import LeaderRow from "@/app/components/leader-row";
import { Offline, Empty } from "@/app/components/state";

export const dynamic = "force-dynamic";

export default async function LeaderboardPage() {
  const { data, error } = await api.leaderboard(25);

  return (
    <section>
      <PageHead
        title="Leaderboard"
        sub="YouTube commenters, ranked by how much Morty liked them."
        badge={data ? `${data.length} users` : undefined}
      />
      {error ? (
        <Offline baseUrl={api.baseUrl()} error={error} />
      ) : data && data.length > 0 ? (
        <Stagger className="card">
          {data.map((user, i) => (
            <LeaderRow key={user.author_id} user={user} rank={i + 1} />
          ))}
        </Stagger>
      ) : (
        <Empty hint="No comments scored yet. Hit /api/comments/score or wait for the poller." />
      )}
    </section>
  );
}
