class DictMixin:
    """  Доступ к полям объекта через ['field']  """

    def __getitem__(self, item):
        return getattr(self, item)
