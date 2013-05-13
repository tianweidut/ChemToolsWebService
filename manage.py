#!/usr/bin/env python

from django.core.management import execute_manager

try:
    import settings_dev
except ImportError, err:
    import sys
    sys.stderr.write("Manage import Error\n")
    sys.stderr.write(str(err)+"\n")
    sys.exit(1)

if __name__ == "__main__":
    execute_manager(settings_dev)
