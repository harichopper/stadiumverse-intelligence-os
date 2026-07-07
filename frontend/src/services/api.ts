/**
 * StadiumVerse Intelligence OS — API Service
 * Talks to FastAPI backend at localhost:8000
 */

const BASE = '/api/stadium';   // proxied by Vite to localhost:8000

async function get<T>(path: string): Promise<T> {
  const r = await fetch(`${BASE}${path}`);
  if (!r.ok) throw new Error(`API ${path} → ${r.status}`);
  return r.json() as Promise<T>;
}

async function post<T>(path: string, body?: Record<string,unknown>): Promise<T> {
  const r = await fetch(`${BASE}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  });
  if (!r.ok) throw new Error(`API POST ${path} → ${r.status}`);
  return r.json() as Promise<T>;
}

// ── Types ────────────────────────────────────────────────────────────────────
export interface Fan {
  id: string; fan_id: string; name: string;
  country: string; flag: string; language: string; age: number;
  favorite_team?: string; sector: string; seat?: string;
  current_emotion: string; stress_level: number; excitement_level: number;
  hunger_level: number; fatigue_level: number;
  loc_x: number; loc_y: number;
  current_thought?: string; memory_summary?: string;
  predicted_action?: string; prediction_confidence: number; risk_score: number;
  updated_at?: string;
}

export interface VolunteerData {
  id: string; volunteer_id: string; name: string;
  languages: string[]; skills: string[]; medical_training: boolean;
  availability: string; zone_assignment?: string;
  loc_x: number; loc_y: number; tasks_today: number;
}

export interface CrowdSnap {
  id: string; timestamp: string; total_fans: number;
  avg_stress: number; avg_excitement: number; risk_level: string;
  gate_densities: Record<string,number>;
  queue_avg_min: number;
  weather: { temp: number; rain_pct: number };
}

export interface AIDecisionData {
  id: string; timestamp: string; match_minute: number;
  agent: string; decision: string; reasoning?: string;
  confidence: number; outcome: string;
  affected_fans: number; impact_pct: number;
}

export interface StadiumEventData {
  id: string; timestamp: string; event_type: string;
  title: string; description?: string; severity: number; zone?: string; resolved: boolean;
}

export interface DashboardData {
  crowd: CrowdSnap;
  fans_online: number;
  volunteers_available: number;
  recent_decisions: AIDecisionData[];
  recent_events: StadiumEventData[];
  timestamp: string;
}

// ── API calls ─────────────────────────────────────────────────────────────────
export const api = {
  // Dashboard
  dashboard:       () => get<DashboardData>('/dashboard'),
  newSnapshot:     () => post<CrowdSnap>('/crowd/snapshot'),

  // Fans
  fans:            (limit = 50) => get<{ fans: Fan[]; total: number }>(`/fans?limit=${limit}`),
  fan:             (id: string) => get<Fan>(`/fans/${id}`),

  // Volunteers
  volunteers:      (availableOnly = false) =>
    get<{ volunteers: VolunteerData[]; total: number }>(
      `/volunteers${availableOnly ? '?available_only=true' : ''}`
    ),
  deployVolunteer: (id: string, zone: string) =>
    post<VolunteerData>(`/volunteers/${id}/deploy?zone=${encodeURIComponent(zone)}`),

  // Crowd history (for charts)
  crowdHistory:    (minutes = 90) => get<{ snapshots: CrowdSnap[] }>(`/crowd/history?minutes=${minutes}`),

  // AI decisions (Black Box)
  decisions:       (limit = 20) => get<{ decisions: AIDecisionData[] }>(`/decisions?limit=${limit}`),

  // Events
  events:          (limit = 30) => get<{ events: StadiumEventData[] }>(`/events?limit=${limit}`),
};
