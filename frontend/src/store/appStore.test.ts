import { describe, it, expect, beforeEach } from 'vitest';
import { useAppStore } from './appStore';

describe('appStore', () => {
  beforeEach(() => {
    // Reset the store before each test
    const store = useAppStore.getState();
    store.setCurrentPage('dashboard');
    store.setCrowdCount(87342);
    store.setRiskLevel('healthy');
  });

  it('should have initial state', () => {
    const store = useAppStore.getState();
    expect(store.currentPage).toBe('dashboard');
    expect(store.crowdCount).toBe(87342);
    expect(store.riskLevel).toBe('healthy');
    expect(store.isDemoRunning).toBe(false);
  });

  it('should update current page', () => {
    useAppStore.getState().setCurrentPage('brain');
    expect(useAppStore.getState().currentPage).toBe('brain');
  });

  it('should update crowd count', () => {
    useAppStore.getState().setCrowdCount(90000);
    expect(useAppStore.getState().crowdCount).toBe(90000);
  });

  it('should update risk level', () => {
    useAppStore.getState().setRiskLevel('critical');
    expect(useAppStore.getState().riskLevel).toBe('critical');
  });
});
