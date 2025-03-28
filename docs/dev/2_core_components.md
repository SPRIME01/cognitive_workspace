# Core Components Development Prompts

This section contains sequential prompts for developing the core components of the Cognitive Workspace application, including the conversation system, cognitive artifact system, and initial integration.

## Conversation System

### Conversation Service - Basic Structure

#### Step 1: Create Conversation Domain Model

**Prompt for Test**:
> Generate unit tests for the Conversation domain model. The tests should verify the proper implementation of entities like Conversation, Message, and Context. Include tests for conversation creation, message addition, context management, and conversation state transitions. Ensure the tests validate that the domain model enforces business rules such as message ordering, conversation lifecycle states, and participant management. Test edge cases like empty conversations, maximum message limits, and invalid state transitions.

**Prompt for Implementation**:
> Implement the Conversation domain model following Domain-Driven Design principles. Create the core entities: Conversation, Message, and Context. The Conversation entity should manage a collection of messages, track participants, maintain conversation state, and handle context. The Message entity should include content, sender information, timestamp, and message type. The Context entity should store conversation context information that helps maintain coherence across interactions. Implement value objects for specialized types like MessageType, ConversationState, and ParticipantRole. Define aggregates with Conversation as the root. Implement domain events for significant state changes like ConversationCreated, MessageAdded, and ContextUpdated. Use Python's type hints throughout for type safety. Ensure all domain logic is properly encapsulated and that the model enforces business rules defined in the project documentation.

**Prompt for Refactoring/Optimization**:
> Refactor the Conversation domain model to improve performance and maintainability. Optimize message storage for efficient retrieval of recent messages. Implement a more sophisticated context management system that can selectively persist relevant context information. Add support for conversation branching and merging to handle complex interaction patterns. Enhance the domain events system to provide more detailed information about state changes. Implement a conversation summarization mechanism to handle long-running conversations.

**Expected Outcome**:
> A well-designed Conversation domain model that effectively captures the business rules and behavior of conversations in the Cognitive Workspace application. The implementation should be type-safe, maintainable, and aligned with Domain-Driven Design principles.

#### Step 2: Implement Conversation Repository

**Prompt for Test**:
> Create tests for the Conversation repository interface and its MongoDB implementation. The tests should verify that conversations can be created, retrieved, updated, and deleted. Include tests for querying conversations by different criteria such as project ID, participant ID, and date range. Test pagination, sorting, and filtering capabilities. Ensure the tests validate proper handling of concurrent modifications and error conditions. Use mock objects to isolate the repository tests from the actual database.

**Prompt for Implementation**:
> Implement a Conversation repository following the Ports and Adapters architecture. First, define a repository interface (port) in the domain layer that specifies methods for conversation persistence without any infrastructure details. Then, create a MongoDB implementation (adapter) that satisfies this interface. The implementation should handle conversation storage, retrieval, updating, and deletion. Implement efficient querying capabilities for finding conversations by project ID, participant ID, date range, and other relevant criteria. Support pagination, sorting, and filtering. Ensure proper handling of MongoDB-specific concerns like connection management, serialization/deserialization, and error handling. Implement optimistic concurrency control to handle concurrent modifications. Use the MongoDB adapter created in the infrastructure setup phase.

**Prompt for Refactoring/Optimization**:
> Optimize the Conversation repository implementation for better performance and scalability. Implement more sophisticated indexing strategies based on common query patterns. Add caching for frequently accessed conversations. Implement a more efficient serialization/deserialization mechanism. Enhance the query capabilities with full-text search and aggregation pipelines. Add support for sharding to handle large conversation volumes. Implement more robust error handling and retry mechanisms.

**Expected Outcome**:
> A robust Conversation repository that effectively persists and retrieves conversation data. The implementation should follow the Ports and Adapters architecture, provide efficient querying capabilities, and handle infrastructure concerns appropriately.

#### Step 3: Develop Conversation Service with AI Integration

**Prompt for Test**:
> Develop tests for the Conversation service with AI integration. Create test cases that verify the core functionality of the service, including conversation creation, message processing, AI response generation, and context management. Test the integration with the AI model service using mock objects. Include tests for error handling, retry mechanisms, and fallback strategies. Test different conversation scenarios, including multi-turn dialogues, context switching, and conversation summarization.

**Prompt for Implementation**:
> Implement a Conversation service that integrates with AI models for intelligent conversation capabilities. Create an application service that coordinates the conversation flow, including message processing, AI response generation, and context management. Implement a port for AI model integration and create an adapter for a specific AI model service. The service should handle conversation creation, message addition, context tracking, and state management. Implement sophisticated context management that preserves relevant information across conversation turns. Add support for conversation analysis, including intent recognition, entity extraction, and sentiment analysis. Ensure the service follows the Ports and Adapters architecture and integrates with the Conversation repository. Implement error handling, retry mechanisms, and fallback strategies for AI model failures.

**Prompt for Refactoring/Optimization**:
> Enhance the Conversation service with more advanced AI integration capabilities. Implement a mechanism to dynamically select the most appropriate AI model based on the conversation context and requirements. Add support for streaming responses to improve user experience. Implement a more sophisticated context management system that can selectively preserve and forget information based on relevance. Add conversation analytics to track metrics like response quality, user satisfaction, and conversation efficiency. Implement a caching mechanism for common AI responses to improve performance.

**Expected Outcome**:
> A sophisticated Conversation service that effectively manages conversations and integrates with AI models for intelligent responses. The implementation should handle context management, error conditions, and provide a solid foundation for the conversation capabilities of the application.

### Suggestion Engine

#### Step 1: Implement Artifact Suggestion System

**Prompt for Test**:
> Create tests for the Artifact Suggestion system. Develop test cases that verify the system can analyze conversations, identify potential artifact opportunities, and suggest appropriate templates. Test different conversation scenarios, including research discussions, planning sessions, and problem-solving dialogues. Include tests for suggestion relevance scoring, template matching, and suggestion presentation. Test the integration with the Conversation service and Template repository using mock objects.

**Prompt for Implementation**:
> Implement an Artifact Suggestion system that analyzes conversations and suggests appropriate artifact templates. Create a service that integrates with the Conversation service to access conversation content and context. Implement algorithms for identifying potential artifact opportunities based on conversation patterns, keywords, and semantic analysis. Develop a template matching system that selects appropriate templates based on the conversation content and purpose. Implement a relevance scoring mechanism to rank suggestions. Create a suggestion presentation component that formats suggestions for display to users. Ensure the system follows the Ports and Adapters architecture and integrates with the Template repository. Implement the suggestion workflow as described in the "Artifact Template Selection Process" flowchart from the project documentation.

**Prompt for Refactoring/Optimization**:
> Enhance the Artifact Suggestion system with more sophisticated analysis capabilities. Implement machine learning algorithms for better identification of artifact opportunities. Add support for personalized suggestions based on user preferences and history. Implement a feedback mechanism to improve suggestion quality over time. Enhance the template matching system with semantic similarity measures. Add support for suggesting combinations of templates for complex tasks. Implement a caching mechanism for suggestion results to improve performance.

**Expected Outcome**:
> An intelligent Artifact Suggestion system that effectively analyzes conversations and suggests appropriate artifact templates. The implementation should provide relevant, timely suggestions that help users capture and structure knowledge from conversations.

#### Step 2: Develop Context Management System

**Prompt for Test**:
> Develop tests for the Context Management system. Create test cases that verify the system can track, update, and retrieve conversation context across multiple interactions. Test context preservation during conversation pauses and resumptions. Include tests for context relevance scoring, context pruning, and context merging. Test the integration with the Conversation service using mock objects. Verify that the system handles different types of context information, including user intents, entities, and conversation history.

**Prompt for Implementation**:
> Implement a Context Management system that maintains conversation context across multiple interactions. Create a service that tracks relevant information from conversations, including user intents, entities, topics, and important statements. Implement mechanisms for context updating, retrieval, and pruning based on relevance and recency. Develop algorithms for context relevance scoring to identify the most important context elements. Create a context storage component that efficiently persists context information. Implement context merging capabilities for handling related conversations. Ensure the system follows the Ports and Adapters architecture and integrates with the Conversation service. Implement the context management workflow as described in the project documentation.

**Prompt for Refactoring/Optimization**:
> Enhance the Context Management system with more sophisticated context handling capabilities. Implement semantic understanding to better identify and track important context elements. Add support for hierarchical context representation to handle complex conversation structures. Implement a more efficient context storage mechanism with selective persistence based on importance. Enhance the context relevance scoring with machine learning algorithms. Add support for cross-conversation context sharing for related topics. Implement a context visualization component to help users understand the current context.

**Expected Outcome**:
> A sophisticated Context Management system that effectively maintains conversation context across multiple interactions. The implementation should enhance conversation coherence, enable more intelligent responses, and provide a foundation for advanced conversation capabilities.

## Cognitive Artifact System

### Template Engine

#### Step 1: Implement Template Model and Repository

**Prompt for Test**:
> Create tests for the Template domain model and repository. Develop test cases that verify the proper implementation of Template entities, including structure definition, field validation, and template instantiation. Test template creation, retrieval, updating, and deletion. Include tests for template categorization, versioning, and metadata management. Test the repository's querying capabilities, including finding templates by category, purpose, and popularity. Use mock objects to isolate the repository tests from the actual database.

**Prompt for Implementation**:
> Implement the Template domain model and repository following Domain-Driven Design principles and the Ports and Adapters architecture. Create the Template entity with properties for name, description, structure definition, fields, and metadata. Implement value objects for specialized types like TemplateCategory, FieldType, and TemplateStatus. Define validation rules for template structure and fields. Create a Template repository interface in the domain layer and implement a PostgreSQL adapter that satisfies this interface. The implementation should handle template storage, retrieval, updating, and deletion. Implement efficient querying capabilities for finding templates by various criteria. Support template versioning to track changes over time. Ensure proper handling of PostgreSQL-specific concerns like connection management, serialization/deserialization, and error handling.

**Prompt for Refactoring/Optimization**:
> Optimize the Template model and repository for better performance and usability. Implement a more sophisticated template structure definition language that supports complex field types, conditional sections, and dynamic content. Add support for template inheritance and composition to enable template reuse. Enhance the repository with full-text search capabilities for finding templates by content. Implement a template recommendation system based on usage patterns and user feedback. Add caching for frequently accessed templates to improve performance.

**Expected Outcome**:
> A robust Template domain model and repository that effectively manages artifact templates. The implementation should follow Domain-Driven Design principles and the Ports and Adapters architecture, providing a solid foundation for the template capabilities of the application.

#### Step 2: Develop Template Rendering Engine

**Prompt for Test**:
> Develop tests for the Template Rendering Engine. Create test cases that verify the engine can correctly render templates with various field types, conditional sections, and dynamic content. Test rendering with different data inputs, including edge cases like missing data, invalid data, and complex nested structures. Include tests for template validation, error handling, and rendering performance. Test the integration with the Template repository using mock objects.

**Prompt for Implementation**:
> Implement a Template Rendering Engine that transforms template definitions and data into rendered artifacts. Create a service that loads template definitions from the Template repository, validates input data against the template structure, and generates rendered output. Support various field types, including text, numbers, dates, choices, and rich text. Implement conditional rendering based on data values. Add support for dynamic content generation, including AI-assisted content suggestions. Create a template validation component that ensures data consistency and completeness. Implement error handling for rendering failures. Ensure the engine follows the Ports and Adapters architecture and integrates with the Template repository. Implement the rendering workflow as described in the project documentation.

**Prompt for Refactoring/Optimization**:
> Enhance the Template Rendering Engine with more sophisticated rendering capabilities. Implement support for custom rendering functions that can transform data in complex ways. Add a plugin system for extending the engine with new field types and rendering behaviors. Implement a caching mechanism for rendered templates to improve performance. Enhance the validation system with more detailed error reporting and suggestions for fixing issues. Add support for partial rendering to enable progressive template completion. Implement a preview mode for seeing rendering results in real-time as data is entered.

**Expected Outcome**:
> A powerful Template Rendering Engine that effectively transforms template definitions and data into rendered artifacts. The implementation should support various field types, conditional rendering, and dynamic content, providing a flexible foundation for artifact creation.

### Cognitive Artifact Management

#### Step 1: Implement Cognitive Artifact Domain Model

**Prompt for Test**:
> Create tests for the Cognitive Artifact domain model. Develop test cases that verify the proper implementation of entities like CognitiveArtifact, Version, and Content. Include tests for artifact creation, content updating, version management, and state transitions. Ensure the tests validate that the domain model enforces business rules such as version ordering, content validation, and artifact lifecycle states. Test edge cases like empty artifacts, maximum content size, and invalid state transitions.

**Prompt for Implementation**:
> Implement the Cognitive Artifact domain model following Domain-Driven Design principles. Create the core entities: CognitiveArtifact, Version, and Content. The CognitiveArtifact entity should manage artifact metadata, track versions, maintain state, and handle template association. The Version entity should include content, creator information, timestamp, and version number. The Content entity should store structured content based on the template definition. Implement value objects for specialized types like ArtifactType, ArtifactState, and ContentField. Define aggregates with CognitiveArtifact as the root. Implement domain events for significant state changes like ArtifactCreated, ContentUpdated, and StateChanged. Use Python's type hints throughout for type safety. Ensure all domain logic is properly encapsulated and that the model enforces business rules defined in the project documentation.

**Prompt for Refactoring/Optimization**:
> Refactor the Cognitive Artifact domain model to improve performance and maintainability. Optimize version storage for efficient retrieval of recent versions. Implement a more sophisticated content validation system that can handle complex template structures. Add support for artifact branching and merging to handle collaborative editing scenarios. Enhance the domain events system to provide more detailed information about content changes. Implement an artifact summarization mechanism to generate concise representations of artifact content.

**Expected Outcome**:
> A well-designed Cognitive Artifact domain model that effectively captures the business rules and behavior of cognitive artifacts in the Cognitive Workspace application. The implementation should be type-safe, maintainable, and aligned with Domain-Driven Design principles.

#### Step 2: Implement Cognitive Artifact Repository

**Prompt for Test**:
> Create tests for the Cognitive Artifact repository interface and its PostgreSQL/MongoDB implementation. The tests should verify that artifacts can be created, retrieved, updated, and deleted. Include tests for querying artifacts by different criteria such as project ID, creator ID, template type, and date range. Test version history retrieval, content searching, and metadata filtering. Ensure the tests validate proper handling of concurrent modifications and error conditions. Use mock objects to isolate the repository tests from the actual database.

**Prompt for Implementation**:
> Implement a Cognitive Artifact repository following the Ports and Adapters architecture. First, define a repository interface (port) in the domain layer that specifies methods for artifact persistence without any infrastructure details. Then, create a hybrid implementation (adapter) that uses PostgreSQL for artifact metadata and MongoDB for artifact content. The implementation should handle artifact storage, retrieval, updating, and deletion. Implement efficient querying capabilities for finding artifacts by various criteria. Support version history retrieval, content searching, and metadata filtering. Ensure proper handling of database-specific concerns like connection management, serialization/deserialization, and error handling. Implement optimistic concurrency control to handle concurrent modifications. Use the database adapters created in the infrastructure setup phase.

**Prompt for Refactoring/Optimization**:
> Optimize the Cognitive Artifact repository implementation for better performance and scalability. Implement more sophisticated indexing strategies based on common query patterns. Add caching for frequently accessed artifacts and versions. Implement a more efficient serialization/deserialization mechanism for artifact content. Enhance the query capabilities with full-text search and aggregation pipelines. Add support for sharding to handle large artifact volumes. Implement more robust error handling and retry mechanisms.

**Expected Outcome**:
> A robust Cognitive Artifact repository that effectively persists and retrieves artifact data. The implementation should follow the Ports and Adapters architecture, provide efficient querying capabilities, and handle infrastructure concerns appropriately.

#### Step 3: Develop Version Control System

**Prompt for Test**:
> Develop tests for the Version Control System. Create test cases that verify the system can track artifact versions, manage version history, and handle concurrent modifications. Test version creation, retrieval, comparison, and restoration. Include tests for branching, merging, and conflict resolution. Test the integration with the Cognitive Artifact repository using mock objects. Verify that the system handles different types of content changes, including additions, deletions, and modifications.

**Prompt for Implementation**:
> Implement a Version Control System for cognitive artifacts. Create a service that tracks artifact versions, manages version history, and handles concurrent modifications. Implement version creation when artifacts are modified, with appropriate metadata like version number, timestamp, and creator information. Develop algorithms for version comparison to identify changes between versions. Create a version restoration mechanism to revert artifacts to previous states. Implement branching and merging capabilities for collaborative editing scenarios. Add conflict detection and resolution mechanisms for handling concurrent modifications. Ensure the system follows the Ports and Adapters architecture and integrates with the Cognitive Artifact repository. Implement the version control workflow as described in the project documentation.

**Prompt for Refactoring/Optimization**:
> Enhance the Version Control System with more sophisticated version management capabilities. Implement a more efficient storage mechanism for version history that reduces duplication. Add support for selective version restoration that can apply specific changes from previous versions. Implement a more advanced conflict resolution system with automatic merging for non-conflicting changes. Add version tagging and annotation capabilities for marking significant versions. Implement a version visualization component to help users understand the version history and relationships.

**Expected Outcome**:
> A powerful Version Control System that effectively tracks artifact versions and manages collaborative editing. The implementation should provide version history, comparison, restoration, and conflict resolution capabilities, enabling effective collaboration on cognitive artifacts.

## Initial Integration

### Conversation to Artifact Flow

#### Step 1: Implement Conversation to Artifact Transformation

**Prompt for Test**:
> Create tests for the Conversation to Artifact transformation process. Develop test cases that verify the system can extract relevant information from conversations and use it to create cognitive artifacts. Test different conversation scenarios, including research discussions, planning sessions, and problem-solving dialogues. Include tests for content extraction, template selection, and artifact initialization. Test the integration with the Conversation service, Suggestion Engine, and Cognitive Artifact service using mock objects.

**Prompt for Implementation**:
> Implement a Conversation to Artifact transformation process that extracts relevant information from conversations and creates cognitive artifacts. Create a service that integrates with the Conversation service to access conversation content and context. Implement algorithms for extracting key points, insights, and structured information from conversations. Develop a workflow that uses the Suggestion Engine to select appropriate templates and then initializes cognitive artifacts with extracted content. Create a mapping system that transforms conversation elements into artifact fields. Implement a user feedback mechanism to refine the extracted content. Ensure the process follows the Ports and Adapters architecture and integrates with the Conversation service, Suggestion Engine, and Cognitive Artifact service. Implement the transformation workflow as described in the "Artifact Creation from Conversation" sequence diagram in the project documentation.

**Prompt for Refactoring/Optimization**:
> Enhance the Conversation to Artifact transformation process with more sophisticated extraction capabilities. Implement machine learning algorithms for better identification of relevant information in conversations. Add support for handling multiple artifact creation from a single conversation. Implement a more advanced mapping system that can handle complex template structures. Add a learning mechanism that improves extraction quality based on user feedback. Implement a preview mode that shows users what information will be extracted before creating the artifact.

**Expected Outcome**:
> An effective Conversation to Artifact transformation process that extracts relevant information from conversations and creates well-structured cognitive artifacts. The implementation should provide a seamless flow from conversation to artifact, helping users capture and organize knowledge from discussions.

#### Step 2: Develop Artifact Suggestion Integration

**Prompt for Test**:
> Develop tests for the Artifact Suggestion Integration. Create test cases that verify the system can present artifact suggestions during conversations, handle user selection, and initiate artifact creation. Test different suggestion scenarios, including proactive suggestions, user-requested suggestions, and context-based suggestions. Include tests for suggestion presentation, user interaction, and artifact initialization. Test the integration with the Conversation service, Suggestion Engine, and Cognitive Artifact service using mock objects.

**Prompt for Implementation**:
> Implement an Artifact Suggestion Integration that presents artifact suggestions during conversations and facilitates artifact creation. Create a service that integrates with the Conversation service to monitor conversations and identify suggestion opportunities. Implement a suggestion presentation component that displays suggestions to users in an unobtrusive way. Develop a user interaction workflow that allows users to view, select, and customize suggestions. Create an artifact initialization process that uses selected suggestions to create cognitive artifacts. Implement a feedback mechanism to track suggestion effectiveness. Ensure the integration follows the Ports and Adapters architecture and connects the Conversation service, Suggestion Engine, and Cognitive Artifact service. Implement the suggestion workflow as described in the project documentation.

**Prompt for Refactoring/Optimization**:
> Enhance the Artifact Suggestion Integration with more sophisticated suggestion capabilities. Implement a more intelligent suggestion timing system that presents suggestions at optimal moments in conversations. Add support for suggestion customization before artifact creation. Implement a learning mechanism that improves suggestion relevance based on user selections and feedback. Add a suggestion history feature that allows users to revisit previous suggestions. Implement a more seamless transition from suggestion to artifact creation.

**Expected Outcome**:
> A seamless Artifact Suggestion Integration that effectively presents artifact suggestions during conversations and facilitates artifact creation. The implementation should provide a natural flow from conversation to artifact suggestion to artifact creation, enhancing the knowledge capture capabilities of the application.

#### Step 3: Implement Collaborative Editing

**Prompt for Test**:
> Create tests for the Collaborative Editing system. Develop test cases that verify multiple users can simultaneously edit cognitive artifacts with proper conflict detection and resolution. Test different editing scenarios, including concurrent edits to the same field, sequential edits, and conflicting edits. Include tests for real-time updates, change notification, and edit history tracking. Test the integration with the Cognitive Artifact service and Version Control System using mock objects.

**Prompt for Implementation**:
> Implement a Collaborative Editing system that allows multiple users to simultaneously edit cognitive artifacts. Create a service that manages editing sessions, tracks user edits, and synchronizes changes across clients. Implement real-time update mechanisms using WebSockets or similar technology. Develop conflict detection algorithms that identify when multiple users are editing the same content. Create conflict resolution strategies for handling concurrent edits, including automatic merging for non-conflicting changes and user-driven resolution for conflicts. Implement change notification to alert users when others make changes. Create an edit history tracking system that records who made what changes and when. Ensure the system follows the Ports and Adapters architecture and integrates with the Cognitive Artifact service and Version Control System. Implement the collaborative editing workflow as described in the project documentation.

**Prompt for Refactoring/Optimization**:
> Enhance the Collaborative Editing system with more sophisticated collaboration capabilities. Implement a more efficient change synchronization mechanism that reduces network traffic. Add support for presence awareness to show which users are currently viewing or editing an artifact. Implement a more advanced conflict resolution system with visual diff tools for manual resolution. Add commenting and annotation capabilities to facilitate discussion about specific content. Implement edit permissions that can restrict who can edit different parts of an artifact. Add a collaborative session management system that supports explicit editing handoffs.

**Expected Outcome**:
> A robust Collaborative Editing system that allows multiple users to simultaneously edit cognitive artifacts. The implementation should provide real-time updates, conflict resolution, and edit history tracking, enabling effective collaboration on knowledge artifacts.
