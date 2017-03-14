"""
  Defines configuration variables and reads configuration file.
"""

import json

class ConfigCP1():

  cp1_positive_fn = 'CP1_train_ads_bylead.json'
  cp1_negative_fn = 'cp1_negative_train_UPDATED.json'
  # Assuming running directory will be 'scripts'
  # base data_gt dir.
  gt_dir = '../data_gt'
  # This would contain connections information and thus should not be commited
  config_fn = '../memex_cp1_images_pkg/conf/config.json'
  # CDR infos to be read from config file
  es_host = None
  es_port = None
  es_index = None
  es_doc_type = None
  es_user = None
  es_pass = None

  def __init__(self):
      """
        Initialize configuration.
      """
      self.read_conf(self.config_fn)

  def read_conf(self, config_fn):
      """
        Read configuration file provided.

      Args:
        config_fn: json configuration file.
      """
      json_conf = json.load(open(config_fn,'rt'))
      self.es_host = json_conf['es_host']
      self.es_port = json_conf['es_port']
      self.es_index = json_conf['es_index']
      self.es_doc_type = json_conf['es_doc_type']
      self.es_user = json_conf['es_user']
      self.es_pass = json_conf['es_pass']

