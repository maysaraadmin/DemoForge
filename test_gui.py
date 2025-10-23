#!/usr/bin/env python3
"""
Test script to verify GUI functionality
"""
import sys
import os

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")

    try:
        import PyQt5
        print("✓ PyQt5 imported successfully")
    except ImportError as e:
        print(f"✗ PyQt5 import failed: {e}")
        return False

    try:
        import subprocess
        print("✓ subprocess module available")
    except ImportError as e:
        print(f"✗ subprocess import failed: {e}")
        return False

    return True

def test_docker_connection():
    """Test Docker connectivity"""
    print("\nTesting Docker connection...")

    try:
        import subprocess
        result = subprocess.run(['docker', '--version'],
                              capture_output=True, text=True, timeout=5)

        if result.returncode == 0:
            print(f"✓ Docker available: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ Docker command failed: {result.stderr}")
            return False

    except FileNotFoundError:
        print("✗ Docker not found in PATH")
        return False
    except Exception as e:
        print(f"✗ Docker test failed: {e}")
        return False

def test_docker_compose():
    """Test Docker Compose availability"""
    print("\nTesting Docker Compose...")

    try:
        import subprocess
        result = subprocess.run(['docker-compose', '--version'],
                              capture_output=True, text=True, timeout=5)

        if result.returncode == 0:
            print(f"✓ Docker Compose available: {result.stdout.strip()}")
            return True
        else:
            print(f"✗ Docker Compose failed: {result.stderr}")
            return False

    except FileNotFoundError:
        print("✗ Docker Compose not found in PATH")
        return False
    except Exception as e:
        print(f"✗ Docker Compose test failed: {e}")
        return False

def test_gui_import():
    """Test if GUI module can be imported"""
    print("\nTesting GUI module import...")

    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import gui_manager
        print("✓ GUI module imported successfully")
        return True
    except ImportError as e:
        print(f"✗ GUI import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ GUI test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("DemoForge GUI Test Suite")
    print("=" * 40)

    tests_passed = 0
    total_tests = 4

    if test_imports():
        tests_passed += 1

    if test_docker_connection():
        tests_passed += 1

    if test_docker_compose():
        tests_passed += 1

    if test_gui_import():
        tests_passed += 1

    print("\n" + "=" * 40)
    print(f"Tests passed: {tests_passed}/{total_tests}")

    if tests_passed == total_tests:
        print("🎉 All tests passed! GUI should work correctly.")
        print("\nTo start the GUI, run:")
        print("  python launch_gui.py")
        print("  or")
        print("  ./launch_gui.bat (Windows)")
    else:
        print("⚠️  Some tests failed. Please fix the issues before running the GUI.")
        print("\nCommon solutions:")
        print("- Install PyQt5: pip install PyQt5")
        print("- Start Docker Desktop")
        print("- Install Docker Compose")
        print("- Check Python version (3.7+)")

    return tests_passed == total_tests

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
