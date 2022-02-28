from urllib.request import Request
from discord import webhook
from fastapi import FastAPI, Request, Response
import asyncio


class Database:
    def __init__(self) -> None:
        self.__db__ = {}

    async def get(self, key: str):
        return self.__db__.get(key)

    async def set(self, key: str, value: str):
        self.__db__[key] = value


class InventoryTracker(Database):
    async def add_subscriber(self, asin: str, webhook_url: str):
        self.__db__[asin]["subscribers"].append(webhook_url)

    async def set_new_price(self, asin: str, price: int):
        self.__db__[asin]["last_price"] = price

    async def get_all_asins(self):
        return list(self.__db__.keys())


{
    "asin": {
        "last_price": 12738,
        "subscribers": ["webhook_url", "webhook_url", "webhook_url"],
    }
}


app = FastAPI()
db = InventoryTracker()


@app.on_event("startup")
async def start():
    asyncio.ensure_future(polling_loop())


@app.get("/")
async def index(request: Request, response: Response) -> Response:
    return "hello"


@app.post("/subscribe")
async def subscribe(request: Request, response: Response) -> Response:
    try:
        data = await request.json()
    except:
        return Response(status_code=400)

    print("new subscriber")

    if (asin := data.get("asin")) and (webhook_url := data.get("webhook_url")):

        print(asin, webhook_url)
        # Check if valid asin

        # check if aldready subscribed

        # validate webhook url

        # verify webhook exists

        if found := await db.get(asin):
            if webhook_url in found["subscribers"]:
                return Response(content="Webhook Already Subscribed", status_code=409)

            await db.add_subscriber(asin, webhook_url)

            return Response(content="Successfuly Subscribed")
        else:
            price = 232  # request to amazon
            await db.set(asin, {"last_price": price, "subscribers": [webhook_url]})
            return Response(content="Successfuly Subscribed")

    return Response(status_code=400)


async def polling_loop():
    while True:
        print(db.__db__)
        asins = await db.get_all_asins()
        for asin in asins:
            price = 0  # make request to amazon price

            found = await db.get(asin)
            if found["last_price"] != price:
                await db.set_new_price(asin, price)

                for webhook_url in found["subscribers"]:
                    print("alerting:", webhook_url)
                    # make post request to the webhjook with new price

                    # if webhook fails, remove the subcribers

                    pass

        await asyncio.sleep(5)