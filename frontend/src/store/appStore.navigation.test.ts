/**
 * Tests: appStore navigation and UI state management
 */
import { describe, it, expect, beforeEach } from 'vitest';
import { useAppStore, type Page } from './appStore';

describe('appStore — navigation', () => {
  beforeEach(() => {
    useAppStore.getState().setCurrentPage('dashboard');
    useAppStore.getState().setCommandBarOpen(false);
    useAppStore.getState().setSidebarExpanded(false);
  });

  it('navigates to all valid pages', () => {
    const pages: Page[] = [
      'dashboard', 'brain', 'twins', 'simulation',
      'future', 'analytics', 'debate', 'memory', 'reports', 'settings',
    ];
    for (const page of pages) {
      useAppStore.getState().setCurrentPage(page);
      expect(useAppStore.getState().currentPage).toBe(page);
    }
  });

  it('command bar toggles open and closed', () => {
    useAppStore.getState().setCommandBarOpen(true);
    expect(useAppStore.getState().commandBarOpen).toBe(true);
    useAppStore.getState().setCommandBarOpen(false);
    expect(useAppStore.getState().commandBarOpen).toBe(false);
  });

  it('sidebar expanded state toggles', () => {
    useAppStore.getState().setSidebarExpanded(true);
    expect(useAppStore.getState().sidebarExpanded).toBe(true);
  });

  it('selected fan id can be set and cleared', () => {
    useAppStore.getState().setSelectedFanId('F001');
    expect(useAppStore.getState().selectedFanId).toBe('F001');
    useAppStore.getState().setSelectedFanId(null);
    expect(useAppStore.getState().selectedFanId).toBeNull();
  });

  it('demo running flag toggles', () => {
    useAppStore.getState().setIsDemoRunning(true);
    expect(useAppStore.getState().isDemoRunning).toBe(true);
    useAppStore.getState().setIsDemoRunning(false);
    expect(useAppStore.getState().isDemoRunning).toBe(false);
  });
});

describe('appStore — AI brain state', () => {
  it('confidence is bounded between 0 and 100', () => {
    useAppStore.getState().setConfidence(95);
    expect(useAppStore.getState().confidence).toBe(95);
  });

  it('current thought updates', () => {
    const thought = 'Gate B approaching capacity — deploying volunteers.';
    useAppStore.getState().setCurrentThought(thought);
    expect(useAppStore.getState().currentThought).toBe(thought);
  });

  it('prediction updates', () => {
    const prediction = 'North Stand will hit 94% in 12 minutes.';
    useAppStore.getState().setCurrentPrediction(prediction);
    expect(useAppStore.getState().currentPrediction).toBe(prediction);
  });

  it('isThinking toggles correctly', () => {
    useAppStore.getState().setIsThinking(true);
    expect(useAppStore.getState().isThinking).toBe(true);
    useAppStore.getState().setIsThinking(false);
    expect(useAppStore.getState().isThinking).toBe(false);
  });
});

describe('appStore — timeline state', () => {
  it('timeline offset updates', () => {
    useAppStore.getState().setTimelineOffset(30);
    expect(useAppStore.getState().timelineOffset).toBe(30);
  });

  it('match minute can be set to any valid minute', () => {
    for (const minute of [0, 45, 67, 90]) {
      useAppStore.getState().setMatchMinute(minute);
      expect(useAppStore.getState().matchMinute).toBe(minute);
    }
  });
});
