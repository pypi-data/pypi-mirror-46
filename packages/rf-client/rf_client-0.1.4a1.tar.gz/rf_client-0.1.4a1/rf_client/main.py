from random import random
import logging
import ujson
from json import JSONDecodeError
from asyncio import ensure_future

import aiohttp
from aiohttp import ClientSession, BasicAuth, ClientTimeout

from typing import List, Tuple, Optional, Dict

from rf_client.models import Node, NodeType, User
from rf_client.exceptions import *

logger = logging.getLogger('rf_client')

API_BASE_URL = 'http://app.redforester.com/api'


def set_config(api_base_url):
    global API_BASE_URL

    logger.info(f'new api_base_url: {api_base_url}')
    API_BASE_URL = api_base_url

# fixme
class Nodes:
    def __init__(self):
        self._nodes = None

    def _make_tree(self, map_data) -> Node:
        pass

    def get_by_id(self, id: str) -> Node:
        pass

    def get_by_type_id(self, type_id: str) -> Node:
        pass

    def get_all_by_type_id(self, type_id: str):
        pass


class NodeTypes:
    """
    Для болле удобной работы с типами узлов на карте.
    """

    def __init__(self, data):
        self._types = [NodeType(**d) for d in data]

    def find(self, type_name: str) -> 'NodeType':
        for t in self._types:
            if t.name.lower() == type_name.lower():
                return t

        raise NodeTypeNotFound(f'Can not find {type_name} type in map')

    def find_by_id(self, id_: str) -> 'NodeType':
        """
        Поиск типа по его uuid
        :param id_: uuid типа узла
        :return:
        """
        for t in self._types:
            if t.id == id_:
                return t

        raise NodeTypeNotFound(f'Can not find {id_} type in map')


class MapUsers:
    def __init__(self, users):
        self._users = self._data_to_users(users)

    @staticmethod
    def _data_to_users(users_data: List[dict]) -> List[User]:
        users = []
        for ud in users_data:
            users.append(
                User(
                    ud['user_id'],
                    ud['username'],
                    ud['name'],
                    ud['surname'],
                    ud['avatar'],
                    ud['is_admin'],
                    ud['can_export']
                ))

        return users

    def find_by_id(self, id_: str) -> User:
        for u in self._users:
            if u.id == id_:
                return u

        raise UserNotFound()

    def find_by_username(self, username) -> User:
        for u in self._users:
            if u.username == username:
                return u

        raise UserNotFound()


def generate_session_id():
    return str(round(random() * 10 ** 10))


async def get_json(response: aiohttp.ClientResponse):
    try:
        return await response.json()
    except (aiohttp.client_exceptions.ClientResponseError, JSONDecodeError, TypeError, ValueError) as e:
        raw = await response.read()
        logger.exception(f'Response was {raw}')
        raise RFApiError('Invalid JSON response from RF') from e


class MindMap:
    """
    Класс для работы с деревом карты. Подразумевает работу со снапшотом дерева.
    """

    def __init__(self, map_id: str, credentials: Tuple[str, str], view_root_id=None, session_id=None,
                 timeout: ClientTimeout = None):
        """
        :param map_id: id карты
        :param credentials: пара логин, пароль или другие доступные сочетания
        :param view_root_id: если указан, то загрузка будет происходить от этого узла
        :param session_id: id сесси пользователя, можно указать из вне, но это не требуется
        :param timeout: инстанс aiohttp.ClientTimeout
        """
        logger.debug(
            f'Init MindMap ({API_BASE_URL}) with map_id={map_id}, view_root_id={view_root_id}, session_id={session_id}'
        )

        self._api_base_url = API_BASE_URL
        self.id = map_id
        self.view_root_id = view_root_id
        self.root: Node = None
        self.ids_to_nodes: Dict[str, Node] = None
        self.nodes: Nodes = None
        self.types: NodeTypes = None
        self.users: MapUsers = None

        username, password = credentials
        if session_id is None:
            session_id = generate_session_id()
            logger.info(f'Generate new session_id: {session_id}')

        self.session_id = session_id

        if timeout is None:
            timeout = ClientTimeout()

        self._session: ClientSession = ClientSession(
            auth=BasicAuth(login=username, password=password),
            json_serialize=ujson.dumps,
            headers={
                'SessionId': self.session_id
            },
            timeout=timeout
        )

    @staticmethod
    def _make_tree(map_data, ignore_out_of_branch=False) -> Tuple[Node, Dict[str, Node]]:
        """
        Соберем дерево из json, которая пришла,
         основная задача метода - правильно обработать узлы ссылки
        :param map_data: json от сервера с GET /nodes
        :param ignore_out_of_branch: иногда полезно проигнорировать ссылки, которые указывают на узлы, которых у нас нет
        :return: Node - корень дерева
        """
        # индекс узлов по их id, чтобы каждый раз не обходить узлы рекурсивно
        ids_to_nodes = dict()
        link_to_postprocess = []

        def dive(node: Node):
            if node.is_link:
                link_to_postprocess.append((node, node.body.id))

            for c in node.body.children:
                dive(c)

        root = Node(**map_data, parent_node=None, ids_to_nodes=ids_to_nodes)

        dive(root)

        for node, link_id in link_to_postprocess:
            linked_node = root.find_by_id(link_id)
            if linked_node:
                node.body = linked_node.body
            else:
                if not ignore_out_of_branch:  # если ссылка вне доступной части карты
                    raise NodeNotFound('Link not found')

        return root, ids_to_nodes

    async def init(self) -> 'MindMap':
        """
        Ленивая инициализация, потом учто конструктор не может быть async
        """
        path = ('/' + self.view_root_id) if self.view_root_id else ''
        async with self._session.get(f'{self._api_base_url}/maps/{self.id}/nodes{path}') as response:
            map_data = await get_json(response)

            if response.status == 401:
                raise RFApiError(f"Unauthorized:\n{map_data}")
            elif response.status == 403:
                raise RFApiError(f"Forbidden:\n{map_data}")
            elif response.status >= 400:
                raise RFApiError(f"Other RF API Error:\n{map_data}")

        async with self._session.get(f'{self._api_base_url}/maps/{self.id}/node_types') as response:
            types_data = await get_json(response)

        async with self._session.get(f'{self._api_base_url}/maps/{self.id}/users') as response:
            users_data = await get_json(response)

        self.root, self.ids_to_nodes = self._make_tree(map_data, ignore_out_of_branch=self.view_root_id is not None)
        self.types = NodeTypes(types_data)
        self.users = MapUsers(users_data)

        return self

    async def close(self):
        """ Закрыть соединение """
        await self._session.close()

    def __enter__(self) -> 'MindMap':
        """
        Не используется.
        Нужно только для тайпинга, PyCharm проблеммы, не понимает он аннотацию от aenter
        """
        return self

    async def __aenter__(self) -> 'MindMap':
        """
        async with MindMap(<id>, <token>) as mm:
            pass
        """
        await ensure_future(self.init())
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()

    def get(self, node_id: str) -> Node:
        """
        Получить ссылку на узел по его id.
        """
        try:
            return self.ids_to_nodes[node_id]
        except KeyError:
            raise NodeNotFound()

    async def create(self, parent: Optional[str] = None, parent_node: Optional[Node] = None,
                     node_type: Optional[NodeType] = None, properties: Optional[dict] = None) -> Node:
        """
        Создать узел new_node в RF.
        """
        url = f'{self._api_base_url}/nodes'
        if parent is None and parent_node is None:
            raise RFApiError('Missing parent node')

        node = None
        # todo sessionId miss
        async with self._session.post(
                url,
                json={
                    'parent': parent_node.id if parent_node else parent,
                    'map_id': self.id,
                    'properties': properties,
                    'type_id': node_type.id,
                }
        ) as response:
            resp = await response.read()
            if response.status == 200:
                logger.info('Node has been created')
                # todo put Node to parent in tree
                node = Node(**ujson.loads(resp), ids_to_nodes=self.ids_to_nodes)
            else:
                logger.error(f'Node has NOT been created: {resp}')

        return node

    async def update(self, node: Node, properties_change: Optional[dict] = None) -> Node:
        url = f'{self._api_base_url}/nodes/{node.id}'
        data = {}
        if properties_change:
            data['properties'] = ujson.dumps(properties_change, ensure_ascii=False)

        async with self._session.patch(url, json=data) as response:
            resp = await response.read()
            if response.status == 200:
                node = Node(**ujson.loads(resp), ids_to_nodes=self.ids_to_nodes)
                logger.info(f'Node has been updated: {resp}')
            else:
                logger.error(f'Node has NOT been updated: {resp}')

        return node

    def delete(self, node: Node) -> bool:
        raise NotImplementedError()
