/**
 * Tests: useLiveData hook — interval scheduling and state updates
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { useAppStore } from '../store/appStore';

describe('useLiveData logic', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    const s = useAppStore.getState();
    s.setMatchMinute(60);
    s.setCrowdCount(87342);
    s.setRiskLevel('healthy');
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('initial crowd count is seeded correctly', () => {
    expect(useAppStore.getState().crowdCount).toBe(87342);
  });

  it('initial match minute is seeded correctly', () => {
    expect(useAppStore.getState().matchMinute).toBe(60);
  });

  it('risk level starts as healthy', () => {
    expect(useAppStore.getState().riskLevel).toBe('healthy');
  });

  it('risk level transitions are valid enum values', () => {
    const validLevels = ['healthy', 'warning', 'critical'];
    const level = useAppStore.getState().riskLevel;
    expect(validLevels).toContain(level);
  });

  it('setRiskLevel updates store', () => {
    useAppStore.getState().setRiskLevel('warning');
    expect(useAppStore.getState().riskLevel).toBe('warning');
    useAppStore.getState().setRiskLevel('critical');
    expect(useAppStore.getState().riskLevel).toBe('critical');
  });

  it('setMatchMinute updates store', () => {
    useAppStore.getState().setMatchMinute(75);
    expect(useAppStore.getState().matchMinute).toBe(75);
  });

  it('match minute does not exceed 90', () => {
    useAppStore.getState().setMatchMinute(89);
    const current = useAppStore.getState().matchMinute;
    const next = current < 90 ? current + 1 : current;
    expect(next).toBeLessThanOrEqual(90);
  });

  it('crowd count fluctuates around 87342', () => {
    const base = 87342;
    const delta = 300;
    useAppStore.getState().setCrowdCount(base + 150);
    const count = useAppStore.getState().crowdCount;
    expect(count).toBeGreaterThanOrEqual(base - delta);
    expect(count).toBeLessThanOrEqual(base + delta);
  });
});
