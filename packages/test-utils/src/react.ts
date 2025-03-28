/**
 * React testing utilities for the Cognitive Workspace.
 */
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { renderHook } from '@testing-library/react-hooks';
import userEvent from '@testing-library/user-event';

/**
 * Custom render function with common providers
 *
 * @param ui - The React component to render
 * @param options - Additional render options
 * @returns The render result
 */
const customRender = (ui: React.ReactElement, options = {}) => {
  // You can add providers here, such as ThemeProvider, AuthProvider, etc.
  return render(ui, { ...options });
};

// Re-export everything
export * from '@testing-library/react';
export * from '@testing-library/react-hooks';
export * from '@testing-library/user-event';

// Override render method
export { customRender as render };
