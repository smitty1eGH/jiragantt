import csv

import pytest

from jiragantt.jiragantt import FIELDS, JiraItem

@pytest.fixture
def data_spec():
    return '/mnt/osis/jira.csv'

def test_main(data_spec):
    jira_items=[]
    with open(data_spec,'r') as csvf:
        tasks=csv.DictReader(csvf)
        for t in tasks:
            jira_items.append(JiraItem(FIELDS,t))
    jira_items.sort(key=lambda x: x.CustomfieldRank)
    print(jira_items[0].__repr__())
    print(jira_items[0])
