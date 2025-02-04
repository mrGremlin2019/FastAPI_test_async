import time
import asyncio
from fastapi import FastAPI, BackgroundTasks

app = FastAPI()


def sync_task():
    time.sleep(3)
    print("отправлен запрос")


async def async_task():
    await asyncio.sleep(3)
    print("запрос в сторонний API")


# Асинхронный роутер
@app.post("/Async")
async def some_route():
    ...
    asyncio.create_task(async_task())  # кладём задачу в событийный цикл
    return {"ok": True}


# Синхронный роутер
@app.post("/Sync")
async def someone_route(bg_tasks: BackgroundTasks):
    ...
    bg_tasks.add_task(sync_task)
    return {"ok": True}


@app.get("/sync/{id}")
def sync_func(id: int):
    print(f"sync. Начал {id}: {time.time(): .2f}")
    time.sleep(3)
    print(f"sync. Закончил {id}: {time.time(): .2f}")


@app.get("/async/{id}")
async def async_func(id: int):
    print(f"async. Начал {id}: {time.time(): .2f}")
    await asyncio.sleep(3)
    print(f"async. Закончил {id}: {time.time(): .2f}")
