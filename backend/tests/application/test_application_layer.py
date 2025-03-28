"""
Tests to validate the structure of the application layer in accordance with DDD principles.
"""

import inspect
import pytest
from typing import Dict, Type, Any, List


class TestApplicationLayer:
    """Test suite for validating the application layer structure."""

    def test_application_layer_exists(self, application_modules):
        """
        Test that the application layer exists and has modules.

        Arrange:
            - Get all application modules

        Act:
            - Count the number of modules

        Assert:
            - Verify that application modules exist
        """
        assert len(application_modules) > 0, (
            "Application layer should have at least one module"
        )

    def test_application_services_exist(self, application_classes):
        """
        Test that application services exist.

        Arrange:
            - Get all application classes

        Act:
            - Identify application service classes
              (conventionally named with *Service, *UseCase suffix or in services module)

        Assert:
            - Verify that application services exist
        """
        app_services = []

        for module_path, classes in application_classes.items():
            for class_name, class_obj in classes.items():
                # Check for application service naming convention or location
                if (
                    class_name.endswith("Service")
                    or class_name.endswith("ApplicationService")
                    or class_name.endswith("UseCase")
                    or class_name.endswith("Command")
                    or class_name.endswith("Query")
                    or "services" in module_path
                    or "usecases" in module_path
                ):
                    app_services.append((module_path, class_name, class_obj))

        assert len(app_services) > 0, (
            "Application layer should have at least one application service"
        )

    def test_application_services_use_domain(self, application_classes, domain_classes):
        """
        Test that application services use domain objects and services.

        Arrange:
            - Get all application service classes
            - Get all domain classes

        Act:
            - Check if application services have dependencies on domain elements

        Assert:
            - Verify that application services interact with the domain layer
        """
        # Skip if either application or domain classes are not found
        if not application_classes or not domain_classes:
            pytest.skip("Application or domain classes not found")

        # Flatten domain classes for easier lookup
        all_domain_classes = {}
        for module_classes in domain_classes.values():
            all_domain_classes.update(module_classes)

        # Find all application services
        app_services = []
        for module_path, classes in application_classes.items():
            for class_name, class_obj in classes.items():
                if (
                    class_name.endswith("Service")
                    or class_name.endswith("ApplicationService")
                    or class_name.endswith("UseCase")
                    or class_name.endswith("Command")
                    or class_name.endswith("Query")
                    or "services" in module_path
                    or "usecases" in module_path
                ):
                    app_services.append((module_path, class_name, class_obj))

        # Skip if no application services found
        if not app_services:
            pytest.skip("No application services found")

        # Check if application services use domain classes
        services_using_domain = 0

        for module_path, class_name, class_obj in app_services:
            # Check for dependencies in constructor
            init_method = getattr(class_obj, "__init__", None)
            if init_method:
                try:
                    init_src = inspect.getsource(init_method)
                    # Check if any domain class names appear in constructor
                    if any(
                        domain_class in init_src
                        for domain_class in all_domain_classes.keys()
                    ):
                        services_using_domain += 1
                        continue
                except (OSError, TypeError):
                    pass

            # Check for domain class usage in method signatures
            for name, method in inspect.getmembers(class_obj, inspect.isfunction):
                try:
                    method_src = inspect.getsource(method)
                    if any(
                        domain_class in method_src
                        for domain_class in all_domain_classes.keys()
                    ):
                        services_using_domain += 1
                        break
                except (OSError, TypeError):
                    pass

        assert services_using_domain > 0, (
            "Application services should use domain objects"
        )

    def test_command_query_separation(self, application_classes):
        """
        Test that application services follow Command Query Separation (CQS) principle.

        Arrange:
            - Get all application service classes

        Act:
            - Check methods for command-query separation

        Assert:
            - Verify that methods either perform actions or return data, not both
        """
        # Find all application services
        app_services = []
        for module_path, classes in application_classes.items():
            for class_name, class_obj in classes.items():
                if (
                    class_name.endswith("Service")
                    or class_name.endswith("ApplicationService")
                    or class_name.endswith("UseCase")
                    or "services" in module_path
                    or "usecases" in module_path
                ):
                    app_services.append((module_path, class_name, class_obj))

        # Skip if no application services found
        if not app_services:
            pytest.skip("No application services found")

        # Check for CQS pattern adherence (dedicated Command and Query classes or methods)
        services_with_cqs = 0

        for module_path, class_name, class_obj in app_services:
            # Check if class is explicitly a Command or Query
            if class_name.endswith("Command") or class_name.endswith("Query"):
                services_with_cqs += 1
                continue

            # Check method signatures and naming conventions
            command_methods = []
            query_methods = []

            for name, method in inspect.getmembers(class_obj, inspect.isfunction):
                if name.startswith("_"):  # Skip private methods
                    continue

                # Check method naming conventions
                if (
                    name.startswith("get")
                    or name.startswith("find")
                    or name.startswith("query")
                    or name.startswith("retrieve")
                    or name.startswith("search")
                ):
                    query_methods.append(name)
                elif (
                    name.startswith("create")
                    or name.startswith("update")
                    or name.startswith("delete")
                    or name.startswith("perform")
                    or name.startswith("execute")
                    or name.startswith("process")
                ):
                    command_methods.append(name)

            # Count classes with clear separation
            if command_methods and query_methods:
                # Check if the service follows CQS by having separate methods for commands and queries
                services_with_cqs += 1
            elif len(command_methods) > 0 and len(query_methods) == 0:
                # Pure command service
                services_with_cqs += 1
            elif len(query_methods) > 0 and len(command_methods) == 0:
                # Pure query service
                services_with_cqs += 1

        assert services_with_cqs > 0, (
            "Application services should follow Command Query Separation"
        )

    def test_application_services_dont_bypass_domain(self, application_classes):
        """
        Test that application services don't bypass domain logic.

        Arrange:
            - Get all application service classes

        Act:
            - Check if application services contain domain logic themselves

        Assert:
            - Verify that application services delegate to domain objects
        """
        # Find all application services
        app_services = []
        for module_path, classes in application_classes.items():
            for class_name, class_obj in classes.items():
                if (
                    class_name.endswith("Service")
                    or class_name.endswith("ApplicationService")
                    or class_name.endswith("UseCase")
                    or class_name.endswith("Command")
                    or class_name.endswith("Query")
                    or "services" in module_path
                    or "usecases" in module_path
                ):
                    app_services.append((module_path, class_name, class_obj))

        # Skip if no application services found
        if not app_services:
            pytest.skip("No application services found")

        # Check if application services contain domain logic
        direct_persistence = 0
        validation_logic = 0

        for module_path, class_name, class_obj in app_services:
            # Check all methods for signs of bypassing domain
            for name, method in inspect.getmembers(class_obj, inspect.isfunction):
                if name.startswith("_"):  # Skip private methods
                    continue

                try:
                    method_src = inspect.getsource(method)

                    # Look for direct DB interaction patterns (suggesting bypassing repositories)
                    if (
                        "connection" in method_src
                        or "cursor" in method_src
                        or "execute(" in method_src
                        or "query(" in method_src
                    ):
                        direct_persistence += 1

                    # Look for domain validation logic in application layer
                    if (
                        "validate" in method_src
                        and "if" in method_src
                        and "raise" in method_src
                    ):
                        validation_logic += 1

                except (OSError, TypeError):
                    pass

        # We want to verify that application services don't contain domain logic
        assert direct_persistence == 0, (
            "Application services should not interact directly with the database"
        )
        assert validation_logic == 0, (
            "Application services should delegate validation to domain objects"
        )
