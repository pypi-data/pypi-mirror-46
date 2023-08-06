import json


def confluent_error_transform(err):
    pass


def kafka_python_error_transform(err):
    pass


def serializer(msg):
    return json.dumps(msg)


def deserializer(msg):
    return json.loads(msg)

