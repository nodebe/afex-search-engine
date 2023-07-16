#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import nltk


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'searchengine.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc

    download_punkt()
    execute_from_command_line(sys.argv)

def download_punkt():
    print("Checking/Downloading Punkt File for Filtering in system.")
    nltk.download('punkt')

if __name__ == '__main__':
    main()
