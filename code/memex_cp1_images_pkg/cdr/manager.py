"""
  Interact with the CDR to get the images infos.
"""

# docs at http://elasticsearch-py.readthedocs.io/en/master/
from elasticsearch import Elasticsearch
import certifi

#import json
#from ..conf.config import ConfigCP1

class CDRManager(object):

  es = None

  def __init__(self, conf_cp1):
      """
      Initialize ElasticSearch object

      :param conf_cp1 (ConfigCP1): configuration class containing connections information.
      """
      self.es = Elasticsearch('https://'+conf_cp1.es_user+':'+conf_cp1.es_pass+'@'+conf_cp1.es_host+':'+str(conf_cp1.es_port))
      self.es_index = conf_cp1.es_index
      self.es_doc_type = conf_cp1.es_doc_type
      # set useful fields from CDR
      self.fields_cdr = ["obj_stored_url", "obj_parent", "obj_original_url"]
      self.batch_size = 200
      # prepare templates for list query
      self.list_query_left = "{\"fields\": [\""+"\", \"".join(self.fields_cdr)+"\"], \"query\": {\"bool\": {\"should\": ["
      self.list_query_right = "]}}, \"size\": "+str(self.batch_size)+" }"
      # prepare templates for single query
      self.single_query_left = "{\"fields\": [\""+"\", \"".join(self.fields_cdr)+"\"], \"query\": {\"filtered\": {\"query\": "
      self.single_query_right = "}}, \"size\": "+str(self.batch_size)+" }"


  def build_match_query_list(self, obj_parent_list):
      """
      Build inner part of ES match query.

      :param obj_parent_list:
      :return:
      """
      # template for one obj_parent_id
      match_template_left = "{\"match\": {\"obj_parent\": \""
      match_template_right = "\" }}"
      # apply it to all obj_parent_ids
      match_query_list = []
      for obj_parent_id in obj_parent_list:
        one_match = match_template_left+str(obj_parent_id)+match_template_right
        match_query_list.append(one_match)
      # returns a comma separeted match list
      return ', '.join(match_query_list)

  def build_query_obj_parent(self, obj_parent_id):
      """
      Query for images of the 'obj_parent_id' (which could be a list)

      :param obj_parent_id:
      :return: dictionary with the images infos of that ad.
      """
      if type(obj_parent_id) == list:
        # build list query
        match_list_query = self.build_match_query_list(obj_parent_id)
        return self.list_query_left+match_list_query+self.list_query_right
      else:
        # build single query
        match_single_query = self.build_match_query_list([obj_parent_id])
        return self.single_query_left+match_single_query+self.single_query_right

  def query_obj_parent(self, obj_parent_id):
      query = self.build_query_obj_parent(obj_parent_id)
      print("[CDRManager: query] {}".format(query))
      response = self.es.search(index=self.es_index, doc_type=self.es_doc_type, body=query, search_type="scan", scroll="5m")
      print("[CDRManager: log] Got "+str(response['hits']['total'])+" results in "+str(response['took'])+"ms.")
      return response




