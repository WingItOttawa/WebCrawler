# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import hashlib
import chardet
import os
import git

class WebcrawlerPipeline(object):
    def __init__(self):
        # Create database connection
        # TODO: Hide service-key code away from pipeline code, or at least put it in a function elsewhere
        dir_path = os.path.dirname(os.path.realpath(__file__))
        git_repo = git.Repo(dir_path, search_parent_directories=True)
        git_root_dir = git_repo.git.rev_parse("--show-toplevel")
        service_key_path = os.path.join(git_root_dir, 'wingit-service-key.json')
        cred = credentials.Certificate(service_key_path)
        firebase_admin.initialize_app(cred)
        self.db = firestore.client()

    def process_item(self, item, spider):
        def get_filter_dict():
            content_encoding = chardet.detect(item['content'])['encoding']

            item['content'] = item['content'].decode(content_encoding).encode('ascii', 'ignore')

            id = hashlib.md5(json.dumps(item)).hexdigest()

            filtered_dict_ascii = {
                'content': item['content'],
                'id': id,
                'title': item['current_url'],
                'url': item['current_url'],
            }

            # Return unicode version of filtered_dict_ascii
            return json.loads(json.dumps(filtered_dict_ascii))

        if 'current_url' not in item:
            return

        filter_dict = get_filter_dict()
        filter_dict['wing'] = None
        filter_dict['wingValue'] = None

        doc_ref = self.db.collection(u'filter').document(filter_dict['id'])
        doc_ref.set(filter_dict)
        return item
