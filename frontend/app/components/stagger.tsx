"use client";

import { useLayoutEffect, useRef } from "react";
import { staggerIn } from "@/lib/anim";

export default function Stagger({
  children,
  className = "",
}: {
  children: React.ReactNode;
  className?: string;
}) {
  const ref = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    if (!ref.current) return;
    staggerIn(Array.from(ref.current.children) as HTMLElement[]);
  }, []);

  return (
    <div ref={ref} className={className}>
      {children}
    </div>
  );
}
