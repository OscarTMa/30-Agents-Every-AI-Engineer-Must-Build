import subprocess
import tempfile
import os
from typing import Tuple

def execute_pytest_in_sandbox(code_str: str, test_str: str) -> Tuple[bool, str]:
    """
    Guarda el código y la suite de pruebas en un directorio temporal aislado
    y ejecuta pytest retornando (éxito, logs_o_stacktrace).
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        module_path = os.path.join(tmpdir, "solution.py")
        test_path = os.path.join(tmpdir, "test_solution.py")

        with open(module_path, "w", encoding="utf-8") as f:
            f.write(code_str)

        with open(test_path, "w", encoding="utf-8") as f:
            # Asegura la importación desde solution.py
            f.write("import pytest\nimport solution\nfrom solution import *\n\n" + test_str)

        cmd = ["pytest", test_path, "-v", "--tb=short"]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, cwd=tmpdir)
        passed = (result.returncode == 0)
        return passed, result.stdout