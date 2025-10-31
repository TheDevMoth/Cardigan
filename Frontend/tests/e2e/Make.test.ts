import { test, expect } from '@playwright/test';

test.beforeEach(async ({ page }) => {
  await page.goto('/make');
  page.locator('.nav-start > .vr').evaluate
})

// Helper to get class list of an element
const getClassList = async (page, selector: string) => {
  return await page.locator(selector).evaluate(el => [...el.classList])
}

test.describe('Navbar Layout Tests', () => { 
  // Large Screen Test (1250px)
  test('Navbar layout on large screens (1250px)', async ({ page }) => {
    await page.setViewportSize({ width: 1250, height: 800 })

    const navContainer = page.locator('.nav-container')
    await expect(navContainer).toBeVisible()

    const height = await navContainer.evaluate(el => el.clientHeight)
    expect(height).toBeLessThan(50)

    expect(await getClassList(page, '.nav-container')).not.toContain('stacked-layout')
    expect(await getClassList(page, '.nav-start > .vr')).not.toContain('hidden-nav')
    expect(await getClassList(page, '.navbar-nav')).not.toContain('hidden-nav')
  })

  // Medium Screen Test (1000px)
  test('Navbar layout on medium screens (1000px)', async ({ page }) => {
    await page.setViewportSize({ width: 1000, height: 800 })

    const navContainer = page.locator('.nav-container')
    await expect(navContainer).toBeVisible()

    const height = await navContainer.evaluate(el => el.clientHeight)
    expect(height).toBeGreaterThan(50)
    expect(height).toBeLessThan(100)

    expect(await getClassList(page, '.nav-container')).toContain('stacked-layout')
    expect(await getClassList(page, '.nav-start > .vr')).not.toContain('hidden-nav')
    expect(await getClassList(page, '.navbar-nav')).not.toContain('hidden-nav')
  })

  // Small Screen Test (500px)
  test('Navbar layout on small screens (500px)', async ({ page }) => {
    await page.setViewportSize({ width: 500, height: 800 })

    const navContainer = page.locator('.nav-container')
    await expect(navContainer).toBeVisible()

    const height = await navContainer.evaluate(el => el.clientHeight)
    expect(height).toBeGreaterThan(50)
    expect(height).toBeLessThan(100)

    expect(await getClassList(page, '.nav-container')).toContain('stacked-layout')
    expect(await getClassList(page, '.nav-start > .vr')).toContain('hidden-nav')
    expect(await getClassList(page, '.navbar-nav')).toContain('hidden-nav')
  })

})
