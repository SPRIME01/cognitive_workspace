# Foundation Setup Prompts

This section contains sequential prompts for setting up the foundation of the Cognitive Workspace application, including project initialization, core architecture setup, base infrastructure configuration, and authentication system.

## Project Initialization

### Project Setup - Monorepo Structure

#### Step 1: Create Project Structure and Configuration

**Prompt for Test**:
> Generate a test script that verifies the correct setup of a monorepo structure for our Cognitive Workspace application. The test should check for the existence of core directories (backend, frontend, shared, infrastructure), verify the presence of essential configuration files (package.json, tsconfig.json, .gitignore, README.md), and validate that the monorepo can be built without errors. Include tests for linting configuration and type checking.

**Prompt for Implementation**:
> Create a monorepo structure for the Cognitive Workspace application using a modern monorepo tool like Nx or Turborepo. Set up the following core directories: backend (for Python FastAPI services), frontend (for React TypeScript application), shared (for common code and types), and infrastructure (for deployment configurations). Include essential configuration files: root package.json with workspaces, appropriate tsconfig.json files, comprehensive .gitignore, and a detailed README.md. Configure linting (ESLint for TypeScript, Flake8 for Python), formatting (Prettier), and commit hooks (Husky). Ensure the structure supports independent versioning while maintaining dependencies between packages. The structure should be designed to scale both vertically and horizontally, with clear boundaries between components to facilitate a potential future migration to microservices.

**Prompt for Refactoring/Optimization**:
> Optimize the monorepo structure by implementing a build caching strategy to improve development efficiency. Configure dependency management to minimize duplication and ensure consistent versions across packages. Implement a shared testing infrastructure that can be used by all packages. Add documentation generation scripts that aggregate documentation from all packages into a cohesive set.

**Expected Outcome**:
> A fully configured monorepo structure with appropriate directory organization, configuration files, development tools, and build processes. The structure should support efficient development workflows, maintain clear boundaries between components, and provide a foundation for scaling the application.

### Backend - Core Architecture Setup

#### Step 1: Define Domain-Driven Design Structure

**Prompt for Test**:
> Create a test suite that validates the Domain-Driven Design (DDD) structure of our backend application. The tests should verify the proper separation of domains, the existence of domain entities, value objects, aggregates, repositories, domain services, and application services. Include tests that check for proper encapsulation of domain logic and that domain objects cannot be modified in invalid ways. Verify that the domain layer is independent of infrastructure concerns.

**Prompt for Implementation**:
> Implement a Domain-Driven Design (DDD) structure for the backend of our Cognitive Workspace application using Python and FastAPI. Create a clear separation between the domain, application, infrastructure, and presentation layers. Define the core domains based on the bounded contexts identified in the project documentation: User Management, Project Management, Conversation System, Artifact Management, Agent System, and Knowledge Management. For each domain, create the necessary entities, value objects, aggregates, repositories, and domain services. Implement domain events for cross-domain communication. Use Python's type hints extensively to ensure type safety. Follow the Ports and Adapters (Hexagonal) architecture pattern to ensure the domain logic is isolated from external concerns. Provide interfaces (ports) for all external dependencies and implement adapters for concrete implementations.

**Prompt for Refactoring/Optimization**:
> Refactor the DDD implementation to improve the domain model based on the core domain concepts. Enhance the domain events system to support asynchronous processing and event sourcing. Implement a more robust validation mechanism for domain objects using a dedicated validation framework. Optimize the repository interfaces to support more flexible query capabilities while maintaining the domain integrity.

**Expected Outcome**:
> A well-structured backend architecture following Domain-Driven Design principles, with clear separation of concerns, proper encapsulation of domain logic, and a flexible, maintainable codebase. The architecture should support the complex domain model of the Cognitive Workspace application while remaining adaptable to changing requirements.

#### Step 2: Implement Ports and Adapters Architecture

**Prompt for Test**:
> Develop tests for the Ports and Adapters (Hexagonal) architecture implementation. Create test cases that verify the proper isolation of the domain layer from external dependencies through ports (interfaces) and adapters. Test that the application can switch between different implementations of the same port (e.g., different database adapters) without affecting the domain logic. Include tests for both primary adapters (driving the application) and secondary adapters (driven by the application).

**Prompt for Implementation**:
> Implement the Ports and Adapters (Hexagonal) architecture for the Cognitive Workspace backend. Define clear interfaces (ports) for all external dependencies, including databases, message buses, AI services, and external APIs. Create adapter implementations for each port, starting with the primary adapters (API controllers, GraphQL resolvers) and secondary adapters (database repositories, message bus clients, external service clients). Use dependency injection to wire up the appropriate adapters to the application services. Ensure that the domain logic remains completely isolated from infrastructure concerns. Implement adapters for PostgreSQL, MongoDB, and Kuzu GraphDB according to the data model defined in the project documentation. Create adapters for RabbitMQ for the message bus implementation. Develop adapters for AI model integration.

**Prompt for Refactoring/Optimization**:
> Enhance the Ports and Adapters implementation by creating a more flexible dependency injection system. Refactor the adapters to support runtime switching between different implementations. Implement adapter factories that can create the appropriate adapter based on configuration. Add comprehensive logging and monitoring to all adapters to track performance and errors.

**Expected Outcome**:
> A flexible and maintainable Ports and Adapters architecture that effectively isolates the domain logic from external dependencies. The implementation should support easy switching between different infrastructure components and provide a solid foundation for implementing the application's features.

#### Step 3: Set Up Message Bus Infrastructure

**Prompt for Test**:
> Create tests for the message bus infrastructure using RabbitMQ. The tests should verify that messages can be published to the bus, that subscribers receive the appropriate messages, and that the system handles errors gracefully. Include tests for different message types, message serialization/deserialization, and retry mechanisms. Test the integration with the domain events system.

**Prompt for Implementation**:
> Implement a message bus infrastructure using RabbitMQ for the Cognitive Workspace application. Create a message bus adapter that implements the message bus port defined in the Ports and Adapters architecture. Develop a message serialization/deserialization system that supports different message formats. Implement a publisher component that can send messages to the bus and a subscriber component that can receive and process messages. Create a message routing system based on message types and topics. Integrate the message bus with the domain events system to publish domain events to the bus. Implement error handling, retry mechanisms, and dead letter queues. Ensure the message bus supports both synchronous and asynchronous communication patterns.

**Prompt for Refactoring/Optimization**:
> Optimize the message bus implementation by adding support for message prioritization, message batching, and message compression. Enhance the error handling with more sophisticated retry strategies and circuit breakers. Implement a monitoring system that tracks message throughput, latency, and error rates. Add support for message versioning to handle schema evolution.

**Expected Outcome**:
> A robust message bus infrastructure using RabbitMQ that supports reliable communication between different components of the application. The implementation should handle errors gracefully, provide monitoring capabilities, and integrate seamlessly with the domain events system.

### Infrastructure - Database Setup

#### Step 1: Configure PostgreSQL for User and Artifact Data

**Prompt for Test**:
> Develop tests for the PostgreSQL database setup. Create test cases that verify the connection to the database, the creation of tables according to the schema defined in the project documentation, and basic CRUD operations on the user and artifact data. Include tests for database migrations, indexes, and constraints. Test the integration with the repository adapters.

**Prompt for Implementation**:
> Set up PostgreSQL for storing user and artifact data in the Cognitive Workspace application. Create a database schema based on the logical and physical data models defined in the project documentation. Implement the necessary tables, indexes, constraints, and relationships. Develop a migration system using Alembic to manage schema changes. Create a PostgreSQL adapter that implements the repository ports for user and artifact data. Implement connection pooling, transaction management, and error handling. Ensure the database setup supports the performance requirements specified in the non-functional requirements.

**Prompt for Refactoring/Optimization**:
> Optimize the PostgreSQL setup by implementing more sophisticated indexing strategies based on query patterns. Add support for partitioning large tables to improve performance. Implement a more robust connection pooling mechanism with monitoring. Enhance the migration system to support zero-downtime migrations.

**Expected Outcome**:
> A properly configured PostgreSQL database for storing user and artifact data, with appropriate schema, indexes, and constraints. The implementation should include a migration system, connection pooling, and integration with the repository adapters.

#### Step 2: Configure MongoDB for Conversation and Agent Data

**Prompt for Test**:
> Create tests for the MongoDB database setup. Develop test cases that verify the connection to the database, the creation of collections according to the schema defined in the project documentation, and basic CRUD operations on the conversation and agent data. Include tests for indexes, validation rules, and aggregation pipelines. Test the integration with the repository adapters.

**Prompt for Implementation**:
> Set up MongoDB for storing conversation and agent data in the Cognitive Workspace application. Create a database schema based on the logical and physical data models defined in the project documentation. Implement the necessary collections, indexes, and validation rules. Develop a migration system to manage schema changes. Create a MongoDB adapter that implements the repository ports for conversation and agent data. Implement connection management, error handling, and retry mechanisms. Ensure the database setup supports the performance requirements specified in the non-functional requirements.

**Prompt for Refactoring/Optimization**:
> Enhance the MongoDB setup by implementing more sophisticated indexing strategies based on query patterns. Add support for sharding to improve scalability. Implement a more robust connection management mechanism with monitoring. Optimize the schema design for better performance and storage efficiency.

**Expected Outcome**:
> A properly configured MongoDB database for storing conversation and agent data, with appropriate collections, indexes, and validation rules. The implementation should include a migration system, connection management, and integration with the repository adapters.

#### Step 3: Configure Kuzu GraphDB for Knowledge Graph

**Prompt for Test**:
> Develop tests for the Kuzu GraphDB setup. Create test cases that verify the connection to the database, the creation of nodes and relationships according to the schema defined in the project documentation, and basic graph operations on the knowledge data. Include tests for graph traversal, pattern matching, and aggregation. Test the integration with the repository adapters.

**Prompt for Implementation**:
> Set up Kuzu GraphDB for storing the knowledge graph in the Cognitive Workspace application. Create a graph schema based on the logical and physical data models defined in the project documentation. Implement the necessary node types, relationship types, and properties. Develop a migration system to manage schema changes. Create a Kuzu GraphDB adapter that implements the repository ports for knowledge data. Implement connection management, error handling, and retry mechanisms. Ensure the database setup supports the performance requirements specified in the non-functional requirements.

**Prompt for Refactoring/Optimization**:
> Optimize the Kuzu GraphDB setup by implementing more sophisticated indexing strategies based on query patterns. Enhance the graph schema design for better performance and query flexibility. Implement a caching mechanism for frequently accessed graph patterns. Develop more advanced graph algorithms for knowledge discovery.

**Expected Outcome**:
> A properly configured Kuzu GraphDB for storing the knowledge graph, with appropriate node types, relationship types, and properties. The implementation should include a migration system, connection management, and integration with the repository adapters.

### Authentication System

#### Step 1: Implement User Authentication Service

**Prompt for Test**:
> Create tests for the user authentication service. Develop test cases that verify user registration, login, logout, password reset, and token validation. Include tests for different authentication methods, error handling, and security features such as rate limiting and account lockout. Test the integration with the user repository and the API gateway.

**Prompt for Implementation**:
> Implement a user authentication service for the Cognitive Workspace application using FastAPI and modern authentication best practices. Create endpoints for user registration, login, logout, and password reset. Implement JWT-based authentication with proper token management, including token issuance, validation, and refresh. Use bcrypt for password hashing. Implement security features such as rate limiting, account lockout after failed attempts, and secure password policies. Create a user repository adapter that integrates with the PostgreSQL database. Ensure the authentication service follows the Ports and Adapters architecture and integrates with the API gateway.

**Prompt for Refactoring/Optimization**:
> Enhance the authentication service by adding support for multi-factor authentication, OAuth2 integration for third-party authentication providers, and more sophisticated token management with token revocation. Implement a more robust rate limiting mechanism based on user behavior patterns. Add comprehensive security logging and monitoring.

**Expected Outcome**:
> A secure and robust user authentication service that supports user registration, login, logout, and password reset. The implementation should follow security best practices, integrate with the user repository, and provide a solid foundation for the application's authentication needs.

#### Step 2: Implement Role-Based Access Control

**Prompt for Test**:
> Develop tests for the role-based access control (RBAC) system. Create test cases that verify role assignment, permission checking, and access control enforcement. Include tests for different user roles, resource types, and access patterns. Test the integration with the authentication service and the API gateway.

**Prompt for Implementation**:
> Implement a role-based access control (RBAC) system for the Cognitive Workspace application. Define a set of roles based on the stakeholders identified in the project documentation, including regular users, project owners, administrators, and system administrators. Create a permission model that covers all resources and operations in the system. Implement role assignment and management, permission checking, and access control enforcement. Integrate the RBAC system with the authentication service and the API gateway. Ensure the implementation follows the Ports and Adapters architecture and supports the security requirements specified in the non-functional requirements.

**Prompt for Refactoring/Optimization**:
> Enhance the RBAC system by implementing a more flexible permission model that supports custom roles and fine-grained permissions. Add support for role hierarchies and permission inheritance. Implement a caching mechanism for permission checks to improve performance. Develop an audit system that tracks permission changes and access attempts.

**Expected Outcome**:
> A comprehensive role-based access control system that effectively manages user roles and permissions. The implementation should integrate with the authentication service, enforce access control across the application, and provide a flexible foundation for the application's security needs.

#### Step 3: Set Up API Gateway with Authentication Middleware

**Prompt for Test**:
> Create tests for the API gateway with authentication middleware. Develop test cases that verify request routing, authentication token validation, rate limiting, and error handling. Include tests for different API endpoints, authentication scenarios, and error conditions. Test the integration with the authentication service and the RBAC system.

**Prompt for Implementation**:
> Implement an API gateway for the Cognitive Workspace application using a modern API gateway solution compatible with FastAPI. Create authentication middleware that validates JWT tokens, extracts user information, and integrates with the RBAC system for permission checking. Implement request routing to the appropriate backend services based on the URL path and HTTP method. Add rate limiting, request logging, and error handling. Ensure the API gateway supports the performance and security requirements specified in the non-functional requirements.

**Prompt for Refactoring/Optimization**:
> Enhance the API gateway by implementing more sophisticated routing strategies based on content type, headers, and query parameters. Add support for request transformation, response caching, and circuit breaking. Implement a more robust rate limiting mechanism based on user behavior patterns. Develop a comprehensive monitoring system that tracks request metrics, error rates, and performance.

**Expected Outcome**:
> A robust API gateway that effectively routes requests to the appropriate backend services, enforces authentication and authorization, and provides essential cross-cutting concerns such as rate limiting and logging. The implementation should integrate seamlessly with the authentication service and the RBAC system.
