#!/usr/bin/env python

import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, roc_auc_score
import sys
import json

# how to use: python CP1_eval_script.py ground_truth_sample_CP1.json submission_sample_CP1.json output_sample_CP1.pdf output_cg_chart.pdf

################################################
# group data ingest - edit to fit your data as needed
sub_id = []
sub_scores = []
sub_outputs = open(sys.argv[2], "r")
for line in sub_outputs:
    entry = json.loads(line)
    sub_id.append(entry['cluster_id'])
    sub_scores.append(entry['score'])
sub_outputs.close()
################################################

################################################
# do not edit - eval data
gt_id = []
gt_scores = []
gt_outputs = open(sys.argv[1], "r")
for line in gt_outputs:
    entry = json.loads(line)
    if entry['cluster_id'] in sub_id:
        gt_id.append(entry['cluster_id'])
        gt_scores.append(entry['score'])    
gt_outputs.close()
################################################

################################################
def cg_chart(gt_id0, gt_scores0, sub_id0, sub_scores0):

    ############################################
    # create dictionaries to match ID to scores (both gt_score and sub_score)
    gt_dict = {}
    for i in xrange(0,len(gt_id0)):
        gt_dict[gt_id0[i]] = {}
        gt_dict[gt_id0[i]]["gt"] = gt_scores0[i]
    for i in xrange(0,len(sub_id0)):
        if not gt_dict.has_key(sub_id0[i]):     # this should be redundant (line 96), but just playing it safe
            print "GROUND TRUTH MISSING SUBMISSION ID: ", sub_id0[i], ". REMOVING ITEM."
            sub_id0.remove(sub_id0[i])
            continue
        else:
            gt_dict[sub_id0[i]]["sub"] = sub_scores0[i]

    ############################################
    # sort user-submitted IDs/predictions by their probability of class 1
    sub_id0, sub_scores0 = zip(*sorted(zip(sub_id0, sub_scores0), key=lambda(x):x[1])) 
    
    ############################################
    # map to x, y data for a chart
    x = []
    y = []
    y_random = []
    y_perfect = []
    i = 0
    j = 0
    for item in sub_id0[::-1]:
        x.append(i+1)
        j += gt_dict[item]["gt"]
        y.append(j)
        i += 1
        
    ############################################
    # create benchmark (straight line)
    for item in x:
        y_random.append(item * float(max(y)) / float(len(x)))
    for item in x:
        if item <= max(y_random):
            y_perfect.append(item)
        else:
            y_perfect.append(max(y_random))
    ############################################
    # plot
    fig = plt.figure()
    plt.plot(x, y, '-', x, y_random, 'r--', x, y_perfect, 'b--')
    title = 'Cumulative Gains Chart'
    plt.title(title)
    plt.ylabel("Cumulative True Positives")
    plt.xlabel("Cumulative IDs (Sorted by Prediction Confidence)")
    plt.axis([0, 130, 0, 40])
    #plt.show()
    plt.savefig(sys.argv[4])
################################################    
    
################################################
# note that if you did not include ids but instead only phone numbers in your file, the below needs modification
# align ground truth and submission by cluster_id

gt_id, gt_scores = zip(*sorted(zip(gt_id, gt_scores), key=lambda(x):x[0]))
sub_id, sub_scores = zip(*sorted(zip(sub_id, sub_scores), key=lambda(x):x[0]))

if len(gt_scores) != len(sub_scores):
    print ('submission line total {} does not match expected {}'.format(len(sub_scores), len(gt_scores)))

elif any([a != b for a, b in zip(sub_id, gt_id)]):
    print  ('submission ids do not match ground truth ids, please check submission data')
################################################ 

else:
    cg_chart(gt_id, gt_scores, sub_id, sub_scores)
    fpr ,tpr, thresholds = roc_curve(gt_scores, sub_scores)
    auc = roc_auc_score(gt_scores, sub_scores)
    fig = plt.figure()
    plt.plot(fpr, tpr, '.-')
    plt.xlim(-0.01, 1.01)
    plt.ylim(-0.01, 1.01)
    title = 'ROC-AUC = {0}'.format(auc)
    plt.title(title)
    plt.ylabel("True Positive Rate")
    plt.xlabel("False Positive Rate")
    plt.savefig(sys.argv[3])
