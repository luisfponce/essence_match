import { describe, expect, it } from 'vitest';

import { homeHeadline } from './home-page';

describe('HomePage', () => {
  it('uses the generated project name', () => {
    expect(homeHeadline).toBe('EssenceMatch');
  });

  it('exposes the recommendation entry point copy', () => {
    expect(homeHeadline).toMatch(/Essence/);
  });
});
