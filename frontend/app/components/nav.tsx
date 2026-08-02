"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/", label: "Leaderboard" },
  { href: "/comments", label: "Comments" },
];

export default function Nav() {
  const pathname = usePathname();
  return (
    <header className="nav">
      <div className="brand">
        <span className="brand-dot" />
        commort
      </div>
      <nav className="nav-links">
        {links.map((l) => (
          <Link key={l.href} href={l.href} className={pathname === l.href ? "active" : ""}>
            {l.label}
          </Link>
        ))}
      </nav>
    </header>
  );
}
