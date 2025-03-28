/**
 * Mock data generators for testing purposes.
 *
 * This module provides functions to generate consistent mock data
 * for testing across all packages in the monorepo.
 */

/**
 * Creates a mock user with the specified properties.
 *
 * @param overrides - Properties to override in the default user
 * @returns A mock user object
 */
export const createMockUser = (overrides = {}) => ({
  id: 'user-1',
  username: 'testuser',
  email: 'test@example.com',
  name: 'Test User',
  createdAt: new Date().toISOString(),
  ...overrides
});

/**
 * Creates a mock workspace with the specified properties.
 *
 * @param overrides - Properties to override in the default workspace
 * @returns A mock workspace object
 */
export const createMockWorkspace = (overrides = {}) => ({
  id: 'workspace-1',
  name: 'Test Workspace',
  description: 'A test workspace',
  ownerId: 'user-1',
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  ...overrides
});

/**
 * Creates a mock artifact with the specified properties.
 *
 * @param overrides - Properties to override in the default artifact
 * @returns A mock artifact object
 */
export const createMockArtifact = (overrides = {}) => ({
  id: 'artifact-1',
  type: 'note',
  content: 'Test content',
  workspaceId: 'workspace-1',
  createdAt: new Date().toISOString(),
  updatedAt: new Date().toISOString(),
  ...overrides
});
