"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const links = [
  { href: "/", label: "Latest" },
  { href: "/leaderboard", label: "Leaderboard" },
];

export default function Header() {
  const pathname = usePathname();

  return (
    <header className="nav">
      <Link href="/" className="brand">
        <span className="brand-portal" />
        <span className="brand-name">commort</span>
      </Link>
      <nav className="nav-links">
        {links.map((l) => (
          <Link key={l.href} href={l.href} className={pathname === l.href ? "active" : ""}>
            {l.label}
          </Link>
        ))}
      </nav>
      <span className="nav-rip">wubba lubba dub dub</span>
    </header>
  );
}
