/**
 * Mock Service Worker (MSW) setup for API mocking in tests.
 *
 * This module provides a consistent way to mock API requests across all packages.
 */
import { setupServer } from 'msw/node';
import { rest } from 'msw';

// Base URL for API requests
export const API_BASE_URL = 'http://localhost:8000/api';

/**
 * Default API handlers that can be used in tests.
 * These provide basic mocks for common API endpoints.
 */
export const defaultHandlers = [
  // User authentication
  rest.post(`${API_BASE_URL}/auth/login`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        token: 'mock-jwt-token',
        user: {
          id: 'user-1',
          username: 'testuser',
          email: 'test@example.com'
        }
      })
    );
  }),

  // Users API
  rest.get(`${API_BASE_URL}/users/:userId`, (req, res, ctx) => {
    const { userId } = req.params;
    return res(
      ctx.status(200),
      ctx.json({
        id: userId,
        username: 'testuser',
        email: 'test@example.com',
        name: 'Test User'
      })
    );
  }),

  // Workspaces API
  rest.get(`${API_BASE_URL}/workspaces`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        workspaces: [
          {
            id: 'workspace-1',
            name: 'Test Workspace',
            description: 'A test workspace',
            ownerId: 'user-1'
          }
        ]
      })
    );
  }),

  // Artifacts API
  rest.get(`${API_BASE_URL}/workspaces/:workspaceId/artifacts`, (req, res, ctx) => {
    return res(
      ctx.status(200),
      ctx.json({
        artifacts: [
          {
            id: 'artifact-1',
            type: 'note',
            content: 'Test content',
            workspaceId: req.params.workspaceId
          }
        ]
      })
    );
  })
];

/**
 * Creates an MSW server with the provided handlers.
 *
 * @param handlers - Additional API handlers to include
 * @returns An MSW server instance
 */
export const createTestServer = (handlers = []) => {
  return setupServer(...defaultHandlers, ...handlers);
};

/**
 * A convenience function to create a test server with the default handlers.
 */
export const server = createTestServer();
