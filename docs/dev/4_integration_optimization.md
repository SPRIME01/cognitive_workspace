# Integration and Optimization Prompts

This section contains sequential prompts for integrating components and optimizing the Cognitive Workspace application, including cross-component integration, performance optimization, and security enhancements.

## Cross-Component Integration

### System-Wide Integration

#### Step 1: Implement Event-Driven Communication

**Prompt for Test**:
> Create tests for the Event-Driven Communication system. Develop test cases that verify events can be published, routed, and consumed across different components of the application. Test various event types, including domain events, integration events, and system events. Include tests for event serialization/deserialization, routing patterns, and delivery guarantees. Test error handling, retry mechanisms, and dead-letter queues. Verify that components can properly react to events from other components.

**Prompt for Implementation**:
> Implement an Event-Driven Communication system using RabbitMQ that enables loosely coupled integration between components. Create an event bus that supports publishing, routing, and consuming events across different services. Define a common event schema that includes event type, timestamp, source, payload, and metadata. Implement event serialization/deserialization using a format like JSON or Protocol Buffers. Develop routing patterns for different event types, including direct routing, topic-based routing, and broadcast. Implement delivery guarantees appropriate for different event types, such as at-least-once delivery for critical events. Add error handling, retry mechanisms, and dead-letter queues for handling failed event processing. Create event handlers in each service that react to relevant events from other services. Ensure the system follows the Ports and Adapters architecture with clear interfaces for event publishing and consumption.

**Prompt for Refactoring/Optimization**:
> Enhance the Event-Driven Communication system with more sophisticated event handling capabilities. Implement event versioning to support backward compatibility as event schemas evolve. Add support for event correlation to track related events across services. Implement event sourcing patterns for critical workflows that need complete history. Enhance the routing system with dynamic routing rules based on event content and system state. Add comprehensive monitoring and tracing for event flows across the system. Implement rate limiting and back pressure mechanisms to prevent event flooding during high load.

**Expected Outcome**:
> A robust Event-Driven Communication system that enables loosely coupled integration between components. The implementation should support various event types and routing patterns, provide reliable delivery, and handle error conditions, creating a foundation for system-wide integration.

#### Step 2: Implement GraphQL API Layer

**Prompt for Test**:
> Develop tests for the GraphQL API Layer. Create test cases that verify the API can handle queries and mutations for all major entities and operations in the system. Test complex queries that retrieve data from multiple services, including nested relationships and filtered collections. Include tests for schema validation, error handling, authentication, and authorization. Test performance with large result sets and complex query patterns. Verify that the API correctly integrates with all backend services.

**Prompt for Implementation**:
> Implement a GraphQL API Layer that provides a unified interface for frontend-backend communication. Create a GraphQL schema that defines types, queries, mutations, and subscriptions for all major entities and operations in the system. Implement resolvers that map GraphQL operations to the appropriate service calls. Develop a data loader pattern to efficiently batch and cache service requests, preventing N+1 query problems. Add authentication and authorization middleware that validates user permissions for each operation. Implement error handling that provides meaningful error messages while protecting sensitive information. Create a schema stitching mechanism that combines schemas from different services into a unified API. Ensure the implementation follows the Ports and Adapters architecture with clear interfaces to backend services. Use FastAPI with a GraphQL library like Strawberry or Ariadne for the implementation.

**Prompt for Refactoring/Optimization**:
> Enhance the GraphQL API Layer with more sophisticated query handling and performance optimizations. Implement query complexity analysis to prevent resource-intensive queries. Add query depth limiting to prevent deeply nested queries that could impact performance. Implement result pagination for large collections using cursor-based pagination. Add field-level caching for frequently accessed data. Enhance the error handling with more detailed error codes and recovery suggestions. Implement real-time subscriptions using WebSockets for live updates. Add comprehensive API documentation with examples and schema introspection.

**Expected Outcome**:
> A powerful GraphQL API Layer that provides a unified interface for frontend-backend communication. The implementation should support complex queries and mutations, handle authentication and authorization, and optimize performance, creating a flexible and efficient API for the frontend.

#### Step 3: Implement End-to-End Workflows

**Prompt for Test**:
> Create tests for the End-to-End Workflows. Develop test cases that verify complete user journeys across multiple components of the system. Test workflows like conversation to artifact creation, artifact transformation, agent execution, and knowledge extraction. Include tests for workflow state management, error recovery, and completion tracking. Test integration points between different services involved in each workflow. Verify that workflows handle edge cases and error conditions gracefully.

**Prompt for Implementation**:
> Implement End-to-End Workflows that coordinate complex user journeys across multiple components. Create workflow orchestrators for key processes like conversation to artifact creation, artifact transformation, agent execution, and knowledge extraction. Implement state management for tracking workflow progress and handling pauses or interruptions. Develop error recovery mechanisms that can handle failures at different stages of a workflow. Create completion tracking that notifies users of workflow status and results. Implement integration with all relevant services using the Event-Driven Communication system and direct service calls as appropriate. Ensure the workflows follow the sequence diagrams and flowcharts defined in the project documentation. Use a combination of event-driven communication and orchestration patterns appropriate for each workflow.

**Prompt for Refactoring/Optimization**:
> Enhance the End-to-End Workflows with more sophisticated orchestration and monitoring capabilities. Implement a workflow engine that can handle complex workflow definitions with conditional branches, parallel execution, and dynamic routing. Add support for long-running workflows with persistence and resumption. Implement workflow versioning to handle changes in workflow definitions. Add comprehensive monitoring and visualization of workflow execution. Enhance error recovery with more sophisticated strategies like compensation transactions and saga patterns. Implement workflow analytics to track performance metrics and identify optimization opportunities.

**Expected Outcome**:
> Robust End-to-End Workflows that effectively coordinate complex user journeys across multiple components. The implementation should handle state management, error recovery, and completion tracking, creating seamless user experiences for key processes in the application.

### Frontend-Backend Integration

#### Step 1: Implement React Query Integration

**Prompt for Test**:
> Develop tests for the React Query integration with the GraphQL API. Create test cases that verify data fetching, caching, and state management for various entity types and operations. Test query invalidation, refetching, and optimistic updates. Include tests for error handling, loading states, and pagination. Test performance with large result sets and complex query patterns. Verify that the integration correctly handles authentication and authorization.

**Prompt for Implementation**:
> Implement React Query integration with the GraphQL API for efficient data fetching and state management in the frontend. Create custom hooks for common queries and mutations using React Query and a GraphQL client like Apollo or urql. Implement query configuration for caching, stale time, and refetch policies appropriate for different data types. Develop optimistic update patterns for mutations to provide immediate feedback to users. Add error handling that provides meaningful error messages and recovery options. Implement pagination for large collections using cursor-based pagination. Create a type-safe approach using TypeScript with generated types from the GraphQL schema. Ensure the implementation follows best practices for React and TypeScript, including proper separation of concerns and component composition.

**Prompt for Refactoring/Optimization**:
> Enhance the React Query integration with more sophisticated data management and performance optimizations. Implement a more advanced caching strategy with selective invalidation based on entity relationships. Add support for real-time updates using GraphQL subscriptions. Implement prefetching for anticipated user actions to improve perceived performance. Enhance error handling with automatic retry for transient errors and fallback UI for critical failures. Add offline support with local persistence and synchronization. Implement analytics tracking for query performance and error rates. Create a more comprehensive type system with runtime validation using libraries like Zod or io-ts.

**Expected Outcome**:
> An efficient React Query integration with the GraphQL API that provides robust data fetching and state management in the frontend. The implementation should handle caching, optimistic updates, error handling, and pagination, creating a responsive and reliable user experience.

#### Step 2: Implement Real-Time Collaboration Features

**Prompt for Test**:
> Create tests for the Real-Time Collaboration features. Develop test cases that verify multiple users can simultaneously view and edit artifacts with proper synchronization. Test presence awareness, cursor tracking, and edit conflict resolution. Include tests for offline editing and synchronization upon reconnection. Test performance with multiple concurrent users and frequent updates. Verify that the features handle network interruptions and reconnections gracefully.

**Prompt for Implementation**:
> Implement Real-Time Collaboration features that enable multiple users to simultaneously work on artifacts. Create a real-time synchronization system using WebSockets or a similar technology for immediate updates across clients. Implement operational transformation or conflict-free replicated data types (CRDTs) for handling concurrent edits without conflicts. Develop presence awareness that shows which users are currently viewing or editing an artifact. Add cursor tracking to display user positions within the artifact. Implement edit locking for sections or fields to prevent simultaneous editing of the same content. Create a change history that tracks who made what changes and when. Add offline editing support with synchronization upon reconnection. Ensure the implementation integrates with the Artifact service and Version Control system.

**Prompt for Refactoring/Optimization**:
> Enhance the Real-Time Collaboration features with more sophisticated collaboration capabilities. Implement a more efficient synchronization protocol that reduces network traffic and improves scalability. Add support for selective subscription to changes based on user focus and interests. Implement more advanced conflict resolution strategies for complex content types. Enhance presence awareness with user status and activity indicators. Add commenting and annotation capabilities tied to specific content sections. Implement collaboration analytics to track usage patterns and identify collaboration bottlenecks. Add support for collaboration permissions that can restrict who can edit different parts of an artifact.

**Expected Outcome**:
> Powerful Real-Time Collaboration features that enable multiple users to simultaneously work on artifacts. The implementation should handle synchronization, presence awareness, conflict resolution, and offline editing, creating a seamless collaborative experience for users.

#### Step 3: Implement Responsive UI Components

**Prompt for Test**:
> Develop tests for the Responsive UI Components. Create test cases that verify components render correctly and function properly across different screen sizes and devices. Test responsive layout adjustments, touch interactions, and accessibility features. Include tests for component composition, state management, and event handling. Test performance with complex component hierarchies and frequent updates. Verify that components correctly integrate with the data fetching layer.

**Prompt for Implementation**:
> Implement Responsive UI Components using React and Styled Components that provide a consistent and adaptive user experience across devices. Create a component library with atomic design principles, including atoms (buttons, inputs), molecules (form groups, cards), organisms (forms, lists), templates (layouts), and pages (screens). Implement responsive layouts using CSS Grid and Flexbox that adapt to different screen sizes. Develop touch-friendly interactions for mobile devices while maintaining keyboard and mouse support for desktop. Add accessibility features including semantic HTML, ARIA attributes, keyboard navigation, and screen reader support. Implement performance optimizations like code splitting, virtualized lists, and memoization. Create a theming system that supports customization and dark mode. Ensure the components follow a consistent design language and integrate with the data fetching layer using React Query.

**Prompt for Refactoring/Optimization**:
> Enhance the Responsive UI Components with more sophisticated design and performance optimizations. Implement a more advanced theming system with support for multiple themes and dynamic theme switching. Add animation and transition effects for a more polished user experience. Implement more sophisticated responsive behaviors that adapt not just to screen size but also to user preferences and context. Enhance accessibility with more comprehensive keyboard navigation and screen reader announcements. Add performance monitoring to track component render times and identify optimization opportunities. Implement storybook documentation with interactive examples and usage guidelines. Create visual regression testing to ensure consistent appearance across browsers and devices.

**Expected Outcome**:
> A comprehensive set of Responsive UI Components that provide a consistent and adaptive user experience across devices. The implementation should handle different screen sizes, support various input methods, ensure accessibility, and optimize performance, creating a polished and responsive user interface.

## Performance Optimization

### Backend Optimization

#### Step 1: Implement Database Query Optimization

**Prompt for Test**:
> Create tests for Database Query Optimization. Develop test cases that measure query performance for common database operations across different database types (PostgreSQL, MongoDB, Kuzu GraphDB). Test query execution time, resource utilization, and result set size for various query patterns. Include tests for indexing effectiveness, query plan analysis, and cache hit rates. Test performance under different load conditions and data volumes. Verify that optimizations improve performance without affecting correctness.

**Prompt for Implementation**:
> Implement Database Query Optimization for all database types used in the application. For PostgreSQL, create optimized indexes based on common query patterns, implement query optimization using EXPLAIN ANALYZE, and configure connection pooling for efficient resource utilization. For MongoDB, develop indexing strategies for frequently queried fields, implement aggregation pipeline optimization, and configure read preferences for distributed deployments. For Kuzu GraphDB, create graph-specific indexes for node and relationship properties, optimize traversal queries with path planning, and implement query caching for repeated patterns. Develop a query monitoring system that tracks slow queries and provides optimization suggestions. Implement database-specific adapters that generate optimized queries for each database type. Ensure all repositories use these optimized query patterns and monitor performance metrics.

**Prompt for Refactoring/Optimization**:
> Enhance the Database Query Optimization with more sophisticated optimization techniques. Implement query result caching using Redis or a similar caching system for frequently executed queries. Add support for database-specific features like PostgreSQL materialized views, MongoDB read-from-secondary, and Kuzu GraphDB specialized algorithms. Implement dynamic query optimization that adapts to changing data patterns and query loads. Add comprehensive query analytics that track performance trends over time. Implement automated index suggestion based on query patterns and performance metrics. Add database sharding strategies for horizontal scaling of large datasets. Implement connection management optimizations like connection pooling tuning and statement caching.

**Expected Outcome**:
> Optimized database queries that significantly improve performance for common operations across all database types. The implementation should include appropriate indexing, query optimization, connection management, and monitoring, creating a foundation for efficient data access throughout the application.

#### Step 2: Implement Caching Strategy

**Prompt for Test**:
> Develop tests for the Caching Strategy. Create test cases that verify cache effectiveness for various data types and access patterns. Test cache hit rates, invalidation timing, and memory utilization. Include tests for distributed caching, cache consistency, and cache warming. Test performance improvements with and without caching under different load conditions. Verify that caching doesn't introduce stale data or inconsistencies.

**Prompt for Implementation**:
> Implement a comprehensive Caching Strategy that improves performance for frequently accessed data. Create a multi-level caching approach with in-memory caching for hot data, distributed caching for shared data, and client-side caching for user-specific data. Implement cache management for different data types, including user profiles, artifacts, templates, conversation context, and knowledge items. Develop cache invalidation strategies based on data update patterns, including time-based expiration, explicit invalidation on updates, and version-based invalidation. Add cache warming for predictable data access patterns. Implement cache monitoring that tracks hit rates, memory usage, and invalidation frequency. Create a cache abstraction layer that allows for different cache implementations while maintaining a consistent interface. Use Redis for distributed caching and a local in-memory cache for application-level caching.

**Prompt for Refactoring/Optimization**:
> Enhance the Caching Strategy with more sophisticated caching techniques. Implement a more advanced cache eviction policy based on access frequency and recency (LFU/LRU). Add support for partial cache invalidation that only invalidates affected portions of cached data. Implement cache hierarchies with cascading invalidation for related data. Add predictive cache warming based on user behavior patterns. Enhance distributed caching with sharding for better scalability. Implement cache compression for memory optimization. Add cache analytics that provide insights into cache effectiveness and optimization opportunities. Implement a circuit breaker pattern for graceful degradation when the cache is unavailable.

**Expected Outcome**:
> A robust Caching Strategy that significantly improves performance for frequently accessed data. The implementation should include appropriate cache levels, invalidation strategies, monitoring, and optimization, creating a responsive and efficient application even under high load.

#### Step 3: Implement Asynchronous Processing

**Prompt for Test**:
> Create tests for the Asynchronous Processing system. Develop test cases that verify tasks can be offloaded to background workers and processed reliably. Test different task types, including long-running operations, batch processing, and scheduled tasks. Include tests for task prioritization, retry handling, and failure recovery. Test performance under different load conditions and concurrency levels. Verify that the system handles edge cases like worker failures and task timeouts.

**Prompt for Implementation**:
> Implement an Asynchronous Processing system that offloads time-consuming operations to background workers. Create a task queue using RabbitMQ or a similar message broker for reliable task distribution. Implement worker processes that consume tasks from the queue and execute them asynchronously. Develop task definitions for various operations, including artifact transformation, knowledge extraction, agent execution, and data exports. Add task prioritization to ensure critical tasks are processed first. Implement retry handling with exponential backoff for transient failures. Create a dead-letter queue for tasks that repeatedly fail. Add task monitoring that tracks execution time, success rates, and resource utilization. Implement task scheduling for recurring operations like cache warming and data aggregation. Ensure the system integrates with the Event-Driven Communication system for notifying task completion.

**Prompt for Refactoring/Optimization**:
> Enhance the Asynchronous Processing system with more sophisticated task handling capabilities. Implement dynamic worker scaling based on queue length and processing load. Add support for task batching that groups similar tasks for more efficient processing. Implement more advanced retry strategies with circuit breakers for persistent failures. Add task routing based on resource requirements and worker capabilities. Enhance monitoring with detailed task tracing and performance profiling. Implement task result caching for idempotent operations. Add support for distributed task execution across multiple servers for horizontal scaling. Implement task dependencies and workflows for complex multi-step processes.

**Expected Outcome**:
> A powerful Asynchronous Processing system that effectively offloads time-consuming operations to background workers. The implementation should handle task distribution, prioritization, retry handling, and monitoring, creating a responsive application that can efficiently process resource-intensive tasks.

### Frontend Optimization

#### Step 1: Implement Code Splitting and Lazy Loading

**Prompt for Test**:
> Develop tests for Code Splitting and Lazy Loading. Create test cases that verify components and modules are correctly split and loaded on demand. Test initial load time, chunk sizes, and loading behavior for different application routes. Include tests for loading states, error handling, and retry mechanisms. Test performance on various network conditions, including slow connections and intermittent connectivity. Verify that the implementation correctly handles code splitting boundaries and dependencies.

**Prompt for Implementation**:
> Implement Code Splitting and Lazy Loading for the React frontend to improve initial load time and overall performance. Use React's lazy and Suspense features to split the application into logical chunks that can be loaded on demand. Implement route-based code splitting that loads components only when their routes are accessed. Add component-level code splitting for large, complex components that aren't immediately needed. Implement prefetching for likely navigation paths to improve perceived performance. Create loading states that provide feedback during chunk loading. Add error handling for chunk loading failures with retry mechanisms. Optimize chunk boundaries to balance between too many small chunks and too few large chunks. Configure Webpack or a similar bundler to generate optimized chunks with appropriate caching headers. Ensure the implementation follows best practices for React and TypeScript, including proper typing for lazy-loaded components.

**Prompt for Refactoring/Optimization**:
> Enhance the Code Splitting and Lazy Loading implementation with more sophisticated loading strategies. Implement a more advanced prefetching system that uses user behavior analytics to predict navigation patterns. Add support for preloading critical chunks during idle browser time. Implement progressive loading that first loads a minimal version of a component and then enhances it with additional features. Add performance monitoring that tracks chunk load times and identifies optimization opportunities. Implement more granular code splitting based on feature usage patterns. Add support for offline caching of critical chunks using service workers. Enhance loading states with skeleton screens that match the layout of the loading component.

**Expected Outcome**:
> An efficient Code Splitting and Lazy Loading implementation that significantly improves initial load time and overall performance. The implementation should balance chunk sizes, provide appropriate loading states, handle errors gracefully, and optimize loading strategies, creating a fast and responsive user experience.

#### Step 2: Implement UI Performance Optimization

**Prompt for Test**:
> Create tests for UI Performance Optimization. Develop test cases that measure rendering performance, interaction responsiveness, and memory usage for various UI components and scenarios. Test component render times, rerender frequency, and frame rates during interactions. Include tests for virtualized lists, memoization effectiveness, and state update batching. Test performance on different devices and browsers. Verify that optimizations improve performance without affecting functionality or user experience.

**Prompt for Implementation**:
> Implement UI Performance Optimization for the React frontend to improve rendering performance and interaction responsiveness. Use React.memo, useMemo, and useCallback to prevent unnecessary rerenders of components. Implement virtualized lists using react-window or a similar library for efficiently rendering large collections. Add windowing for large forms and complex layouts to only render visible elements. Optimize state management to minimize rerenders by using appropriate state granularity and update batching. Implement efficient event handling with debouncing and throttling for frequent events like scrolling and resizing. Add performance-focused CSS optimizations, including will-change for animations, contain for layout isolation, and efficient selectors. Optimize images and icons with appropriate formats, sizes, and loading strategies. Implement Web Workers for CPU-intensive operations to keep the main thread responsive. Ensure the implementation follows best practices for React and TypeScript, including proper typing and component composition.

**Prompt for Refactoring/Optimization**:
> Enhance the UI Performance Optimization with more sophisticated optimization techniques. Implement a more advanced virtualization strategy that supports variable-height items and horizontal scrolling. Add support for incremental rendering of complex components using time-slicing techniques. Implement more efficient state management with specialized data structures for specific use cases. Add performance profiling that automatically identifies and suggests optimizations for slow components. Implement more sophisticated animation optimizations using the Web Animations API or CSS containment. Add support for offscreen rendering of complex visualizations using Canvas or WebGL. Enhance image optimization with responsive images, lazy loading, and modern formats like WebP and AVIF.

**Expected Outcome**:
> Optimized UI components that significantly improve rendering performance and interaction responsiveness. The implementation should include appropriate memoization, virtualization, state management, and rendering optimizations, creating a smooth and responsive user interface even for complex views and large datasets.

#### Step 3: Implement Progressive Web App Features

**Prompt for Test**:
> Develop tests for Progressive Web App features. Create test cases that verify offline functionality, installation behavior, and performance metrics. Test service worker registration, caching strategies, and update handling. Include tests for app installation, splash screen display, and notification behavior. Test performance improvements from PWA features, including faster subsequent loads and offline access. Verify that the implementation meets PWA requirements and best practices.

**Prompt for Implementation**:
> Implement Progressive Web App features to enhance the user experience and performance of the application. Create a service worker that caches critical assets and API responses for offline access and faster loading. Implement a Web App Manifest that defines the application name, icons, colors, and display mode for installed instances. Add an app shell architecture that loads instantly and then dynamically populates with content. Implement background sync for offline operations that need to be synchronized when connectivity is restored. Add push notifications for important events and updates. Implement an installation prompt that encourages users to install the application on their devices. Create offline fallbacks for components that require network connectivity. Add a splash screen for a more native-like launch experience. Ensure the implementation follows PWA best practices and meets the criteria for installable web applications.

**Prompt for Refactoring/Optimization**:
> Enhance the Progressive Web App features with more sophisticated capabilities. Implement a more advanced caching strategy with stale-while-revalidate patterns for fresher content. Add support for periodic background sync that keeps content updated even when the app isn't open. Implement more sophisticated offline capabilities with conflict resolution for concurrent online and offline changes. Add support for rich notifications with actions and images. Implement app shortcuts for quick access to specific features. Add badging for important updates and notifications. Enhance the installation experience with custom installation flows and onboarding. Implement analytics that track PWA usage patterns and performance metrics. Add support for Web Share API and other modern web capabilities.

**Expected Outcome**:
> A full-featured Progressive Web App that provides a native-like experience with offline support, installation capabilities, and performance optimizations. The implementation should follow PWA best practices, meet installable criteria, and enhance the user experience across devices and network conditions.

## Security Enhancements

### Authentication and Authorization

#### Step 1: Implement OAuth2 and OpenID Connect

**Prompt for Test**:
> Create tests for OAuth2 and OpenID Connect implementation. Develop test cases that verify authentication flows, token handling, and user profile retrieval. Test different grant types, including authorization code, implicit, and refresh token flows. Include tests for token validation, expiration handling, and refresh mechanisms. Test integration with identity providers and error handling for authentication failures. Verify that the implementation correctly protects resources and handles authentication state.

**Prompt for Implementation**:
> Implement OAuth2 and OpenID Connect for secure authentication with support for multiple identity providers. Create an authentication service that handles OAuth2 flows, including authorization code grant with PKCE for web applications and refresh token grant for maintaining sessions. Implement OpenID Connect for retrieving user profile information during authentication. Add support for multiple identity providers, including popular services like Google, Microsoft, and GitHub, as well as enterprise identity providers. Implement secure token storage using HTTP-only cookies or similar mechanisms to prevent XSS attacks. Add token validation that checks signature, expiration, and claims. Implement token refresh mechanisms that automatically renew expired tokens. Create login, logout, and account linking flows with appropriate security measures. Ensure the implementation follows OAuth2 and OpenID Connect specifications and security best practices.

**Prompt for Refactoring/Optimization**:
> Enhance the OAuth2 and OpenID Connect implementation with more sophisticated authentication capabilities. Implement a more advanced token management system with token revocation and introspection. Add support for fine-grained permissions using OAuth2 scopes. Implement multi-factor authentication integration for additional security. Add support for social login with account linking and merging. Enhance session management with inactivity timeouts and concurrent session controls. Implement more sophisticated token storage with encryption and secure storage mechanisms. Add comprehensive authentication analytics that track login patterns and detect suspicious activities. Implement risk-based authentication that adjusts security requirements based on context and behavior patterns.

**Expected Outcome**:
> A robust OAuth2 and OpenID Connect implementation that provides secure authentication with support for multiple identity providers. The implementation should handle various authentication flows, token management, and user profile retrieval, creating a secure and flexible authentication system for the application.

#### Step 2: Implement Fine-Grained Authorization

**Prompt for Test**:
> Develop tests for Fine-Grained Authorization. Create test cases that verify access control for various resources, operations, and user roles. Test permission checks at different levels, including API endpoints, service methods, and data access. Include tests for role-based access, attribute-based access, and dynamic permissions. Test authorization caching, permission inheritance, and context-aware rules. Verify that the implementation correctly enforces access control and handles authorization failures.

**Prompt for Implementation**:
> Implement Fine-Grained Authorization that controls access to resources based on user roles, attributes, and context. Create an authorization service that provides centralized permission checking for all application components. Implement role-based access control (RBAC) with predefined roles like User, Project Owner, Administrator, and System Administrator. Add attribute-based access control (ABAC) that considers resource attributes, user attributes, and environmental conditions. Develop permission definitions for all resources and operations in the system, following the principle of least privilege. Implement permission inheritance for hierarchical resources like projects and artifacts. Add context-aware authorization rules that consider factors like time, location, and device. Create an authorization cache that improves performance for frequent permission checks. Implement policy enforcement points at API gateways, service boundaries, and data access layers. Ensure the implementation follows security best practices and integrates with the authentication system.

**Prompt for Refactoring/Optimization**:
> Enhance the Fine-Grained Authorization with more sophisticated access control capabilities. Implement a policy language for defining complex authorization rules in a declarative way. Add support for delegated administration that allows resource owners to manage permissions for their resources. Implement more advanced permission inheritance with override capabilities for exceptions. Add dynamic permission calculation based on resource relationships and user context. Enhance the authorization cache with selective invalidation for permission changes. Implement authorization analytics that track permission usage and identify potential security issues. Add support for temporary permissions and permission expiration. Implement a permission simulation tool that helps administrators understand the effects of policy changes.

**Expected Outcome**:
> A comprehensive Fine-Grained Authorization system that effectively controls access to resources based on user roles, attributes, and context. The implementation should provide flexible permission definitions, efficient permission checking, and integration with all application components, creating a secure and manageable access control system.

#### Step 3: Implement Security Monitoring and Auditing

**Prompt for Test**:
> Create tests for Security Monitoring and Auditing. Develop test cases that verify audit logging, security event detection, and alerting mechanisms. Test audit trail completeness, integrity, and searchability for various security-relevant actions. Include tests for security event correlation, anomaly detection, and alert generation. Test performance impact of audit logging under different load conditions. Verify that the implementation correctly captures security events and provides useful audit information.

**Prompt for Implementation**:
> Implement Security Monitoring and Auditing that tracks security-relevant actions and detects potential security issues. Create an audit logging system that records all security-relevant actions, including authentication attempts, authorization decisions, resource access, and configuration changes. Implement structured audit logs with consistent fields like timestamp, user, action, resource, result, and context. Add log integrity protection using techniques like digital signatures or secure append-only storage. Develop security event detection that identifies suspicious patterns like failed login attempts, unusual access patterns, and privilege escalation. Implement real-time alerting for critical security events that require immediate attention. Create an audit search and reporting interface that allows security administrators to investigate incidents and generate compliance reports. Ensure the implementation follows security best practices and minimizes performance impact on the application.

**Prompt for Refactoring/Optimization**:
> Enhance the Security Monitoring and Auditing with more sophisticated security capabilities. Implement a more advanced security event correlation engine that can detect complex attack patterns across multiple events. Add machine learning-based anomaly detection that learns normal behavior patterns and identifies deviations. Implement user behavior analytics that profiles typical user actions and detects unusual behavior. Add context-aware security monitoring that considers factors like time, location, and device. Enhance alerting with severity classification, alert aggregation, and automated response actions. Implement more sophisticated audit storage with efficient compression, retention policies, and archiving. Add compliance reporting templates for common regulatory frameworks like GDPR, HIPAA, and SOC2. Implement a security dashboard that provides real-time visibility into the security posture of the application.

**Expected Outcome**:
> A comprehensive Security Monitoring and Auditing system that effectively tracks security-relevant actions and detects potential security issues. The implementation should provide complete audit trails, security event detection, and alerting mechanisms, creating a secure and compliant application environment.
