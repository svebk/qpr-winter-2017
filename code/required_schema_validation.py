import json
import sys

# Define what team's submission is being validated
team_A_submission_file = sys.argv[1]

# Load team submission
team_A_submission = []
with open(team_A_submission_file, 'r') as f:
    for line in f:
        entry = json.loads(line)
        team_A_submission.append(entry)
        
# Validate team submission
fail = 0
for entry in team_A_submission:
    if 'cluster_id' not in entry.keys():
        print "CODE BREAKING ERROR: 'cluster_id' field missing.  Submission is not valid."
        fail = 1
    if 'score' not in entry.keys():
        print "CODE BREAKING ERROR: 'score' field missing.  Submission is not valid."
        fail = 1
    if type(entry['score']) != float and type(entry['score']) != int:
        print "CODE BREAKING ERROR: 'score' not a real number or integer.  Submission is not valid."
        fail = 1
    if entry['score'] < 0.0 or entry['score'] > 1.0:
        print "WARNING: 'score' not between 0.0 and 1.0 as expected."

if fail == 0:
    print "Submission format is valid."
else:
    print "CODE BREAKING ERROR: Check commment(s) above. Submission is not valid."
