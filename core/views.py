
class MultiSerializerMixin:  # pylint:disable=too-few-public-methods
    """
    Get specified serializer from array.
    """
    serializers = {
        'default': None,
    }

    def get_serializer_class(self):
        """
        Function get serializer for every specific action

        :return: Serializer described in serializers dict
        """
        try:
            serializer_class = self.serializers[self.action]
        except KeyError:
            serializer_class = self.serializers['default']
        return serializer_class
