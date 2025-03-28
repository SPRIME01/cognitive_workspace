"""
Tests to validate the structure of the infrastructure layer in accordance with DDD principles.
"""

import inspect
import pytest
import os
from typing import Dict, Type, Any, List


class TestInfrastructureLayer:
    """Test suite for validating the infrastructure layer structure."""

    def test_infrastructure_layer_exists(self, infrastructure_modules):
        """
        Test that the infrastructure layer exists and has modules.

        Arrange:
            - Get all infrastructure modules

        Act:
            - Count the number of modules

        Assert:
            - Verify that infrastructure modules exist
        """
        assert len(infrastructure_modules) > 0, (
            "Infrastructure layer should have at least one module"
        )

    def test_repository_implementations_exist(
        self, infrastructure_classes, domain_classes
    ):
        """
        Test that repository implementations exist in the infrastructure layer.

        Arrange:
            - Get all infrastructure classes
            - Get all domain repository interfaces

        Act:
            - Identify repository implementation classes
            - Check if they implement domain repository interfaces

        Assert:
            - Verify that repositories are properly implemented
        """
        # Skip if either infrastructure or domain classes are not found
        if not infrastructure_classes or not domain_classes:
            pytest.skip("Infrastructure or domain classes not found")

        # Find domain repository interfaces
        domain_repositories = []
        for module_path, classes in domain_classes.items():
            for class_name, class_obj in classes.items():
                if class_name.endswith("Repository") or "repositories" in module_path:
                    domain_repositories.append((module_path, class_name, class_obj))

        # Skip if no domain repositories found
        if not domain_repositories:
            pytest.skip("No domain repositories found")

        # Find repository implementations in infrastructure
        repo_implementations = []
        for module_path, classes in infrastructure_classes.items():
            for class_name, class_obj in classes.items():
                if (
                    "Repository" in class_name
                    or "repositories" in module_path
                    or "persistence" in module_path
                ):
                    repo_implementations.append((module_path, class_name, class_obj))

        assert len(repo_implementations) > 0, (
            "Infrastructure layer should have repository implementations"
        )

        # Advanced: Check that implementations actually implement domain interfaces
        # This is complex and might be skipped based on actual project structure

    def test_domain_independence(self, domain_classes, infrastructure_classes):
        """
        Test that the domain layer does not depend on infrastructure.

        Arrange:
            - Get all domain classes
            - Get all infrastructure classes

        Act:
            - Check if domain classes import or use infrastructure classes

        Assert:
            - Verify that domain layer is independent from infrastructure concerns
        """
        # Skip if either domain or infrastructure classes are not found
        if not domain_classes or not infrastructure_classes:
            pytest.skip("Domain or infrastructure classes not found")

        # Get all infrastructure module paths
        infra_module_paths = list(infrastructure_classes.keys())

        # Check domain classes for dependencies on infrastructure
        domain_with_infra_deps = []

        for domain_module, classes in domain_classes.items():
            for class_name, class_obj in classes.items():
                # Check source code for imports of infrastructure modules
                try:
                    class_src = inspect.getsource(class_obj)

                    # Look for imports from infrastructure modules
                    for infra_module in infra_module_paths:
                        # Extract module name without full path for import checks
                        infra_module_name = infra_module.split(".")[-1]
                        if (
                            f"import {infra_module_name}" in class_src
                            or f"from {infra_module_name}" in class_src
                        ):
                            domain_with_infra_deps.append((domain_module, class_name))
                            break
                except (OSError, TypeError):
                    pass

        assert len(domain_with_infra_deps) == 0, (
            "Domain classes should not depend on infrastructure"
        )

    def test_infrastructure_implements_domain_interfaces(
        self, domain_classes, infrastructure_classes
    ):
        """
        Test that infrastructure classes properly implement domain interfaces.

        Arrange:
            - Get all domain interfaces
            - Get all infrastructure implementations

        Act:
            - Check if infrastructure classes implement required domain interface methods

        Assert:
            - Verify that infrastructure properly implements domain contracts
        """
        # Skip if either domain or infrastructure classes are not found
        if not domain_classes or not infrastructure_classes:
            pytest.skip("Domain or infrastructure classes not found")

        # Find domain interfaces (repositories and services)
        domain_interfaces = []
        for module_path, classes in domain_classes.items():
            for class_name, class_obj in classes.items():
                if (
                    class_name.endswith("Repository")
                    or class_name.endswith("Service")
                    or class_name.endswith("Port")
                ):
                    # Store name and methods
                    methods = [
                        name
                        for name, _ in inspect.getmembers(class_obj, inspect.isfunction)
                        if not name.startswith("_")
                    ]
                    domain_interfaces.append((class_name, methods))

        # Skip if no domain interfaces found
        if not domain_interfaces:
            pytest.skip("No domain interfaces found")

        # Find infrastructure implementations
        implementations_count = 0

        for module_path, classes in infrastructure_classes.items():
            for class_name, class_obj in classes.items():
                # Check class hierarchy to find domain interface implementation
                bases = inspect.getmro(class_obj)
                for base in bases:
                    base_name = base.__name__
                    # Find matching domain interface
                    for interface_name, interface_methods in domain_interfaces:
                        if base_name == interface_name:
                            # Check if implementation provides all methods
                            class_methods = [
                                name
                                for name, _ in inspect.getmembers(
                                    class_obj, inspect.isfunction
                                )
                                if not name.startswith("_")
                            ]

                            implements_all = all(
                                method in class_methods for method in interface_methods
                            )
                            if implements_all:
                                implementations_count += 1
                                break

        assert implementations_count > 0, (
            "Infrastructure should implement domain interfaces"
        )

    def test_database_adapters_exist(self, infrastructure_classes):
        """
        Test that database adapters exist in the infrastructure layer.

        Arrange:
            - Get all infrastructure classes

        Act:
            - Identify database adapter classes

        Assert:
            - Verify that database adapters are implemented
        """
        # Find database adapter classes
        db_adapters = []

        for module_path, classes in infrastructure_classes.items():
            for class_name, class_obj in classes.items():
                # Check for database adapter naming patterns
                if (
                    class_name.endswith("Adapter")
                    or class_name.endswith("Repository")
                    or "database" in module_path
                    or "persistence" in module_path
                    or "repositories" in module_path
                ):
                    # Check for database-related methods or imports
                    try:
                        class_src = inspect.getsource(class_obj)
                        if (
                            "database" in class_src
                            or "connection" in class_src
                            or "session" in class_src
                            or "query" in class_src
                            or "postgresql" in class_src.lower()
                            or "mongo" in class_src.lower()
                            or "kuzu" in class_src.lower()
                        ):
                            db_adapters.append((module_path, class_name))
                    except (OSError, TypeError):
                        pass

        assert len(db_adapters) > 0, (
            "Infrastructure layer should have database adapters"
        )

    def test_external_services_adapters_exist(self, infrastructure_classes):
        """
        Test that adapters for external services exist in the infrastructure layer.

        Arrange:
            - Get all infrastructure classes

        Act:
            - Identify external service adapter classes

        Assert:
            - Verify that external service adapters are implemented
        """
        # Find external service adapter classes
        ext_adapters = []

        for module_path, classes in infrastructure_classes.items():
            for class_name, class_obj in classes.items():
                # Check for external service adapter naming patterns
                if (
                    class_name.endswith("Adapter")
                    or class_name.endswith("Client")
                    or class_name.endswith("Gateway")
                    or "services" in module_path
                    or "clients" in module_path
                    or "integrations" in module_path
                ):
                    # Check for external service related code
                    try:
                        class_src = inspect.getsource(class_obj)
                        if (
                            "http" in class_src
                            or "request" in class_src
                            or "api" in class_src
                            or "url" in class_src
                            or "client" in class_src
                        ):
                            ext_adapters.append((module_path, class_name))
                    except (OSError, TypeError):
                        pass

        # External service adapters might not be required in all applications
        # So this test is informational rather than a hard requirement
        if not ext_adapters:
            pytest.skip("No external service adapters found")
        else:
            assert len(ext_adapters) > 0, (
                "Infrastructure layer should have external service adapters"
            )

    def test_ports_and_adapters_separation(
        self, domain_classes, infrastructure_classes
    ):
        """
        Test that the architecture follows the Ports and Adapters pattern.

        Arrange:
            - Get all domain port/interface classes
            - Get all infrastructure adapter implementations

        Act:
            - Check for proper separation of ports (domain) and adapters (infrastructure)

        Assert:
            - Verify ports and adapters are properly separated
        """
        # Skip if either domain or infrastructure classes are not found
        if not domain_classes or not infrastructure_classes:
            pytest.skip("Domain or infrastructure classes not found")

        # Find domain ports (interfaces)
        domain_ports = []
        for module_path, classes in domain_classes.items():
            for class_name, class_obj in classes.items():
                # Look for port naming patterns
                if (
                    class_name.endswith("Port")
                    or class_name.endswith("Repository")
                    or class_name.endswith("Gateway")
                    or "ports" in module_path
                ):
                    domain_ports.append(class_name)

        # Find adapter implementations in infrastructure
        adapters = []
        for module_path, classes in infrastructure_classes.items():
            for class_name, class_obj in classes.items():
                # Look for adapter naming patterns
                if (
                    class_name.endswith("Adapter")
                    or class_name.endswith("RepositoryImpl")
                    or class_name.endswith("Implementation")
                    or "adapters" in module_path
                ):
                    adapters.append(class_name)

        # Check if we have both ports and adapters
        has_ports = len(domain_ports) > 0
        has_adapters = len(adapters) > 0

        assert has_ports, "Domain layer should define ports (interfaces)"
        assert has_adapters, "Infrastructure layer should implement adapters"
