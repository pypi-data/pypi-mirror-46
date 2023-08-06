#!/usr/bin/python
# -*- coding: UTF-8 -*-
from pathlib import Path
from sekg.util.annotation import catch_exception
from gensim.summarization.bm25 import BM25
from sekg.ir.doc.wrapper import PreprocessMultiFieldDocumentCollection
from sekg.ir.models.base import DocumentSimModel
import pickle
import gensim
import numpy as np


class BM25Model(DocumentSimModel):
    """
    This class is used the BM25 model to compute the document similarity score.
    The implementation from BM25 is from gensim.
    """
    __bm25_model_name__ = "bm25.model"
    __doc_collection_name__ = "doc.pre.collection"

    def __init__(self, name, model_dir_path, **config):

        """
        init the model with model_dir_path:
        """
        super().__init__(name, model_dir_path, **config)

        self.bm25_model = None
        self.corpus = None
        self.__init_sub_model_path__()

        self.preprocessor = None
        self.preprocess_doc_collection = None

    def __init_sub_model_path__(self):
        if self.model_dir_path is None:
            return
        model_dir = Path(self.model_dir_path)
        self.bm25_model_path = str(model_dir / self.__bm25_model_name__)
        self.entity_collection_path = str(model_dir / self.__doc_collection_name__)
        model_dir.mkdir(parents=True, exist_ok=True)

    def init_model_as_submodel(self):
        """
        init the model
        :return:
        """
        self.init_model()

    @catch_exception
    def init_model(self):
        """
        init the model
        :return:
        """
        self.__init_sub_model_path__()
        print("loading the bm25 models")
        fr = open(self.bm25_model_path, 'rb')
        self.bm25_model = pickle.load(fr)
        fr.close()
        preprocess_doc_collection = PreprocessMultiFieldDocumentCollection.load(self.entity_collection_path)
        self.__init_document_collection(preprocess_doc_collection)

    def __init_document_collection(self, preprocess_doc_collection):
        self.preprocess_doc_collection = preprocess_doc_collection
        self.preprocessor = self.preprocess_doc_collection.get_preprocessor()
        self.field_set = self.preprocess_doc_collection.get_field_set()

    def train_from_document_collection(self, preprocess_document_collection):
        print("start training")
        self.__init_document_collection(preprocess_document_collection)
        corpus_clean_text = []
        preprocess_multi_field_doc_list = preprocess_document_collection.get_all_preprocess_document_list()

        for docno, multi_field_doc in enumerate(preprocess_multi_field_doc_list):
            corpus_clean_text.append(multi_field_doc.get_document_text_words())
        print("corpus len=%d" % len(corpus_clean_text))
        self.corpus = corpus_clean_text
        print("bm25 Training...")
        self.bm25_model = gensim.summarization.bm25.BM25(corpus=self.corpus)
        print("bm25 compelete...")

    def train_from_doc_collection_with_preprocessor(self, doc_collection: PreprocessMultiFieldDocumentCollection,
                                                    **config):
        if isinstance(doc_collection, PreprocessMultiFieldDocumentCollection):
            self.train_from_document_collection(preprocess_document_collection=doc_collection)

    @catch_exception
    def save(self, model_dir_path):
        """
        save model to the model_dir_path
        :param model_dir_path: the dir to save the model
        :return:
        """
        super().save(model_dir_path)
        self.__init_sub_model_path__()

        print("save bm25 model into ", self.bm25_model_path)
        fw = open(self.bm25_model_path, 'wb')
        pickle.dump(self.bm25_model, fw)
        fw.close()

        print("entity collection saving...")
        self.preprocess_doc_collection.save(self.entity_collection_path)
        print(
            "entity collection finish saving , save to %s, %r" % (
                self.entity_collection_path, self.preprocess_doc_collection))

    def get_full_doc_score_vec(self, query):
        """
        score vector is a vector v=[0.5,2.0,3.0], v[0] means that the document 'd' whose index is 0 in document collection, its score with query is 0.5.
        :param query: a str stands for the query.
        :return: get all document similar score with query as a numpy vector.
        """

        full_entity_score_vec = self.get_cache_score_vector(query)
        if full_entity_score_vec is not None:
            return full_entity_score_vec

        query_words = self.preprocessor.clean(query)
        # average_idf = sum(map(lambda k: float(self.bm25_model.idf[k]), self.bm25_model.idf.keys())) / len(
        #     self.bm25_model.idf.keys())
        full_entity_score_vec = np.array(self.bm25_model.get_scores(query_words))
        self.cache_entity_score_vector(query, full_entity_score_vec)
        return full_entity_score_vec

    def similarity_4_doc_id_pair(self, doc_id1, doc_id2):
        if doc_id1 not in self.doc_id_2_doc_index_map or doc_id2 not in self.doc_id_2_doc_index_map:
            return 0
        pos1 = self.doc_id_2_doc_index_map[doc_id1]
        pos2 = self.doc_id_2_doc_index_map[doc_id2]
        return self.bm25_model.get.similarity_by_id(pos1)[pos2]
