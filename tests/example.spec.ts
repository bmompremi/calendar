import { test, expect } from '@playwright/test';

test.describe('Calendar Application', () => {
  test('has title', async ({ page }) => {
    await page.goto('/');

    // Expect a title "to contain" a substring.
    await expect(page).toHaveTitle(/Calendar/);
  });

  test('basic navigation', async ({ page }) => {
    await page.goto('/');

    // Example: Check if the page loaded successfully
    expect(page.url()).toContain('localhost');
  });
});
