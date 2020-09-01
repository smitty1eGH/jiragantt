import csv

import pytest

from jiragantt.jiragantt import FIELDS, JiraItem, JiraGantt,jira_csv_to_org


@pytest.fixture
def data_spec():
    return "/mnt/osis/jira.csv"

@pytest.fixture
def out_file(tmp_path):
    return f'{tmp_path}/asdf.org'

def test_jira_item(data_spec):
    jira_items = []
    with open(data_spec, "r") as csvf:
        tasks = csv.DictReader(csvf)
        for t in tasks:
            jira_items.append(JiraItem(FIELDS, t))
    jira_items.sort(key=lambda x: x.CustomfieldRank)
    print(jira_items[0].__repr__())
    print(jira_items[0])

def test_jira_csv_to_org(data_spec, out_file):
    jira_csv_to_org(data_spec, out_file)
