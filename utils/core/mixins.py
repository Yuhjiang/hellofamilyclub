class MultiActionConfViewSetMixin:
    """
    重写获取相应配置的方法，需要在view中写对应的dict，映射action name(key)到配置的class(value)
    以serializer为例
    i.e.:

    class MyViewSet(MultiSerializerViewSetMixin, ViewSet):
        serializer_class = MyDefaultSerializer
        serializer_action_classes = {
           'list': MyListSerializer,
           'my_action': MyActionSerializer,
        }

        @action
        def my_action:
            ...

    如果没有找到action的入口，则回退到常规的get_serializer_class
    lookup: self.serializer_class, MyDefaultSerializer.
    配置对应的dict为
    get_serializer_class() : serializer_action_classes
    get_permission_class() : permission_action_classes

    Thanks gonz: http://stackoverflow.com/a/22922156/11440
    """
    serializer_action_classes = {}
    permission_action_classes = {}
    queryset_action_classes = {}

    def get_serializer_class(self):

        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiActionConfViewSetMixin,
                         self).get_serializer_class()

    def get_permissions(self):

        try:
            return [permission() for permission in
                    self.permission_action_classes[self.action]]
        except (KeyError, AttributeError):
            return super(MultiActionConfViewSetMixin, self).get_permissions()

    def get_queryset(self):
        try:
            return self.queryset_action_classes[self.action]
        except (KeyError, AttributeError):
            return super().get_queryset()