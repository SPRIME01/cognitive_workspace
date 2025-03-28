/**
 * Jest setup file that runs before tests.
 *
 * This file sets up the testing environment with common configurations
 * like mocks and cleanup for all tests.
 */

import '@testing-library/jest-dom';
import { server } from './msw';

// Establish API mocking before all tests
beforeAll(() => server.listen({ onUnhandledRequest: 'warn' }));

// Reset any request handlers that we may add during tests
afterEach(() => server.resetHandlers());

// Clean up after all tests are done
afterAll(() => server.close());
