from mlpipe.utils import MLPipeLogger, Config
from typing import Tuple
from mlpipe.data_reader.mongodb import MongoDBConnect


def load_ids(col_details: Tuple[str, str, str], data_split: Tuple = (60, 40), sort_by: dict = None, limit: int = None):
    """
    Load MongoDB Document Ids from a collection and split them in training and validation data set
    :param col_details: MongoDB collection details with a tuple of 3 string entries
                        [client name (from config), database name, collection name]
    :param data_split: Tuple of percentage of training and test data e.g. (60, 40) for 60% training and 40% test data
    :param sort_by: MongoDB sort expressiong. e.g. { created_at: -1 }
    :param limit: maximum number of ids that should be fetched
    :return: training and validation data
    """
    MLPipeLogger.logger.info("Loading Document IDs from MongoDB")
    mongo_con = MongoDBConnect()
    mongo_con.add_connections_from_config(Config.get_config_parser())
    collection = mongo_con.get_collection(*col_details)

    db_cursor = collection.find({}, {"_id": 1})
    if sort_by is not None:
        db_cursor.sort(sort_by)
    if limit:
        db_cursor.limit(limit)
    tmp_docs = []
    for doc in db_cursor:
        tmp_docs.append(doc["_id"])

    train_range = int((data_split[0] / 100) * len(tmp_docs))
    train_data = tmp_docs[:train_range]
    val_data = tmp_docs[train_range:]
    MLPipeLogger.logger.info("Documents loaded (train|validation): {0} | {1}\n\n".format(
        len(train_data), len(val_data)))

    return train_data, val_data
