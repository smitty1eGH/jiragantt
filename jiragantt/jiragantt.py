import csv
import logging
import logging.config
import re

logging.config.fileConfig("./etc/logging.conf", disable_existing_loggers=False)
logger = logging.getLogger('jiragantt')

NON_CHARS='\W*'

#Field names retrieve directly from the Jira .csv. This list is like an SQL
#  SELECT clause for the  fj
FIELDS=['Summary'                      ,'Issue key'                  ,'Assignee'
       ,'Created'                      ,'Due Date'                   ,'Description'
       ,'Original Estimate'            ,'Remaining Estimate'         ,'Time Spent'
       ,'Outward issue link (Precedes)','Custom field (Epic Link)'   ,'Custom field (Epic Name)'
       ,'Custom field (Rank)'          ,'Custom field (Story Points)'
       ]
#This is the form to return for dumping the Jira item to a straight LaTeX file
LATEX_REPR='''#+LATEX_HEADER: \\usepackage{pgfgantt}
ALL_YOUR_JIRA_ITEMS
#+BEGIN: org-gantt-chart :id "todo-deadlines-schedules"
#+END
'''

#This is the form to return for dumping the Jira item to a .org agenda file
#  Need to group on Epic Name with **
#  And then put out the Summary with ***
ORG_AGENDA=''' '''

class JiraGantt:
    '''Set up a specific .org file for having the Jira data witten as a Gantt.
    '''
    def __init__(self,outfile):
        self.outfile=outfile

    def add_jira_item(self,jira_item):
        pass

    def __str__(self):
        pass


class JiraItem:
    def __init__(self,jira_fields,jira_item):

        def tidy_field(field):
            return re.sub(NON_CHARS,'',field)

        self.tidy_fields={}
        for jf in jira_fields:
            tf = tidy_field(jf)
            self.tidy_fields[tidy_field(tf)] = jf
            setattr(self, tf, jira_item[jf] )

    def __repr__(self):
        return f'{{"Summary":"{self.Summary}"}}'

    def __str__(self):
        return f'The name is {self.Summary}'
