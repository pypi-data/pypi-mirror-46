import aiohttp
import asyncio
from pyatag.gateway import atagDataStore


async def test(TESTDATA):

    async with aiohttp.ClientSession() as session:
        atag = atagDataStore(host=TESTDATA["_host"],
                             port=TESTDATA["_port"],
                             mail=TESTDATA["_mail"],
                             interface=TESTDATA["_interface"],
                             scan_interval=TESTDATA["_scan_interval"],
                             session=session,
                             sensors=TESTDATA["_sensors"])
        await atag.async_check_pair_status()
        # await atag.async_update()
        print(await atag.async_set_atag(_target_mode="manual", _target_temp=13))
        return atag

asyncio.get_event_loop().run_until_complete(test(TESTDATA))
