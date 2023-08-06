# aiomixpanel
aiohttp-based mixpanel client for python3


### Usage Example
```python
import os
import asyncio
from uuid import uuid4

from mixpanel import Mixpanel
from aiohttp import ClientSession

from aiomixpanel import AIOConsumer


async def main():
    async with ClientSession() as client:
        mp = Mixpanel(token=os.environ.get("MIXPANEL_TOKEN"), consumer=AIOConsumer(client))
        mp.track(str(uuid4()), "FIRST_EVENT", dict(name="John Doe"))

        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())

```
