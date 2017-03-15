
# coding: utf-8

# ## Face detection
# The goal of this notebook is to detect faces in all the images associated to the set of ads provided for the CP1 during the MEMEX Winter QPR 2017.
# 
# ### Inputs
# 1. image_url_sha1.csv
# This is a mapping of the URLs images to their SHA1, the images in this file have been downloaded and their SHA1 computed properly.
# The corresponding images should be stored locally
# 
# ### Outputs
# 1. faces.jl   
# These are all the faces detected in the images related to all of the ads in the input.    
# 
# 
# ### Requirements
# jq and parallel
# 
#     sudo apt-get install parallel
#     
# facenet repository: https://github.com/svebk/facenet

# In[1]:

import os
from subprocess import call

#facesearch_dir = "ColumbiaFaceSearch"
facesearch_dir = "facesearch"
# set some path parameters
input_dir = "../data/"
FACENET_DIR = "../../../"+facesearch_dir+"/facenet/"
DATA_DIR = "../../../"+facesearch_dir+"/data"
prefix = "train"
input_file = os.path.join(input_dir,prefix+"_image_url_sha1.csv")
IMAGE_DIR = os.path.join(input_dir,prefix+'_images')


# In[2]:

# get just sha1 list
IMAGE_SHA1S = os.path.join(input_dir,prefix+"_image_sha1_list.csv")
#get_ipython().system(u"cat $input_file | cut -d ',' -f2 | sort | uniq > $IMAGE_SHA1S")
#call("cat {} | cut -d ',' -f2 | sort | uniq > {}".format(input_file, IMAGE_SHA1S))
cmd = "cat {} | cut -d ',' -f2 | sort | uniq > {}".format(input_file, IMAGE_SHA1S)
print cmd
call(cmd, shell=True)

DETECTED_FACES = os.path.join(input_dir,prefix+"_faces.jl")
FACES_JOBLOG = prefix+"_faces.joblog"


# In[3]:

# find faces in images of ads
#get_ipython().system(u'parallel --joblog $FACES_JOBLOG           --retries 0           --arg-file $IMAGE_SHA1S           --max-args 200           --jobs 2         python ../scripts/detect_face.py $FACENET_DIR $DATA_DIR $IMAGE_DIR > $DETECTED_FACES')
#call('parallel --joblog $FACES_JOBLOG --retries 0 --arg-file $IMAGE_SHA1S --max-args 200 --jobs 30 python ../scripts/detect_face.py $FACENET_DIR $DATA_DIR $IMAGE_DIR > $DETECTED_FACES')
set_env = 'source activate facesearch; parallel --record-env; '
cmd = 'parallel --env _ --joblog {} --retries 0 --arg-file {} --max-args 100 --jobs 30 python ../scripts/detect_face.py {} {} {} > {}'.format(FACES_JOBLOG, IMAGE_SHA1S, FACENET_DIR, DATA_DIR, IMAGE_DIR, DETECTED_FACES)
print cmd
call(set_env+cmd, shell=True, executable='/bin/bash')


# In[ ]:



