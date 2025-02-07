import httpx


async def loginHandle(username="", password=""):
    if len(username) <= 3 or len(password) <= 4:
        return False

    try:
        print(f"{username} {password}")
        url = "http://192.168.1.100:4000/api/login"

        async with httpx.AsyncClient() as client:
            res = await client.post(
                url, json={"username": username, "password": password}
            )

        data = res.json()
        if data["success"]:
            return True
        else:
            return False
    except Exception as err:
        print(f"An error occurred: {err}")
        return False
