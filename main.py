import asyncio
import aiohttp
from bs4 import BeautifulSoup

result = []

async def gather_data():
    headers = {
        "Accept": "*/*",
        "User-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Mobile Safari/537.36"
    }

    url = f"https://www.labirint.ru/genres/2308/?page=1"

    async with aiohttp.ClientSession() as session:
        res = await session.get(url=url, headers=headers)
        res_text = await res.text()
        soup = BeautifulSoup(res_text, "html.parser")
        pages_count = int(soup.find("div", class_="pagination-number-viewport").find_all("a")[-2].text)

        task_list = []

        for i in range(1, pages_count+1):
            task = asyncio.create_task(get_data(session, i))
            task_list.append(task)

        await asyncio.gather(*task_list)

async def get_data(session, i):
    headers = {
        "Accept": "*/*",
        "User-agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Mobile Safari/537.36"
    }
    url = f"https://www.labirint.ru/genres/2308/?page={i}"
    host = "https://www.labirint.ru"

    async with session.get(url=url, headers=headers) as res:
        res_text = await res.text()
        soup = BeautifulSoup(res_text, "html.parser")
        products = soup.find("div", class_="catalog-responsive outer-catalog catalog").find_all("div",
                                                                                                class_="card-column")

        for item in products:
            book_url = host + item.find("a", class_="cover").get("href")
            book_name = item.find("a", class_="cover").get("title")
            book_price = item.find("div", class_="product need-watch").get("data-price") + " ₽"
            book_pubhouse = "Издатель: " + item.find("div", class_="product need-watch").get("data-pubhouse")
            print(book_name)
            print(book_price)
            print(book_url)
            print(book_pubhouse)
            print("---------------------------------------------------------------------------------")
            result.append(book_name)
        print(" ")
        print(f"[INFO] Обработал страницу {i}")
        print(" ")

if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(gather_data())
