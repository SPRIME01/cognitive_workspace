"""
Shared test fixtures and utilities for DDD structure validation.
"""

import os
import sys
import importlib
import pkgutil
import pytest
import inspect
from typing import List, Dict, Any, Set, Type

# Add the backend directory to Python path so we can import from app
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)


def get_module_classes(module_path: str) -> Dict[str, Type]:
    """
    Retrieve all classes from a module path.

    Args:
        module_path: The Python import path to the module

    Returns:
        Dictionary mapping class names to class objects
    """
    try:
        module = importlib.import_module(module_path)
        return {
            name: obj
            for name, obj in inspect.getmembers(module, inspect.isclass)
            if obj.__module__ == module_path
        }
    except (ImportError, ModuleNotFoundError):
        return {}


def get_all_modules_in_package(package_path: str) -> List[str]:
    """
    Recursively get all module paths in a package.

    Args:
        package_path: The Python import path to the package

    Returns:
        List of module paths
    """
    try:
        package = importlib.import_module(package_path)
        if not hasattr(package, '__file__') or package.__file__ is None:
            return []
        package_dir = os.path.dirname(package.__file__)
        module_paths = []

        for _, name, is_pkg in pkgutil.walk_packages([package_dir], f"{package_path}."):
            if not is_pkg:
                module_paths.append(name)
            else:
                module_paths.extend(get_all_modules_in_package(name))

        return module_paths
    except (ImportError, ModuleNotFoundError, AttributeError):
        return []


@pytest.fixture
def domain_modules() -> List[str]:
    """
    Fixture that returns all domain module paths.
    """
    # Adjust this path based on your actual domain package location
    return get_all_modules_in_package("app.domain")


@pytest.fixture
def application_modules() -> List[str]:
    """
    Fixture that returns all application module paths.
    """
    # Adjust this path based on your actual application package location
    return get_all_modules_in_package("app.application")


@pytest.fixture
def infrastructure_modules() -> List[str]:
    """
    Fixture that returns all infrastructure module paths.
    """
    # Adjust this path based on your actual infrastructure package location
    return get_all_modules_in_package("app.infrastructure")


@pytest.fixture
def domain_classes(domain_modules) -> Dict[str, Dict[str, Type]]:
    """
    Fixture that returns all domain classes grouped by module.
    """
    return {module_path: get_module_classes(module_path) for module_path in domain_modules}


@pytest.fixture
def application_classes(application_modules) -> Dict[str, Dict[str, Type]]:
    """
    Fixture that returns all application classes grouped by module.
    """
    return {module_path: get_module_classes(module_path) for module_path in application_modules}


@pytest.fixture
def infrastructure_classes(infrastructure_modules) -> Dict[str, Dict[str, Type]]:
    """
    Fixture that returns all infrastructure classes grouped by module.
    """
    return {module_path: get_module_classes(module_path) for module_path in infrastructure_modules}
