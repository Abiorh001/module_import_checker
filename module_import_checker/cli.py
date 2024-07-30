from .module_import_checker import ModuleImportChecker


def main():
    """Main entry point for the CLI."""
    checker = ModuleImportChecker()
    checker.run_module_checker()
