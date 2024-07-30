import argparse
import ast
import logging
import os


class ModuleImportChecker:
    def find_imports(self, filename):
        """Extract import statements from a Python file."""
        imports = set()
        with open(filename, "r") as file:
            node = ast.parse(file.read(), filename=filename)

        for n in ast.walk(node):
            if isinstance(n, ast.Import):
                for alias in n.names:
                    imports.add(alias.name.split(".")[0])
            elif isinstance(n, ast.ImportFrom):
                if n.module:
                    imports.add(n.module.split(".")[0])

        return imports

    def check_imports(self, base_dir, modules):
        """Check if a module imports another module."""
        errors = set()
        logging.info(f"Checking imports in Base Directory: {base_dir}")
        for module, forbidden_imports in modules.items():
            module_dir = os.path.join(base_dir, module)
            logging.info(f"Checking module: {module_dir}")
            if not os.path.isdir(module_dir):
                logging.warning(
                    f"Directory for module '{module}' does not exist."
                )
                exit(1)

            for root, _, files in os.walk(module_dir):
                for file in files:
                    if file.endswith(".py") and file != "__init__.py":
                        filepath = os.path.join(root, file)
                        imports = self.find_imports(filepath)

                        forbidden_found = forbidden_imports.intersection(
                            imports
                        )
                        if forbidden_found:
                            for forbidden_import in forbidden_found:
                                message = f"Forbidden import detected: '{module}' imports '{forbidden_import}' in {filepath}"
                                errors.add(message)

        return errors

    def run_module_checker(self):
        parser = argparse.ArgumentParser(
            description="Modular Monolith Import Checker",
            epilog="Ensure that your modules do not import each other inappropriately. Use this script to enforce modular boundaries.",
            usage=""" python import_checker.py /path/to/project module1 module2 module3 ...
\tpython import_checker.py . module1 module2 module3 ...
\tpython import_checker.py project_name module1 module2 module3 ...""",
        )
        parser.add_argument(
            "base_dir",
            type=str,
            help="Base directory of the project or the module within the project. Can be a relative path or an absolute path.",
        )
        parser.add_argument(
            "modules",
            type=str,
            nargs="+",
            help="List of module names to check. Provide all modules in your project. Each module name should be listed separately with a space.",
        )

        args = parser.parse_args()

        base_dir = args.base_dir
        module_names = args.modules

        # Automatically create forbidden import rules
        modules = {
            module: set(module_names) - {module} for module in module_names
        }

        logging.basicConfig(level=logging.INFO)
        errors = self.check_imports(base_dir, modules)
        if errors:
            logging.error("Module Import check failed with errors:")
            for error in errors:
                logging.error(error)
            exit(1)
        else:
            logging.info("Module Import check passed successfully.")
            exit(0)
