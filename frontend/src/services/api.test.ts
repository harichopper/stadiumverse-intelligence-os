/**
 * Tests: API Service layer — type contracts and interface validation
 */
import { describe, it, expect } from 'vitest';
import type {
  Fan, VolunteerData, CrowdSnap,
  AIDecisionData, StadiumEventData, DashboardData,
} from './api';

describe('API Type Contracts', () => {
  it('Fan interface has all required fields', () => {
    const fan: Fan = {
      id: 'uuid-1',
      fan_id: 'F001',
      name: 'Carlos M.',
      country: 'BRA',
      flag: '🇧🇷',
      language: 'pt',
      age: 28,
      sector: 'N1',
      current_emotion: 'excited',
      stress_level: 30,
      excitement_level: 85,
      hunger_level: 25,
      fatigue_level: 10,
      loc_x: 50.0,
      loc_y: 48.0,
      prediction_confidence: 0.88,
      risk_score: 12,
    };
    expect(fan.fan_id).toBe('F001');
    expect(fan.country).toBe('BRA');
    expect(fan.stress_level).toBeGreaterThanOrEqual(0);
    expect(fan.stress_level).toBeLessThanOrEqual(100);
  });

  it('CrowdSnap interface has gate_densities map', () => {
    const snap: CrowdSnap = {
      id: 'snap-1',
      timestamp: '2026-07-07T10:00:00',
      total_fans: 87342,
      avg_stress: 45.0,
      avg_excitement: 65.0,
      risk_level: 'healthy',
      gate_densities: { A: 72, B: 94, C: 68, D: 61 },
      queue_avg_min: 5.5,
      weather: { temp: 22.0, rain_pct: 18.0 },
    };
    expect(snap.total_fans).toBe(87342);
    expect(snap.gate_densities['B']).toBe(94);
    expect(['healthy', 'warning', 'critical']).toContain(snap.risk_level);
  });

  it('AIDecisionData interface has required fields', () => {
    const decision: AIDecisionData = {
      id: 'dec-1',
      timestamp: '2026-07-07T10:00:00',
      match_minute: 67,
      agent: 'Coordinator',
      decision: 'Deploy 3 volunteers to Gate B',
      confidence: 0.94,
      outcome: 'SUCCESS',
      affected_fans: 1400,
      impact_pct: 23.0,
    };
    expect(decision.outcome).toBe('SUCCESS');
    expect(decision.confidence).toBeGreaterThan(0);
    expect(decision.confidence).toBeLessThanOrEqual(1);
  });

  it('DashboardData aggregates all sub-types', () => {
    const dashboard: DashboardData = {
      crowd: {
        id: 'snap-1', timestamp: '2026-07-07T10:00:00',
        total_fans: 87342, avg_stress: 50, avg_excitement: 60,
        risk_level: 'healthy', gate_densities: {},
        queue_avg_min: 5, weather: { temp: 22, rain_pct: 10 },
      },
      fans_online: 10,
      volunteers_available: 6,
      recent_decisions: [],
      recent_events: [],
      timestamp: '2026-07-07T10:00:00',
    };
    expect(dashboard.fans_online).toBe(10);
    expect(dashboard.recent_decisions).toBeInstanceOf(Array);
  });

  it('StadiumEventData severity is 1–5', () => {
    const event: StadiumEventData = {
      id: 'evt-1',
      timestamp: '2026-07-07T10:00:00',
      event_type: 'crowd',
      title: 'Gate B congestion',
      severity: 3,
      resolved: false,
    };
    expect(event.severity).toBeGreaterThanOrEqual(1);
    expect(event.severity).toBeLessThanOrEqual(5);
  });

  it('VolunteerData languages is an array', () => {
    const vol: VolunteerData = {
      id: 'vol-1',
      volunteer_id: 'V001',
      name: 'Alice',
      languages: ['en', 'ar'],
      skills: ['crowd_control'],
      medical_training: false,
      availability: 'available',
      loc_x: 50,
      loc_y: 50,
      tasks_today: 0,
    };
    expect(Array.isArray(vol.languages)).toBe(true);
    expect(vol.availability).toBe('available');
  });
});
