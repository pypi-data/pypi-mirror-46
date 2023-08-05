# pygocomma

Control Gocomma R9 devices with Python 3 using asyncio (single threaded with event loop).
Tu use the library you need the id and key of your device. You can get them using any of [those](https://github.com/clach04/python-tuya/wiki) methods.

## Usage

```python
import sys
import logging
from pygocomma.r9 import R9
import asyncio
import binascii
from pygocomma import _LOGGER
async def testFake(n):
    for i in range(n):
        _LOGGER.debug("Counter is %d",i)
        await asyncio.sleep(1)
async def ping_test(*args):
    a = R9((args[2],DEFAULT_PORT),args[3],args[4])
    rv = await a.ping()
    if rv:
        _LOGGER.info("Ping OK %s",binascii.hexlify(rv))
    else:
        _LOGGER.warning("Ping failed")
    await a.destroy_connection()
async def ask_last_test(*args):
    a = R9((args[2],DEFAULT_PORT),args[3],args[4])
    rv = await a.ask_last()
    if rv:
        _LOGGER.info("Ask last OK %s",rv)
    else:
        _LOGGER.warning("Ask last failed")
    await a.destroy_connection()
async def discovery_test(*args):
    rv = await R9.discovery(int(args[2]))
    if rv:
        _LOGGER.info("Discovery OK %s",rv)
    else:
        _LOGGER.warning("Discovery failed")
        
async def emit_test(*args):
    import re
    mo = re.search('^[a-fA-F0-9]+$', args[5])
    if mo:
        payload = binascii.unhexlify(args[5])
    else:
        payload = b64decode(args[5])
    a = R9((args[2],DEFAULT_PORT),args[3],args[4])
    rv = await a.emit_ir(payload)
    if rv:
        _LOGGER.info("Emit OK %s",binascii.hexlify(rv).decode('utf-8'))
    else:
        _LOGGER.warning("Emit failed")
    await a.destroy_connection()
async def learn_test(*args):
    a = R9((args[2],DEFAULT_PORT),args[3],args[4])
    rv = await a.enter_learning_mode()
    if rv:
        _LOGGER.info("Entered learning mode (%s): please press key",rv)
        rv = await a.get_learned_key()
        if rv:
            _LOGGER.info("Obtained %s",binascii.hexlify(rv).decode('utf-8'))
        else:
            _LOGGER.warning("No key pressed")
        rv = await a.exit_learning_mode()
        if rv:
            _LOGGER.info("Exit OK %s", rv)
        else:
            _LOGGER.warning("Exit failed")
    else:
        _LOGGER.warning("Enter learning failed")
    await a.destroy_connection()
_LOGGER.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stderr)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
_LOGGER.addHandler(handler)
loop = asyncio.get_event_loop()
try:
    asyncio.ensure_future(testFake(150))
    if sys.argv[1]=="learn":
        loop.run_until_complete(learn_test(*sys.argv))
    elif sys.argv[1]=="discovery":
        loop.run_until_complete(discovery_test(*sys.argv))
    elif sys.argv[1]=="ping":
        loop.run_until_complete(ping_test(*sys.argv))
    elif sys.argv[1]=="asklast":
        loop.run_until_complete(ask_last_test(*sys.argv))
    elif sys.argv[1]=="pingst":
        for i in range(int(sys.argv[5])):
            loop.run_until_complete(ping_test(*sys.argv))
    else:
        loop.run_until_complete(emit_test(*sys.argv))
except BaseException as ex:
    _LOGGER.error("Test error %s",str(ex))
    traceback.print_exc()
except:
    _LOGGER.error("Test error")
    traceback.print_exc()
finally:
    loop.close()
```

## Contributions

Pull requests are welcome. 

## Disclaimer

Not affiliated with Gocomma in any way.


### Related Projects

  * https://github.com/codetheweb/tuyapi node.js
  * https://github.com/sean6541/tuyaapi Python API to the web api
  * https://github.com/clach04/python-tuya/ Python API to the web api