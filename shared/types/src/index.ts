/**
 * Core types for the Cognitive Workspace application.
 */

export interface User {
  id: string;
  email: string;
  name: string | null;
  isActive: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Workspace {
  id: string;
  name: string;
  description: string | null;
  ownerId: string;
  isPublic: boolean;
  createdAt: string;
  updatedAt: string;
}

export interface Document {
  id: string;
  title: string;
  content: string;
  workspaceId: string;
  createdById: string;
  tags: string[];
  createdAt: string;
  updatedAt: string;
}

export interface Tag {
  id: string;
  name: string;
  color: string | null;
  workspaceId: string;
}

export interface WorkspacePermission {
  userId: string;
  workspaceId: string;
  role: 'owner' | 'editor' | 'viewer';
}

export interface ApiResponse<T> {
  data: T;
  success: boolean;
  message?: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

export type ApiError = {
  message: string;
  statusCode: number;
  errors?: Record<string, string[]>;
};
