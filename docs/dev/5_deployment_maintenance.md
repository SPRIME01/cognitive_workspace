# Deployment and Maintenance Prompts

This section contains sequential prompts for deploying and maintaining the Cognitive Workspace application, including CI/CD pipeline setup, deployment configuration, and monitoring and maintenance.

## CI/CD Pipeline Setup

### Continuous Integration

#### Step 1: Implement Automated Testing Pipeline

**Prompt for Test**:
> Create tests for the Automated Testing Pipeline. Develop test cases that verify the pipeline correctly executes unit tests, integration tests, and end-to-end tests for both backend and frontend code. Test pipeline triggers, test execution, result reporting, and failure handling. Include tests for test coverage calculation, quality gate enforcement, and test result visualization. Verify that the pipeline correctly identifies and reports test failures and quality issues.

**Prompt for Implementation**:
> Implement an Automated Testing Pipeline using GitHub Actions or a similar CI/CD platform. Create workflow configurations that trigger test execution on code pushes, pull requests, and scheduled intervals. Implement separate test stages for different test types, including unit tests, integration tests, and end-to-end tests for both backend and frontend code. Add test parallelization for faster execution of large test suites. Implement test coverage calculation using tools like pytest-cov for Python and Jest coverage for TypeScript. Create quality gates that enforce minimum test coverage and code quality standards. Add test result reporting with detailed information about failures and performance metrics. Implement test result visualization using GitHub Actions summaries or a dedicated dashboard. Ensure the pipeline integrates with the version control system and provides clear feedback to developers.

**Prompt for Refactoring/Optimization**:
> Enhance the Automated Testing Pipeline with more sophisticated testing capabilities. Implement test selection that only runs tests affected by code changes to improve pipeline speed. Add test flakiness detection and automatic retries for unstable tests. Implement test result trend analysis that tracks test health over time. Add performance testing that measures and enforces performance benchmarks. Enhance test coverage analysis with branch coverage and complexity metrics. Implement mutation testing to evaluate test effectiveness. Add security testing using tools like SAST (Static Application Security Testing) and dependency scanning. Implement a test environment management system that provides isolated environments for parallel test execution.

**Expected Outcome**:
> A robust Automated Testing Pipeline that effectively executes tests, reports results, and enforces quality standards. The implementation should support various test types, provide clear feedback, and integrate with the development workflow, creating a foundation for continuous integration.

#### Step 2: Implement Code Quality Analysis

**Prompt for Test**:
> Develop tests for the Code Quality Analysis system. Create test cases that verify the system correctly analyzes code quality, identifies issues, and enforces standards. Test static code analysis, linting, formatting checks, and complexity metrics for both backend and frontend code. Include tests for custom rule enforcement, quality trend tracking, and issue prioritization. Verify that the system correctly integrates with the CI/CD pipeline and provides useful feedback to developers.

**Prompt for Implementation**:
> Implement a Code Quality Analysis system using tools like SonarQube, ESLint, Flake8, and Prettier. Create configurations for static code analysis that identify code smells, bugs, vulnerabilities, and maintainability issues. Implement linting rules that enforce coding standards and best practices for Python and TypeScript. Add formatting checks that ensure consistent code style across the codebase. Implement complexity metrics calculation to identify overly complex code that needs refactoring. Create custom rules that enforce project-specific standards and architectural constraints. Add quality trend tracking that monitors code quality over time. Implement issue prioritization based on severity, impact, and effort. Create quality gates that prevent merging code with critical issues. Ensure the system integrates with the CI/CD pipeline and provides clear feedback through comments on pull requests and dashboard visualizations.

**Prompt for Refactoring/Optimization**:
> Enhance the Code Quality Analysis system with more sophisticated analysis capabilities. Implement AI-assisted code review that provides intelligent suggestions for improvements. Add architectural analysis that verifies compliance with the intended architecture and identifies dependency issues. Implement more advanced security analysis with vulnerability detection and secure coding practice enforcement. Add performance analysis that identifies potential performance bottlenecks. Enhance the feedback mechanism with inline code suggestions and automatic fix proposals. Implement team-level quality metrics that track quality trends by team and component. Add gamification elements that encourage developers to improve code quality. Implement a knowledge base that provides guidance on addressing common quality issues.

**Expected Outcome**:
> A comprehensive Code Quality Analysis system that effectively analyzes code quality, identifies issues, and enforces standards. The implementation should support various analysis types, provide clear feedback, and integrate with the development workflow, creating a foundation for maintaining high code quality.

#### Step 3: Implement Build and Artifact Management

**Prompt for Test**:
> Create tests for the Build and Artifact Management system. Develop test cases that verify the system correctly builds application components, manages dependencies, and produces deployment artifacts. Test build triggers, dependency resolution, compilation, bundling, and artifact storage for both backend and frontend code. Include tests for versioning, tagging, and artifact promotion across environments. Verify that the system correctly handles build failures and dependency conflicts.

**Prompt for Implementation**:
> Implement a Build and Artifact Management system using tools like GitHub Actions, Docker, and a container registry. Create build workflows that compile, bundle, and package application components for deployment. Implement dependency management that resolves and caches dependencies for faster builds. Add versioning that assigns unique identifiers to builds based on git tags, commit hashes, or semantic versioning. Create Docker image building for containerized deployment of backend services. Implement frontend asset bundling with optimizations for production. Add artifact storage in a container registry or artifact repository with appropriate access controls. Implement artifact promotion workflows that move tested artifacts through environments from development to production. Create build caching to improve build performance for unchanged components. Ensure the system integrates with the CI/CD pipeline and provides clear feedback about build status and artifacts.

**Prompt for Refactoring/Optimization**:
> Enhance the Build and Artifact Management system with more sophisticated build capabilities. Implement distributed builds that parallelize build steps across multiple runners for faster execution. Add incremental builds that only rebuild changed components. Implement more advanced dependency analysis with vulnerability scanning and license compliance checking. Add build performance monitoring that tracks build times and identifies bottlenecks. Enhance artifact management with retention policies, artifact metadata, and usage tracking. Implement reproducible builds that guarantee the same inputs produce the same outputs. Add build notifications that alert developers about build status and issues. Implement a build dashboard that provides visibility into build history, performance, and artifacts.

**Expected Outcome**:
> A robust Build and Artifact Management system that effectively builds application components, manages dependencies, and produces deployment artifacts. The implementation should support various build types, provide clear feedback, and integrate with the development workflow, creating a foundation for continuous delivery.

### Continuous Deployment

#### Step 1: Implement Deployment Automation

**Prompt for Test**:
> Develop tests for the Deployment Automation system. Create test cases that verify the system correctly deploys application components to different environments, manages configuration, and handles deployment lifecycle. Test deployment triggers, environment selection, configuration injection, and deployment verification. Include tests for rollback mechanisms, canary deployments, and blue-green deployments. Verify that the system correctly handles deployment failures and provides appropriate feedback.

**Prompt for Implementation**:
> Implement a Deployment Automation system using tools like GitHub Actions, Kubernetes, and Helm. Create deployment workflows that deploy application components to different environments based on triggers like manual approvals, successful builds, or scheduled releases. Implement environment management that maintains separate configurations for development, staging, and production environments. Add configuration management that injects environment-specific configuration into deployments. Implement deployment strategies including rolling updates, blue-green deployments, and canary releases. Add deployment verification that confirms successful deployment through health checks and smoke tests. Implement rollback mechanisms that can revert to previous versions in case of issues. Create deployment notifications that alert stakeholders about deployment status and issues. Ensure the system integrates with the CI/CD pipeline and provides clear feedback about deployment status and history.

**Prompt for Refactoring/Optimization**:
> Enhance the Deployment Automation system with more sophisticated deployment capabilities. Implement a more advanced deployment orchestration that coordinates complex multi-service deployments with dependencies. Add traffic management that gradually shifts traffic to new versions during deployment. Implement feature flags that allow enabling or disabling features without redeployment. Add deployment windows that restrict deployments to specific time periods to minimize risk. Enhance rollback mechanisms with automatic rollback triggers based on monitoring metrics. Implement deployment analytics that track deployment frequency, success rates, and recovery times. Add deployment approval workflows with role-based permissions and audit trails. Implement a deployment dashboard that provides visibility into deployment history, status, and metrics.

**Expected Outcome**:
> A comprehensive Deployment Automation system that effectively deploys application components to different environments, manages configuration, and handles deployment lifecycle. The implementation should support various deployment strategies, provide clear feedback, and integrate with the development workflow, creating a foundation for reliable and frequent deployments.

#### Step 2: Implement Infrastructure as Code

**Prompt for Test**:
> Create tests for the Infrastructure as Code implementation. Develop test cases that verify the system correctly defines, provisions, and manages infrastructure resources. Test infrastructure definition, validation, provisioning, and updates for different environments. Include tests for resource dependencies, state management, and drift detection. Verify that the system correctly handles provisioning failures and provides appropriate feedback.

**Prompt for Implementation**:
> Implement Infrastructure as Code using tools like Terraform, AWS CDK, or Pulumi. Create infrastructure definitions for all required resources, including compute instances, databases, message queues, storage, networking, and security components. Implement modular infrastructure components that can be composed for different environments. Add environment-specific configurations that customize infrastructure for development, staging, and production. Implement state management that tracks the current state of infrastructure and manages changes. Add validation that checks infrastructure definitions for errors, security issues, and best practices before provisioning. Create provisioning workflows that apply infrastructure changes through the CI/CD pipeline. Implement drift detection that identifies manual changes to infrastructure. Add documentation generation that creates diagrams and documentation from infrastructure code. Ensure the implementation follows infrastructure best practices and integrates with the CI/CD pipeline.

**Prompt for Refactoring/Optimization**:
> Enhance the Infrastructure as Code implementation with more sophisticated infrastructure management capabilities. Implement a more advanced module system with versioned, reusable infrastructure components. Add cost estimation that calculates the expected cost of infrastructure changes before provisioning. Implement policy as code that enforces security, compliance, and architectural standards for infrastructure. Add infrastructure testing that verifies provisioned resources meet requirements. Enhance state management with locking and remote state storage for team collaboration. Implement infrastructure monitoring that tracks resource utilization and performance. Add self-healing infrastructure that automatically recovers from failures. Implement infrastructure analytics that track provisioning times, success rates, and resource efficiency.

**Expected Outcome**:
> A robust Infrastructure as Code implementation that effectively defines, provisions, and manages infrastructure resources. The implementation should support various resource types, provide clear feedback, and integrate with the development workflow, creating a foundation for reliable and reproducible infrastructure.

#### Step 3: Implement Release Management

**Prompt for Test**:
> Develop tests for the Release Management system. Create test cases that verify the system correctly plans, coordinates, and tracks releases across environments. Test release planning, approval workflows, release execution, and post-release verification. Include tests for release notes generation, changelog management, and release communication. Verify that the system correctly handles release failures and provides appropriate feedback to stakeholders.

**Prompt for Implementation**:
> Implement a Release Management system that coordinates and tracks releases across environments. Create release planning tools that help teams define release scope, schedule, and dependencies. Implement approval workflows that require appropriate sign-offs before promoting releases to production. Add release execution coordination that orchestrates deployment steps and verifies success. Implement release notes generation that automatically compiles changes from version control commits and issue tracking. Create changelog management that maintains a history of releases and their contents. Add release communication tools that notify stakeholders about upcoming and completed releases. Implement release metrics tracking that measures release frequency, success rates, and recovery times. Ensure the system integrates with the CI/CD pipeline and provides clear visibility into release status and history.

**Prompt for Refactoring/Optimization**:
> Enhance the Release Management system with more sophisticated release capabilities. Implement a more advanced release planning system with dependency tracking and impact analysis. Add release risk assessment that evaluates potential risks based on change scope, affected components, and historical data. Implement feature-based releases that track features across multiple code changes and environments. Add release train scheduling that coordinates regular release cycles. Enhance release notes with automatic categorization of changes and affected components. Implement release analytics that track trends in release metrics over time. Add integration with incident management to correlate releases with potential issues. Implement a release dashboard that provides comprehensive visibility into release planning, execution, and history.

**Expected Outcome**:
> A comprehensive Release Management system that effectively plans, coordinates, and tracks releases across environments. The implementation should support various release workflows, provide clear communication, and integrate with the development process, creating a foundation for reliable and predictable releases.

## Monitoring and Maintenance

### Application Monitoring

#### Step 1: Implement Logging and Error Tracking

**Prompt for Test**:
> Create tests for the Logging and Error Tracking system. Develop test cases that verify the system correctly captures, stores, and analyzes logs and errors from all application components. Test log generation, collection, storage, and search for different log levels and components. Include tests for error detection, grouping, and notification. Verify that the system correctly handles high log volumes and provides appropriate search and analysis capabilities.

**Prompt for Implementation**:
> Implement a Logging and Error Tracking system using tools like ELK Stack (Elasticsearch, Logstash, Kibana), Sentry, or similar solutions. Create a centralized logging architecture that collects logs from all application components, including backend services, frontend applications, and infrastructure. Implement structured logging with consistent fields like timestamp, service, level, message, and context. Add log levels (DEBUG, INFO, WARN, ERROR, FATAL) with appropriate usage guidelines. Implement context enrichment that adds request IDs, user information, and other relevant context to logs. Create error tracking that captures exceptions, groups similar errors, and tracks occurrence frequency. Add error notification that alerts developers about new or recurring errors. Implement log retention policies that balance storage costs with troubleshooting needs. Create log search and visualization dashboards that help developers investigate issues. Ensure the system handles high log volumes and provides good performance for log queries.

**Prompt for Refactoring/Optimization**:
> Enhance the Logging and Error Tracking system with more sophisticated capabilities. Implement log correlation that connects related logs across services using trace IDs. Add log analysis with pattern detection and anomaly identification. Implement error prioritization based on impact, frequency, and affected users. Add root cause analysis tools that help identify the underlying causes of errors. Enhance notification with intelligent alerting that reduces noise and alert fatigue. Implement log-based metrics that extract performance and business metrics from logs. Add security monitoring that identifies potential security issues in logs. Implement a self-service log exploration tool that allows non-technical users to investigate issues.

**Expected Outcome**:
> A comprehensive Logging and Error Tracking system that effectively captures, stores, and analyzes logs and errors from all application components. The implementation should provide clear visibility into application behavior, help troubleshoot issues, and support proactive problem detection, creating a foundation for reliable application operation.

#### Step 2: Implement Performance Monitoring

**Prompt for Test**:
> Develop tests for the Performance Monitoring system. Create test cases that verify the system correctly measures, stores, and analyzes performance metrics from all application components. Test metric collection, aggregation, storage, and visualization for different metric types and components. Include tests for threshold alerting, trend analysis, and anomaly detection. Verify that the system correctly handles high metric volumes and provides appropriate analysis capabilities.

**Prompt for Implementation**:
> Implement a Performance Monitoring system using tools like Prometheus, Grafana, New Relic, or similar solutions. Create a metrics collection architecture that gathers performance data from all application components, including backend services, frontend applications, databases, and infrastructure. Implement the RED method (Request rate, Error rate, Duration) for service monitoring and the USE method (Utilization, Saturation, Errors) for resource monitoring. Add custom business metrics that track application-specific performance indicators. Implement metric aggregation that combines data points for efficient storage and analysis. Create dashboards that visualize performance metrics with appropriate charts and graphs. Add threshold-based alerting that notifies operators when metrics exceed defined thresholds. Implement trend analysis that identifies gradual performance degradation. Create performance baselines that establish normal performance patterns for comparison. Ensure the system handles high metric volumes and provides good performance for metric queries.

**Prompt for Refactoring/Optimization**:
> Enhance the Performance Monitoring system with more sophisticated monitoring capabilities. Implement distributed tracing that tracks requests across multiple services to identify bottlenecks. Add anomaly detection using statistical methods or machine learning to identify unusual performance patterns. Implement predictive alerting that forecasts potential issues before they impact users. Add synthetic monitoring that simulates user interactions to detect issues proactively. Enhance dashboards with service-level objective (SLO) tracking and error budgets. Implement performance analytics that correlate metrics with deployments, traffic patterns, and infrastructure changes. Add capacity planning tools that help predict future resource needs based on growth trends. Implement a self-service monitoring platform that allows teams to create custom dashboards and alerts.

**Expected Outcome**:
> A robust Performance Monitoring system that effectively measures, stores, and analyzes performance metrics from all application components. The implementation should provide clear visibility into application performance, help identify bottlenecks, and support proactive optimization, creating a foundation for a responsive and efficient application.

#### Step 3: Implement User Experience Monitoring

**Prompt for Test**:
> Create tests for the User Experience Monitoring system. Develop test cases that verify the system correctly measures, stores, and analyzes user experience metrics from frontend applications. Test metric collection, aggregation, storage, and visualization for different user experience aspects. Include tests for real user monitoring, synthetic monitoring, and user feedback collection. Verify that the system correctly handles high metric volumes and provides appropriate analysis capabilities.

**Prompt for Implementation**:
> Implement a User Experience Monitoring system using tools like Google Analytics, Mixpanel, or custom solutions. Create a monitoring architecture that captures user experience metrics from frontend applications, including page load times, interaction times, error rates, and user flows. Implement real user monitoring (RUM) that collects performance data from actual user sessions. Add synthetic monitoring that simulates user journeys to detect issues before users encounter them. Implement user feedback collection through in-app surveys, feedback forms, and session recordings. Create user segmentation that analyzes metrics by user type, device, location, and other relevant factors. Add user journey analysis that tracks how users navigate through the application. Implement conversion funnel tracking that identifies drop-off points in critical workflows. Create dashboards that visualize user experience metrics with appropriate charts and graphs. Ensure the system respects user privacy and complies with relevant regulations like GDPR.

**Prompt for Refactoring/Optimization**:
> Enhance the User Experience Monitoring system with more sophisticated monitoring capabilities. Implement session replay that records and replays user sessions to understand issues in context. Add heatmap visualization that shows where users click, scroll, and focus on pages. Implement sentiment analysis on user feedback to identify emotional responses. Add A/B testing integration that correlates user experience metrics with different application variants. Enhance user journey analysis with path comparison and optimization suggestions. Implement predictive analytics that forecasts user behavior based on historical patterns. Add competitive benchmarking that compares user experience metrics with industry standards. Implement a user experience score that combines multiple metrics into an overall health indicator.

**Expected Outcome**:
> A comprehensive User Experience Monitoring system that effectively measures, stores, and analyzes user experience metrics from frontend applications. The implementation should provide clear visibility into user behavior, help identify usability issues, and support continuous improvement, creating a foundation for a user-centered application.

### Maintenance and Support

#### Step 1: Implement Incident Management

**Prompt for Test**:
> Develop tests for the Incident Management system. Create test cases that verify the system correctly detects, tracks, and resolves incidents across all application components. Test incident detection, classification, notification, and resolution workflows. Include tests for escalation procedures, status communication, and post-incident analysis. Verify that the system correctly handles different incident types and provides appropriate coordination tools.

**Prompt for Implementation**:
> Implement an Incident Management system using tools like PagerDuty, OpsGenie, or similar solutions. Create an incident detection mechanism that identifies issues from monitoring alerts, user reports, and system checks. Implement incident classification that categorizes incidents by severity, impact, and affected components. Add incident notification that alerts appropriate responders based on incident type and severity. Implement on-call scheduling that ensures 24/7 coverage for critical systems. Create incident response workflows that guide responders through investigation and resolution steps. Add status communication tools that keep stakeholders informed about incident progress. Implement incident tracking that records timeline, actions taken, and resolution details. Create post-incident analysis (postmortem) templates that help teams learn from incidents. Ensure the system integrates with monitoring tools and communication platforms for seamless incident handling.

**Prompt for Refactoring/Optimization**:
> Enhance the Incident Management system with more sophisticated incident handling capabilities. Implement automated incident triage that suggests likely causes and resolution steps based on historical data. Add incident correlation that identifies related incidents and root causes. Implement runbooks and playbooks that provide detailed resolution procedures for common incidents. Add incident prediction that identifies potential issues before they impact users. Enhance communication with automated status updates and dedicated incident channels. Implement incident analytics that track metrics like mean time to detect (MTTD), mean time to resolve (MTTR), and incident frequency. Add learning systems that improve incident response based on past incidents. Implement chaos engineering integration that proactively tests system resilience.

**Expected Outcome**:
> A robust Incident Management system that effectively detects, tracks, and resolves incidents across all application components. The implementation should provide clear incident visibility, streamline response coordination, and support continuous improvement, creating a foundation for reliable application operation and quick issue resolution.

#### Step 2: Implement Backup and Recovery

**Prompt for Test**:
> Create tests for the Backup and Recovery system. Develop test cases that verify the system correctly backs up, stores, and restores data from all persistence layers. Test backup scheduling, execution, verification, and storage for different data types and volumes. Include tests for point-in-time recovery, disaster recovery, and backup security. Verify that the system correctly handles backup failures and provides appropriate monitoring and reporting.

**Prompt for Implementation**:
> Implement a Backup and Recovery system for all persistence layers, including PostgreSQL, MongoDB, Kuzu GraphDB, and file storage. Create backup strategies appropriate for each data type, including full backups, incremental backups, and continuous archiving (WAL shipping) for databases. Implement backup scheduling that balances frequency with performance impact. Add backup verification that confirms backup integrity and restorability. Create secure backup storage with encryption, access controls, and geographic redundancy. Implement retention policies that balance storage costs with recovery needs. Add point-in-time recovery capabilities for databases to enable precise restoration. Create disaster recovery procedures that can restore the entire system in case of major failures. Implement backup monitoring that tracks backup success, size, and duration. Add recovery testing procedures that regularly verify backup effectiveness. Ensure the system complies with data protection regulations and business continuity requirements.

**Prompt for Refactoring/Optimization**:
> Enhance the Backup and Recovery system with more sophisticated backup capabilities. Implement application-consistent backups that ensure data integrity across related services. Add backup impact reduction through techniques like snapshot-based backups and backup offloading. Implement more advanced retention strategies with tiered storage and archival policies. Add automated recovery testing that regularly verifies backup integrity and recovery procedures. Enhance disaster recovery with cross-region replication and automated failover. Implement backup analytics that track backup trends, storage usage, and recovery performance. Add self-service recovery options that allow developers to restore specific data without administrator intervention. Implement backup optimization that reduces backup size through compression, deduplication, and incremental strategies.

**Expected Outcome**:
> A comprehensive Backup and Recovery system that effectively backs up, stores, and restores data from all persistence layers. The implementation should provide reliable data protection, efficient recovery options, and appropriate monitoring, creating a foundation for data durability and business continuity.

#### Step 3: Implement System Maintenance Procedures

**Prompt for Test**:
> Develop tests for System Maintenance Procedures. Create test cases that verify the procedures correctly handle routine maintenance tasks, updates, and optimizations. Test database maintenance, software updates, security patching, and performance tuning procedures. Include tests for maintenance scheduling, execution, verification, and rollback. Verify that the procedures minimize downtime and user impact while effectively maintaining system health.

**Prompt for Implementation**:
> Implement System Maintenance Procedures for routine upkeep of all application components. Create database maintenance procedures for tasks like index rebuilding, statistics updates, vacuum operations, and integrity checks. Implement software update workflows for applying patches, library updates, and security fixes with minimal downtime. Add infrastructure maintenance procedures for operating system updates, capacity adjustments, and resource optimization. Create security maintenance workflows for vulnerability scanning, patch management, and security configuration updates. Implement performance tuning procedures based on monitoring data and usage patterns. Add maintenance scheduling that balances urgency with user impact, preferring off-peak hours for disruptive operations. Create maintenance documentation that provides step-by-step instructions, verification steps, and rollback procedures. Implement maintenance notification that informs users about planned maintenance activities. Ensure the procedures integrate with monitoring systems to verify successful completion and detect any issues.

**Prompt for Refactoring/Optimization**:
> Enhance the System Maintenance Procedures with more sophisticated maintenance capabilities. Implement automated maintenance that executes routine tasks without manual intervention. Add impact analysis that predicts the effects of maintenance activities before execution. Implement maintenance windows that define appropriate times for different maintenance types. Add zero-downtime maintenance techniques like rolling updates, blue-green deployments, and database replication. Enhance maintenance coordination to handle dependencies between components. Implement maintenance analytics that track maintenance frequency, duration, and success rates. Add predictive maintenance that identifies potential issues before they require emergency intervention. Implement a maintenance calendar that coordinates activities across teams and systems.

**Expected Outcome**:
> Comprehensive System Maintenance Procedures that effectively handle routine maintenance tasks, updates, and optimizations. The implementation should provide clear instructions, minimize user impact, and maintain system health, creating a foundation for reliable and efficient long-term operation.
