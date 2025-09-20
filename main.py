import asyncio
import os
import platform
import subprocess

import httpx

httpx_client = httpx.AsyncClient()
head_url = os.getenv("HEAD_URL")


# 下载文件到指定目录
async def download_V2bX_file(name, parm=None):
    url = head_url + "/V2bX/" + name
    if parm:
        url = url + "?" + parm
    print(url)
    path = "/etc/V2bX/" + name

    response = await httpx_client.get(url)
    if response.status_code != 200:
        return False
    if os.path.exists(path):
        with open(path, "rb") as f:
            if f.read() == response.content:
                return False
    with open(path, "wb+") as f:
        f.write(response.content)
        return True


async def main():
    response = httpx.get("https://ifconfig.me/ip")
    ip = response.text
    host_name = platform.node().split("-")[-1]
    print(f"当前公网IP：{response.text}")
    while True:
        tasks = [
            download_V2bX_file("config.json", f"ip={ip}&host_name={host_name}"),
            download_V2bX_file("custom_outbound.json"),
            download_V2bX_file("route.json"),
        ]
        rets = await asyncio.gather(*tasks)
        if all(rets):
            print("download success")
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
