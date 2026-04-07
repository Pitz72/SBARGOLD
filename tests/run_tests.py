import unittest
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import test modules
# We need to adapt existing tests to be unittest compatible or just run them as scripts.
# Since existing tests are scripts with `if __name__ == "__main__":`, we can just run them using subprocess or import and call main.
# But better to make a proper runner.

import subprocess

def run_script(script_name):
    print(f"Running {script_name}...")
    env = os.environ.copy()
    env['SBG_TEST_MODE'] = '1'
    result = subprocess.run([sys.executable, script_name], capture_output=True, text=True, env=env)
    if result.returncode == 0:
        print(f"[OK] {script_name} PASSED")
        return True
    else:
        print(f"[FAIL] {script_name} FAILED")
        print(result.stderr)
        print(result.stdout)
        return False

def main():
    tests_dir = os.path.join(os.path.dirname(__file__))
    scripts = [
        "test_lexer.py",
        "test_parser.py",
        "test_interpreter_v2.py",
        "test_strings.py",
        "test_file_io.py",
        "test_data_structures.py",
        "test_modules.py",
        "test_namespaces.py",
        "test_safety.py",
        "test_debugger.py",
        "test_logic.py",
        "test_control_flow.py",
        "test_mutation.py"
    ]
    
    passed = 0
    total = 0
    
    for script in scripts:
        script_path = os.path.join(tests_dir, script)
        if os.path.exists(script_path):
            total += 1
            if run_script(script_path):
                passed += 1
        else:
            print(f"[SKIP] Script {script} not found")
            
    print(f"\nSummary: {passed}/{total} tests passed.")
    
    if passed == total:
        sys.exit(0)
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
