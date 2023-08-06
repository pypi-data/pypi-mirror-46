import asyncio

import aiohttp


async def get_ip() -> str:
    url = 'https://api.ipify.org?format=json'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response_json = await response.json()
            return response_json['ip']


def print_result(ip: str):
    print(f'Your IP is {ip}')


async def main():
    print_result(await get_ip())


if __name__ == '__main__':
    asyncio.run(main())
