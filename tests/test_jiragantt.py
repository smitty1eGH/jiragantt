import pytest

from jiragantt.jiragantt import main

def test_main():
    assert main() == "Hello, world."
