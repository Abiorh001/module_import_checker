# Modular Monolith Import Checker

## Overview

The **Modular Monolith Import Checker** is a Python utility designed to enforce modular boundaries within your codebase. It ensures that modules in a modular monolith architecture do not import each other inappropriately, maintaining clear module boundaries and a clean architecture. It can also be used to enforce modular boundaries in a monorepo and ensuring modular boundaries are enforced both locally and in CI/CD pipelines.

## Features

- **Detect Forbidden Imports:** Identifies cases where a module imports another module that it shouldn't.
- **Flexible Path Handling:** Supports both absolute and relative paths for specifying base directories.
- **Dynamic Module List:** Allows you to specify a list of modules to check.

## Installation

To use the Modular Monolith Import Checker, you need Python 3 installed. Install the package using pip:

```bash
pip install module-import-checker
```

## Usage

You can run the import checker from the command line or import it into your Python scripts.

### Command-Line Interface

Run the import checker directly from the command line with various configurations:

1. **Modules at the Project Root:**

   ```bash
   import_module_checker /path/to/project module1 module2 module3
   ```

   - `/path/to/project` is the base directory of your project.
   - `module1`, `module2`, `module3`, etc., are the names of the modules you want to check.

2. **Modules in the Current Directory:**

   ```bash
   import_module_checker . module1 module2 module3
   ```

   - Use `.` if you are running the script from the project root directory.

3. **Modules Inside a Subdirectory:**

   ```bash
   import_module_checker project_name module1 module2 module3
   ```

   - `project_name` is the name of the subdirectory containing your modules.

### Example

To check imports in a project located in `/home/user/myproject` where modules are named `auth`, `users`, and `payments`, run:

```bash
import_module_checker /home/user/myproject auth users payments
```

You can create a bash script to run this command automatically:

```bash
#!/bin/bash
import_module_checker /home/user/myproject auth users payments
```

### Command-Line Help

For detailed usage information, run:

```bash
import_module_checker --help
```

### Using within a Build Process

To integrate the import checker into your CI/CD pipeline and ensure that builds fail if there are forbidden imports, you can include it in your build script. This will either pass and continue the build process or fail and exit. For example, in a GitHub Actions workflow:

```yaml
name: CI

on: [push, pull_request]

jobs:
  import-check:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'
      
      - name: Install Dependencies
        run: |
          python -m pip install --upgrade pip
          pip install --no-cache-dir module-import-checker
      
      - name: Run Import Checker
        run: |
          import_module_checker project_name module1 module2 module3
```

### Example Output

```text
Checking imports in Base Directory: /home/user/myproject
Checking module: /home/user/myproject/auth/
Import check failed with errors:
Forbidden import detected: 'users' imports 'auth' in /home/user/myproject/users/services.py
```

## Contributing

If you would like to contribute to this project, please fork the repository and submit a pull request. Ensure that your code follows the existing style and includes tests for new features.

## License

This project is licensed under the GNU General Public License - see the [LICENSE](LICENSE) file for details.

## Contact

For any questions or issues, please contact [abiolaadeshinaadedayo@gmail.com](mailto:abiolaadeshinaadedayo@gmail.com).