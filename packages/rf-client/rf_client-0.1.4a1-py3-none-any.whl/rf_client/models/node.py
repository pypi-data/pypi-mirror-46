from typing import Optional, List, Dict

from dateutil import parser

from rf_client.exceptions import NodeNotFound, RFApiError
from rf_client.utils import DictMixin


class Node(DictMixin):
    """
    Модель узла
    """
    class Properties(DictMixin):
        """
        Свойства узла. Состоят из групп
        """
        def __init__(self, properties):
            if properties is None:
                properties = {}

            self.byUser = properties.get('byUser', [])  # todo map to OrderedDict
            self.byType = properties.get('byType', {})
            self.global_ = properties.get('global', {})
            self.style = properties.get('style', {})

        def __str__(self):
            return str(dict({
                'byUser': self.byUser,
                'byType': self.byType,
                'global': self.global_,
                'style': self.style
            }))

    class Body(DictMixin):
        """ Тело узла """
        def __init__(self, id, type_id=None, properties=None, parent=None, children=None, parent_node=None,
                     unread_comments_count=None, ids_to_nodes=None, **kwargs):

            assert ids_to_nodes is not None  # fixme

            self.id = id
            self.type_id = type_id
            self.properties = Node.Properties(properties)
            self.parent = parent

            self.unread_comments_count = unread_comments_count

            if children:
                self.children = [
                    Node(**node_dict, parent_node=parent_node, ids_to_nodes=ids_to_nodes) for node_dict in children
                ]
            else:
                self.children = []

        def __repr__(self):
            return f"Body('{self.id}', ...)"

    class Meta(DictMixin):
        """ Метаданные узла """

        # fixme editable and commentable
        def __init__(self, creation_timestamp, last_modified_timestamp, last_modified_user, author, **kwargs):
            try:
                self.creation_timestamp = parser.parse(creation_timestamp) if creation_timestamp else None
                self.last_modified_timestamp = parser.parse(last_modified_timestamp) if last_modified_timestamp else None
            except ValueError:
                raise RFApiError("Wrong datetime response format")

            self.last_modified_user = last_modified_user
            self.author = author

        def __str__(self):
            return str({
                'creation_timestamp': self.creation_timestamp,
                'last_modified_timestamp': self.last_modified_timestamp,
                'last_modified_user': self.last_modified_user,
                'author': self.author
            })

    def __init__(self, id, map_id, meta, position, body, parent, originalParent, hidden, properties=None,
                 unread_comments_count=None,
                 parent_node=None,
                 ids_to_nodes=None, **kwargs):

        assert ids_to_nodes is not None  # fixme
        self.ids_to_nodes: Dict[str, Node] = ids_to_nodes
        self.ids_to_nodes[id] = self

        self.id = id
        self.map_id = map_id
        self.meta = Node.Meta(**meta)
        self.position = position
        self.properties = Node.Properties(properties)
        self.parent = parent  # это id предка, так сделано из-за формата ответа с сервера
        self.parent_node = parent_node  # это ссылка на предка Node
        # fixme
        self.originalParent = originalParent

        self.unread_comments_count = unread_comments_count
        self.hidden = hidden

        body_id = body['id']

        self._is_link = body_id != self.id

        if not self._is_link:
            self.body = Node.Body(**body, parent_node=self, ids_to_nodes=ids_to_nodes)  # fixme
        else:
            self.body = Node.Body(body_id, ids_to_nodes=ids_to_nodes)  # fixme

    @property
    def is_link(self):
        return self._is_link

    def __repr__(self):
        title = self.body.properties.global_.get('title', 'N/A')
        title = title[:100] + '...' if len(title) > 100 else title
        return f"Node('{self.id}', '{self.body.id}', '{title}')"

    def find(self, type_id: Optional[str]) -> Optional['Node']:
        """
        Найти первого потомка с указанным типом. Понятие "первый" означает лишь любого, кто попадется первым.
        :return None | Node
        """
        def dive(children: List[Node]):
            for node in children:
                if node.is_link:
                    continue  # fixme

                if node.body.type_id == type_id:
                    return node
                else:
                    result = dive(node.body.children)
                    if result:
                        return result

        return dive(self.body.children) if self.body.type_id is not type_id else self

    def find_by_id(self, id: str) -> Optional['Node']:
        """
        Найти первого потомка с указанным id. Понятие "первый" означает лишь любого, кто попадется первым.
        :return None | Node
        """
        try:
            target_node = self.ids_to_nodes[id]
            if self in target_node.get_parents():
                return target_node
            else:
                return None
        except KeyError:
            return None

    def find_all(self, type_id: Optional[str]) -> List['Node']:
        """
        Тоже, что и find, но не останавливаемся на первом найденном, а возвращает список потомков узла
          с определенным типом.

        :return [] | [Node, ...]
        """
        def dive(children: List[Node]):
            result = []
            for node in children:
                if node.is_link:
                    continue  # fixme в нашем дереве появляется цикл из-за ссылок!
                if node.body.type_id == type_id:
                    result.append(node)

                t = dive(node.body.children)
                result += t if t is not None else []

            return result

        t = dive(self.body.children)
        return t if t is not None else []

    def find_closest_parent(self, type_id: str) -> 'Node':
        """
        Найти ближайшего предка опредленного типа type_id узла node_id.
        """
        cur = self
        while cur.body.type_id != type_id:
            cur = cur.parent_node
            if cur is None:  # Если дошли до корня
                raise NodeNotFound()

        return cur

    def get_parents(self) -> List['Node']:
        """
        Получить список родителей узла. Порядок - от узла к корню, не включая себя.
        """
        result = []
        cur = self
        while cur.parent_node is not None:
            cur = cur.parent_node
            result.append(cur)

        return result
