#!/usr/bin/env python3
"""
Ejecuta todos los tests del proyecto.
Uso: python tests/run_tests.py
"""
import unittest, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

loader = unittest.TestLoader()
suite = loader.discover(str(Path(__file__).parent), pattern="test_*.py")

runner = unittest.TextTestRunner(verbosity=2)
result = runner.run(suite)
sys.exit(0 if result.wasSuccessful() else 1)
