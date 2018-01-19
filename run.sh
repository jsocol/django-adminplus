#!/bin/bash

export PYTHONPATH=".:$PYTHONPATH"
export DJANGO_SETTINGS_MODULE="test_settings"

usage() {
    echo "USAGE: $0 [command]"
    echo "  test - run the adminplus tests"
    echo "  check - run flake8 checks"
    echo "  shell - open the Django shell"
    exit 1
}

case "$1" in
    "test" )
        django-admin.py test adminplus ;;
    "check" )
        flake8 adminplus/ --exclude=tests*.py ;;
    "shell" )
        django-admin.py shell ;;
    * )
        usage ;;
esac
