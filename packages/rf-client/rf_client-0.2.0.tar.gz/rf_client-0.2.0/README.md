### Python Red Forester async client

This is early version of Red Forester API wrapper.

Current API limitations:

 - node-links are ignored

Todo:

 - complete node API
 - partial map loading
 - comments API
 - node_type API
 - map API
 - map event listening
 - source code

### Usage Example

To work with wrapper, you need to run Python `event_loop`.

```python
async def task():
     async with MindMap('map_id', ('username', 'password_md5_hash')) as mm:
         # At this moment you can access map nodes, 
         #  map users and map types through mm object.
         # Can create and update nodes
         
         # mm.root is map root Node.
         # Node model has methods to find childs and ancestors Nodes.
         # mm object has methods to act with API.

         pass

loop = asyncio.get_event_loop()
loop.run_until_complete(task())
```

MindMap usage:
```python
MindMap(map_id: str,
        token: Tuple[str, str],  # username (email) + md5 hash
        view_root_id=None,  # id of root Node

        # temporary way to ignore node-links from outside of loading branch
        ignore_out_of_branch=False,

        # session_id is identifier of user-session. Allows to detect you own events 
        #  (if you do events listening)
        session_id=None
        )
```

You also can instantiate `MindMap(...)` without context manager (`with`),
but you will need to call `await mm.init()` and `await mm.close()` manually.
