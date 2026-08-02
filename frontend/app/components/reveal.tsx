"use client";

import { useLayoutEffect, useRef } from "react";
import { revealIn } from "@/lib/anim";

export default function Reveal({
  children,
  className = "",
  delay = 0,
}: {
  children: React.ReactNode;
  className?: string;
  delay?: number;
}) {
  const ref = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    if (ref.current) revealIn(ref.current, { delay });
  }, [delay]);

  return (
    <div ref={ref} className={className}>
      {children}
    </div>
  );
}
