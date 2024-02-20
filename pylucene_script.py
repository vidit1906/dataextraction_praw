#!/usr/bin/env python3
import json
import lucene
import os
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import IndexWriter, IndexWriterConfig, IndexOptions
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.search import IndexSearcher
from java.nio.file import Paths
from lucene import getVMEnv
import argparse

def load_reddit_data(filepath):
    with open(filepath, 'r') as file:
        for line in file:
            yield json.loads(line)

import time
base_dir = 'reddit_lucene_index'
def create_index(dir, data):
    writer = None
    total_time = 0
    #num_documents = 0
    try:
        if not os.path.exists(dir):
            os.mkdir(dir)
        store = SimpleFSDirectory(Paths.get(dir))
        analyzer = StandardAnalyzer()
        config = IndexWriterConfig(analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)
        writer = IndexWriter(store, config)
    
        
        metaType = FieldType()
        metaType.setStored(True)
        metaType.setTokenized(False)
    
        contextType = FieldType()
        contextType.setStored(True)
        contextType.setTokenized(True)
        contextType.setIndexOptions(IndexOptions.DOCS_AND_FREQS_AND_POSITIONS)
    
        for sample in data:
            start_time=time.time()
            subreddit = sample.get('subreddit', '')
            post_title = sample.get('post_title', '')
            post_body = sample.get('post_body', '')  
            parent_comment_id = sample.get('parent_comment_id', '')
            comment_id = sample.get('comment_id', '')
            comment_body = sample.get('body', '')  
    
            doc = Document()
            doc.add(Field('Subreddit', subreddit, metaType))
            doc.add(Field('PostTitle', post_title, metaType))
            doc.add(Field('PostBody', post_body, contextType))  
            doc.add(Field('ParentCommentId', parent_comment_id, metaType))
            doc.add(Field('CommentId', comment_id, metaType))
            doc.add(Field('CommentBody', comment_body, contextType))
            writer.addDocument(doc)
            end_time=time.time()
            total_time+=(end_time - start_time)
            #num_documents += 1
    finally:
        if writer is not None:
            writer.close()
    #avg_time_per_doc = total_time/num_documents if num_documents else 0
    print("total time taken to index(in seconds):", total_time )
    writer.close()

def retrieve(storedir, query):
    searchDir = SimpleFSDirectory(Paths.get(storedir))
    searcher = IndexSearcher(DirectoryReader.open(searchDir))
    parser = QueryParser('CommentBody', StandardAnalyzer())  
    parsed_query = parser.parse(query)

    topDocs = searcher.search(parsed_query, 5).scoreDocs
    topkdocs = []
    for hit in topDocs:
        doc = searcher.doc(hit.doc)
        topkdocs.append({
            "score": hit.score,
            "subreddit": doc.get("Subreddit"),
            "post_title": doc.get("PostTitle"),
            "post_body": doc.get("PostBody"),  
            "parent_comment_id": doc.get("ParentCommentId"),  
            "comment_id": doc.get("CommentId"),  
            "comment_body": doc.get("CommentBody")
        })
    
    return topkdocs

reddit_data = load_reddit_data('./reddit_comments_duplicates_final.json')
lucene.initVM(vmargs=['-Djava.awt.headless=true'])
create_index('reddit_lucene_index_copy/', reddit_data)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Lucene Search')
    parser.add_argument('query', type=str, help='Search query')
    args = parser.parse_args()
    results = retrieve('reddit_lucene_index_copy/', args.query)
    print(results)


else:
    print("Please enter valid query")