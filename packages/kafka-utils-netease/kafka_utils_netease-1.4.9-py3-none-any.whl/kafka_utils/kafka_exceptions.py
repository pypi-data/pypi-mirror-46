class KafkaExceptions(Exception):
    pass


class PartitionCreationException(KafkaExceptions):
    pass


class BufferFullException(KafkaExceptions):
    pass


class ProduceFailException(KafkaExceptions):
    pass


class GetMetaDataFailException(KafkaExceptions):
    pass
