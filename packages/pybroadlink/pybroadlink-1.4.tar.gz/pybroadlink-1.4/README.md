# pybroadlink

Control Broadlink devices with Python 3 using asyncio (single threaded with event loop). Currently supports the RM3 Smart Remote.

## Usage

```python
import sys
import logging
import traceback
from pybroadlink.broadlink_udp import BroadlinkRM3
import asyncio
import binascii
from base64 import b64decode
from pybroadlink import _LOGGER
async def testFake(n):
    for i in range(n):
        _LOGGER.debug("Counter is %d",i)
        await asyncio.sleep(1)
async def discovery_test(*args):
    rv = await BroadlinkUDP.discovery(local_ip_address=args[2],timeout=int(args[3]))
    if rv:
        _LOGGER.info("Discovery OK %s",rv)
    else:
        _LOGGER.warning("Discovery failed")
        
async def emit_test(*args):
    import re
    mo = re.search('^[a-fA-F0-9]+$', args[4])
    if mo:
        payload = binascii.unhexlify(args[4])
    else:
        payload = b64decode(args[4])
    a = BroadlinkRM3((args[2],PORT),args[3])
    rv = await a.emit_ir(payload,retry=1)
    if rv:
        _LOGGER.info("Emit OK %s",binascii.hexlify(rv[0]).decode('utf-8'))
    else:
        _LOGGER.warning("Emit failed")
    a.destroy_remote()
async def learn_test(*args):
    a = BroadlinkRM3((args[2],PORT),args[3])
    rv = await a.enter_learning_mode()
    if rv:
        _LOGGER.info("Entered learning mode (%s): please press key",rv)
        rv = await a.learn_ir_get(30)
        if rv:
            _LOGGER.info("Obtained %s",binascii.hexlify(rv[0]).decode('utf-8'))
        else:
            _LOGGER.warning("No key pressed")
    else:
        _LOGGER.warning("Enter learning failed")
    a.destroy_remote()
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

Pull requests are welcome. Possible areas for improvement:

* Additional Broadlink devices (switches).

## Disclaimer

Not affiliated with Broadlink.