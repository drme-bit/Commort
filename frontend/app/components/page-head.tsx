import Reveal from "@/app/components/reveal";

export default function PageHead({
  title,
  sub,
  badge,
}: {
  title: string;
  sub: string;
  badge?: string;
}) {
  return (
    <Reveal className="page-head">
      <div>
        <h1>{title}</h1>
        <p className="sub">{sub}</p>
      </div>
      {badge ? <span className="badge">{badge}</span> : null}
    </Reveal>
  );
}
