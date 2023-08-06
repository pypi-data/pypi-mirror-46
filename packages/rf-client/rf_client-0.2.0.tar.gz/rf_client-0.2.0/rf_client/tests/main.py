import asyncio
import json
import logging
import sys

import unittest

from rf_client import MindMap, NodeNotFound, set_config, logger, Node, UserNotFound

with open('./secret.json') as f:
    config = json.load(f)

set_config(config['api_url'])


def async_test(coro):
    # https://stackoverflow.com/a/46324983
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))

    return wrapper


def debug(*args):
    logger.debug(' '.join(map(str, args)))


class TestMapLoading(unittest.TestCase):
    @async_test
    async def test_root_loading(self):
        map_id = config['map_id']
        username = config['username']
        password_hash = config['password_hash']
        async with MindMap(map_id, (username, password_hash)) as mm:
            self.assertEqual(mm.root.body.children[0].parent_node, mm.root)
            self.assertEqual(mm.root.body.children[0].parent_node, mm.root.body.children[1].parent_node)
            self.assertEqual(mm.root.get_parents(), [])

            with self.assertRaises(NodeNotFound):
                mm.get('bad_uuid')

            n = mm.root.find(None)
            self.assertIsInstance(n, Node)

            nl = mm.root.find_all(None)
            self.assertIsInstance(nl, list)

            with self.assertRaises(UserNotFound):
                mm.users.find_by_id('bad_uuid')

            with self.assertRaises(UserNotFound):
                mm.users.find_by_username('bad_username')

            current_user = mm.users.find_by_username(username)
            self.assertEqual(current_user.username, username)


if __name__ == '__main__':
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.info('Tests started')

    unittest.main()
