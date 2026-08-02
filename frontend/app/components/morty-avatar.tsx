export default function MortyAvatar({ size = 30 }: { size?: number }) {
  return (
    <svg
      className="morty-avatar"
      width={size}
      height={size}
      viewBox="0 0 64 64"
      role="img"
      aria-label="Morty"
    >
      <ellipse cx="32" cy="35" rx="17" ry="20" fill="#f2cfae" />
      <path d="M15 29c0-14 8-20 17-18 9-2 17 4 17 18-3-8-8-12-17-12-9 0-14 4-17 12z" fill="#5f4326" />
      <path d="M16 27c4-6 9-9 16-9s12 3 16 9c-2-10-8-16-16-16S18 17 16 27z" fill="#7a5533" />
      <circle cx="24" cy="34" r="4.5" fill="#141414" />
      <circle cx="26.5" cy="32.2" r="1.4" fill="#fff" />
      <circle cx="40" cy="34" r="4.5" fill="#141414" />
      <circle cx="42.5" cy="32.2" r="1.4" fill="#fff" />
      <path d="M19.5 27.5L27 29.5" stroke="#7a5533" strokeWidth="2" strokeLinecap="round" />
      <path d="M44.5 27.5L37 29.5" stroke="#7a5533" strokeWidth="2" strokeLinecap="round" />
      <path d="M27.5 42.5c3 2 6 2 9 0" stroke="#7a4a30" strokeWidth="2" fill="none" strokeLinecap="round" />
      <path d="M14 52c6-4 11-4 18 1l0 11H14z" fill="#3e9ef0" />
      <path d="M32 53c7-5 12-5 18-1v11H32z" fill="#2f7fd0" />
      <path d="M28 52c2 2 6 2 8 0" stroke="#d8f0ff" strokeWidth="2.5" fill="none" strokeLinecap="round" />
    </svg>
  );
}
