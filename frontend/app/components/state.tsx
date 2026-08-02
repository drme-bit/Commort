export function Offline({ baseUrl, error }: { baseUrl: string; error: string }) {
  return (
    <div className="state">
      <div className="state-title">Ooh-wee, the backend hopped to another dimension.</div>
      <div className="state-sub">
        Can&apos;t reach <code>{baseUrl}</code>. {error}
      </div>
    </div>
  );
}

export function Empty({ hint }: { hint: string }) {
  return (
    <div className="state">
      <div className="state-title">Nobody&apos;s been judged yet.</div>
      <div className="state-sub">{hint}</div>
    </div>
  );
}
