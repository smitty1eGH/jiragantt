import csv
import logging
import logging.config
import re

logging.config.fileConfig("./etc/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger("jiragantt")

NON_CHARS = "\W*"

# Field names retrieve directly from the Jira .csv. This list is like an SQL
#  SELECT clause for the  fj
FIELDS = [
    "Summary",
    "Issue key",
    "Assignee",
    "Created",
    "Due Date",
    "Description",
    "Original Estimate",
    "Remaining Estimate",
    "Time Spent",
    "Outward issue link (Precedes)",
    "Custom field (Epic Link)",
    "Custom field (Epic Name)",
    "Custom field (Rank)",
    "Custom field (Story Points)",
]

# Name of generic epic
CATCH_ALL = "catch_all"

# This is the form to return for dumping the Jira item to a straight LaTeX file
LATEX_REPR = """#+LATEX_HEADER: \\usepackage{pgfgantt}
ALL_YOUR_JIRA_ITEMS
#+BEGIN: org-gantt-chart :id "todo-deadlines-schedules"
#+END
"""

# This is the form to return for dumping the Jira item to a .org agenda file
#  Need to group on Epic Name with **
#  And then put out the Summary with ***
ORG_AGENDA = """ """


class JiraGantt:
    """Set up a specific .org file for having the Jira data witten as a Gantt.
    """

    def __init__(self, out_file):
        self.out_file = out_file
        self.jira_epics = set()
        self.jira_items = {}
        self.epics2items = set()

    def add_jira_item(self, jira_item):
        ji = JiraItem(FIELDS, jira_item)
        ji_epic = ji.epic_name
        ji_rank = ji.jira_rank
        if ji.epic_name not in self.jira_epics:
            self.jira_epics.add(ji.epic_name)
        self.epics2items.add((ji_epic, ji_rank))
        self.jira_items[ji_rank] = ji

    def all_your_jira_items(self):
        '''Roll up the list of jira items do as a list comprehension, maybe make a generator
        '''
        output = []
        for epic in self.jira_epics:

            output.append(f'** {epic}')

            items = [item for item in self.epics2items if item[0] == epic]

            for item in items:
                output.append(item.__str__())

        return '\n'.join(output)

    def publish(self):
        """Output a .org file suitable to ganttify
        """
        with open(self.out_file,'w') as f:
            f.write(LATEX_REPR.replace('ALL_YOUR_JIRA_ITEMS',self.all_your_jira_items()))



class JiraItem:
    def __init__(self, jira_fields, jira_item):
        self.tidy_fields = {}
        for jf in jira_fields:
            tf = self.tidy_field(jf)
            self.tidy_fields[self.tidy_field(tf)] = jf
            setattr(self, tf, jira_item[jf])

    def tidy_field(self,field):
        return re.sub(NON_CHARS, "", field)

    @property
    def epic_name(self):
        return getattr(self, self.tidy_fields[self.tidy_field("Custom field (Epic Name)")], CATCH_ALL)

    @property
    def jira_rank(self):
        return getattr(self, self.tidy_fields[self.tidy_field("Custom field (Rank)")],'0')

    def __repr__(self):
        '''Put out a straight pgfgantt representation of the item.
        '''
        return f'{{"Summary":"{self.Summary}"}}'

    def __str__(self):
        '''Put out an org-gantt ready version
        '''
        return f"*** {self.Summary}"

def jira_csv_to_org(data_spec, out_file):
    '''Transform the file DATA_SPEC to OUT_FILE

    '''
    jg = JiraGantt(out_file)
    with open(data_spec, "r") as csvf:
        tasks = csv.DictReader(csvf)
        for t in tasks:
            jg.add_jira_item(t)
    jg.publish()
