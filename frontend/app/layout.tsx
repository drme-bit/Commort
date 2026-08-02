import type { Metadata } from "next";
import { Bangers } from "next/font/google";
import "./globals.css";
import Header from "@/app/components/header";
import PortalBg from "@/app/components/portal-bg";
import LenisProvider from "@/app/components/lenis-provider";

const bangers = Bangers({
  weight: "400",
  subsets: ["latin"],
  variable: "--font-bangers",
  display: "swap",
});

export const metadata: Metadata = {
  title: "commort — Morty picks the funniest comments",
  description: "YouTube comments, judged by Morty from Rick and Morty.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={bangers.variable}>
        <LenisProvider>
          <PortalBg />
          <Header />
          <main className="container">{children}</main>
        </LenisProvider>
      </body>
    </html>
  );
}
