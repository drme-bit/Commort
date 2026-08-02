export default function ScorePill({ score, label }: { score: number; label?: string }) {
  const hi = score >= 7;
  return (
    <span className={`score-pill${hi ? " score-pill--hi" : ""}`}>
      {label ? <span className="score-pill__label">{label}</span> : null}
      {score}
    </span>
  );
}
