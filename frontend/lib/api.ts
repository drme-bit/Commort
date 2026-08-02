const API = process.env.COMMORT_API_URL ?? "http://localhost:8000";

export interface Comment {
  id: string;
  source: string;
  text: string;
  score: number;
  author: string;
  author_id: string;
  author_avatar: string;
  post_title: string;
  post_url: string;
}

export interface Verdict {
  score: number;
  assessment: string;
  adaptive_score: number;
}

export interface ScoredComment {
  comment: Comment;
  verdict: Verdict;
  fetched_at: string;
  scored_at: string | null;
}

export interface UserRow {
  author_id: string;
  username: string;
  author_avatar: string;
  total_score: number;
  comments_count: number;
  avg_score: number;
  best_score: number;
  best_assessment: string | null;
  last_seen: string | null;
}

export interface ApiResult<T> {
  data: T | null;
  error: string | null;
}

async function get<T>(path: string): Promise<ApiResult<T>> {
  try {
    const res = await fetch(`${API}${path}`, {
      cache: "no-store",
      signal: AbortSignal.timeout(5000),
    });
    if (!res.ok) throw new Error(`API ${path}: HTTP ${res.status}`);
    return { data: (await res.json()) as T, error: null };
  } catch (err) {
    return { data: null, error: err instanceof Error ? err.message : String(err) };
  }
}

export const api = {
  baseUrl: () => API,
  leaderboard: (limit = 25) => get<UserRow[]>(`/api/users?limit=${limit}`),
  comments: (limit = 50) => get<ScoredComment[]>(`/api/comments?limit=${limit}&scored_only=true`),
};
