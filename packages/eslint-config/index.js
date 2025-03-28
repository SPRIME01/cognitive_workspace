/**
 * Main ESLint configuration entry point.
 *
 * This file exports the main ESLint configuration that can be extended
 * by other packages in the monorepo.
 */

module.exports = {
  extends: [
    './base',
    './typescript',
  ].map(require.resolve),
};
