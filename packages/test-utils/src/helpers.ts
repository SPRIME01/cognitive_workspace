/**
 * Common test helpers for the Cognitive Workspace.
 *
 * This module provides utility functions to simplify common testing tasks.
 */

/**
 * Waits for a specified amount of time.
 *
 * @param ms - The number of milliseconds to wait
 * @returns A promise that resolves after the specified time
 */
export const wait = (ms: number): Promise<void> =>
  new Promise(resolve => setTimeout(resolve, ms));

/**
 * Creates a mock response object for testing API handlers.
 *
 * @param overrides - Properties to override in the default response
 * @returns A mock response object
 */
export const createMockResponse = (overrides = {}) => ({
  status: 200,
  json: jest.fn().mockResolvedValue({}),
  send: jest.fn(),
  ...overrides
});

/**
 * Creates a mock request object for testing API handlers.
 *
 * @param overrides - Properties to override in the default request
 * @returns A mock request object
 */
export const createMockRequest = (overrides = {}) => ({
  body: {},
  params: {},
  query: {},
  headers: {},
  user: { id: 'user-1' },
  ...overrides
});
