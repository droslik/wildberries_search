import aiohttp
import asyncio


def get_url_data(article):
    if len(str(article)) > 5:
        vol = int(str(article)[0:-5])
        part = int(str(article)[0:-3])
    else:
        if len(str(article)) < 4:
            vol = 0
            part = 0
        else:
            vol = 0
            part = int(str(article)[0:-3])
    return vol, part


async def create_one_task(session, article):
    for i in range(1, 10):
        async with session.get(
                f'https://basket-0{i}.wb.ru/'
                f'vol{get_url_data(article)[0]}/'
                f'part{get_url_data(article)[1]}/'
                f'{article}/info/ru/card.json'
        ) as resp:
            if resp.status != 200:
                continue
            if resp.status == 200:
                json_data = await resp.json()
                title = json_data['imt_name']\
                    if 'imt_name' in json_data \
                    else json_data['subj_name']
                article = json_data['nm_id']
                brand = json_data['selling']['brand_name']
                data = {"title": title, "brand": brand, "article": article}
                return data
            return None


async def get_all_tasks(session, articles):
    tasks = []
    for article in articles:
        task = asyncio.create_task(create_one_task(session, article))
        tasks.append(task)
    results = await asyncio.gather(*tasks)
    return results


async def main(articles):
    async with aiohttp.ClientSession(trust_env=True) as session:
        response = await get_all_tasks(session, articles)
        items = [result for result in response if result is not None]
        if len(articles) > 1:
            return items
        else:
            if len(items) == 0:
                return None
            return items[0]
