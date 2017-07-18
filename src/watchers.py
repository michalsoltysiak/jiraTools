'''
Created on Jul 18, 2017

@author: slsm
'''

from jira import JIRA
import sys



import argparse


def parseCommandLine(argv):
    dictArgs = dict({'user':'', 'password':'', 'key':'', 'inputFile':'', 'server':'', 'epics':False})
    parser = argparse.ArgumentParser(description='Transfers TestRail test cases from csv file to specified TestFLO project in Jira.')
    parser.add_argument('-s', '--server', metavar='server-url', nargs=1, required=True, type=str, help='url of your jira server, including http(s)://')
    parser.add_argument('-k', '--key', metavar='PROJECTKEY', nargs=1, required=True, type=str, help='project KEY, not name, not id, the KEY')
    parser.add_argument('-u', '--user', metavar='username', nargs=1, required=True, type=str, help='your jira user name')
    parser.add_argument('-p', '--pass', metavar='password', nargs=1, required=True, type=str, help='your jira passowrd')
    args = vars(parser.parse_args())
    dictArgs['user'] = args['user'][0]
    dictArgs['password'] = args['pass'][0]
    dictArgs['key'] = args['key'][0]
    dictArgs['server'] = args['server'][0]
    
    return dictArgs

if __name__ == "__main__":
    parsedArgs = parseCommandLine(sys.argv[1:])


    jira = JIRA(parsedArgs['server'], basic_auth=(parsedArgs['user'], parsedArgs['password']))
 
    issues = jira.search_issues('watcher = currentUser() and project != "Vitotrol 300C"  and statusCategory not in (Done)')
    for issue in issues:
        watcher = jira.watchers(issue)
        user = parsedArgs['user']
        for watcher in watcher.watchers:
            if watcher.key is parsedArgs['user']:
                user = watcher.name
        print('removing watcher from issut %s' % issue.key)
        result = jira.remove_watcher(issue, user)

    
