from uuid import uuid4, UUID

from bson import Binary, binary
from cocktail_apikit import DictMongoQueryBuilder


def test_dict_mongo_query_builder(demo_schema):
    id_value = str(uuid4())
    query_dict = {'name__eq': 'demo', 'id__ne': id_value}

    builder = DictMongoQueryBuilder(query_data=query_dict, schema=demo_schema)

    mongo_query = builder.to_mongo_query()

    print(mongo_query.to_dict())
    mongo_query_dict = mongo_query.to_dict()

    assert mongo_query_dict['name'] == {'$eq': 'demo'}
    assert mongo_query_dict['_id'] == {'$ne': Binary(UUID(id_value).bytes, binary.STANDARD)}

    for key in ['sort', 'projection', 'page', 'limit', 'skip']:
        assert key in mongo_query_dict
