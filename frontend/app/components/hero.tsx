"use client";

import { useEffect, useState } from "react";
import MortyAvatar from "@/app/components/morty-avatar";
import UserAvatar from "@/app/components/user-avatar";
import ScorePill from "@/app/components/score-pill";
import type { ScoredComment } from "@/lib/api";

const INTERVAL = 5000;

export default function Hero({
  comments,
  error,
}: {
  comments: ScoredComment[];
  error: string | null;
}) {
  const total = comments.length;
  const [index, setIndex] = useState(0);

  useEffect(() => {
    if (total < 2) return;
    const id = setInterval(() => setIndex((i) => (i + 1) % total), INTERVAL);
    return () => clearInterval(id);
  }, [total]);

  const broken = !!error || total === 0;

  return (
    <section className="hero">
      <div className="hero-copy">
        <div className="hero-morty" aria-hidden="true">
          <span className="hero-morty__ring" />
          <span className="hero-morty__avatar">
            <MortyAvatar size={110} />
          </span>
        </div>
        <h1 className="hero-title">
          Every comment gets the <em>Morty test</em>.
        </h1>
        <p className="hero-sub">
          The internet&apos;s funniest YouTube comments, judged in character by
          Morty. Newest verdicts first.
        </p>
      </div>

      <div className="hero-ticker">
        {broken ? (
          <div className="hero-ticker__empty">
            <div className="state-title">Ooh-wee, the backend hopped to another dimension.</div>
            <div className="state-sub">
              {error ? (
                <>
                  Can&apos;t reach the API. <code>{error}</code>
                </>
              ) : (
                "No comments scored yet."
              )}
            </div>
          </div>
        ) : (
          <>
            <div className="hero-comments">
              {comments.map((item, i) => (
                <div
                  key={item.comment.id}
                  className={`hero-comment${i === index ? " hero-comment--active" : ""}`}
                >
                  <div className="hero-comment__head">
                    <UserAvatar
                      src={item.comment.author_avatar}
                      name={item.comment.author}
                      size={26}
                    />
                    <span className="hero-comment__author">{item.comment.author}</span>
                    <span className="hero-comment__meta">{item.comment.post_title}</span>
                  </div>
                  <p className="hero-comment__text">“{item.comment.text}”</p>
                  <div className="hero-comment__morty">
                    <MortyAvatar size={28} />
                    <div className="hero-comment__morty-body">
                      <span className="hero-comment__morty-name">morty says</span>
                      <p className="hero-comment__morty-text">
                        {item.verdict?.assessment ?? "no verdict yet"}
                      </p>
                    </div>
                    <ScorePill score={item.verdict?.score ?? 0} label="grade" />
                  </div>
                </div>
              ))}
            </div>
            <div className="hero-dots">
              {comments.map((c, i) => (
                <button
                  key={c.comment.id}
                  type="button"
                  className={`hero-dot${i === index ? " hero-dot--active" : ""}`}
                  onClick={() => setIndex(i)}
                  aria-label={`Show comment ${i + 1}`}
                />
              ))}
            </div>
          </>
        )}
      </div>
    </section>
  );
}
