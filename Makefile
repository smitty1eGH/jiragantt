.PHONY: help eserv ecli b c t tidy ddb install reqsFr reqsInst
.DEFAULT_GOAL := help

FILES=`find . -type f -name "*.py"`

help:
	@echo ""
	@echo "Handy project commands. make <target>:"
	@echo ""
	@echo "target   | description"
	@echo "---------+------------"
	@echo "b          fix style with black"
	@echo "c          check typing with mypy"
	@echo "t          run tests quickly with the default Python"
	@echo "tidy       fix style, type check, and test"
	@echo "reqsFr     freeze requirements.txt in etc"
	@echo "reqsInst   install requirements.txt in etc"
	@echo ""

b:
	@python -m black --config etc/pyproject.toml $(FILES)
c:
	@python    mypy  --config-file etc/mypy.ini  $(FILES)
t:
	@python -m pytest -c etc/pytest.ini tests --capture=no
reqsFr:
	@pip freeze > etc/requirements.txt
reqsInst:
	@pip install -r etc/requirements.txt
