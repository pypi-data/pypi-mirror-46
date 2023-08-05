""" Data Generator for MongoDB """
import math
import numpy as np
from typing import List, Tuple, NoReturn
from random import shuffle

from mlpipe.utils import Config
from mlpipe.data_reader.base_data_generator import BaseDataGenerator
from mlpipe.data_reader.mongodb import MongoDBConnect


class MongoDBGenerator(BaseDataGenerator):
    def __init__(self,
                 col_details: Tuple[str, str, str],
                 doc_ids: List[any] = list(),
                 batch_size: int = 32,
                 processors: List[any] = list(),
                 shuffle_data: bool = True,
                 shuffle_steps: int = 1):
        """
        :param col_details: MongoDB collection details with a tuple of 3 string entries
                            [client name (from config), database name, collection name]
        :param doc_ids: List of doc ids which are used to get the specific data from the MongoDB
        :param batch_size: number of batch size
        :param processors: List of MLPipe data processors
        :param shuffle_data: bool flag to determine if set should be shuffled after epoch is done
        :param shuffle_steps: number of steps that should be shuffled e.g. if fixed length time series are shuffled
        """
        assert (len(col_details) == 3)

        super().__init__(batch_size, processors)
        self.doc_ids = doc_ids
        self.shuffle_data = shuffle_data
        self.shuffle_steps = shuffle_steps
        self.doc_ids = doc_ids
        self.col_details = col_details
        self.collection = None
        self.mongo_con = MongoDBConnect()
        self.mongo_con.add_connections_from_config(Config.get_config_parser())

    def _fetch_data(self, query_docs: list) -> List[any]:
        """
        Get a set of _ids from the database (in order)
        :param query_docs: A list of _ids
        :return: A pymongo cursor
        """
        # to ensure the order of query_docs, use this method. For more details look at this stackoverflow question:
        # https://stackoverflow.com/questions/22797768/does-mongodbs-in-clause-guarantee-order/22800784#22800784
        query = [
            {"$match": {"_id": {"$in": query_docs}}},
            {"$addFields": {"__order": {"$indexOfArray": [query_docs, "$_id"]}}},
            {"$sort": {"__order": 1}}
        ]
        docs = self.collection.aggregate(query)
        return docs

    def __len__(self) -> int:
        """
        :return: Number of batches per epoch
        """
        return int(math.ceil(len(self.doc_ids) / self.batch_size))

    def __getitem__(self, idx):
        """
        Get batch data
        :param idx: current idx in the doc_ids list
        :return: arrays for traning_data (x) and labels (y)
        """

        # Connection should always be established on first __getitem__ class to support multiprocessing
        # every fork needs to have its own database connection
        if self.collection is None:
            self.collection = self.mongo_con.get_collection(*self.col_details)

        batch_ids = self.doc_ids[idx * self.batch_size:(idx + 1) * self.batch_size]
        docs = self._fetch_data(batch_ids)
        batch_x, batch_y = self._process_batch(docs)
        return np.asarray(batch_x), np.asarray(batch_y)

    def on_epoch_end(self):
        """
        Called after each epoch
        """
        if self.shuffle_data:
            if self.shuffle_steps == 1:
                shuffle(self.doc_ids)
            else:
                x = np.reshape(self.doc_ids, (-1, self.shuffle_steps))
                np.random.shuffle(x)
                self.doc_ids = x.flatten().tolist()
