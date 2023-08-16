import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import re

class MALScraper:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def fetch_data(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    def popularity(self, limit=10):
        data = []
        index = 0
        limitinc = 0

        async def _popularity():
            nonlocal limitinc
            nonlocal index
            async with aiohttp.ClientSession() as session:
                while len(data) < limit:
                    url = f"https://myanimelist.net/topanime.php?type=bypopularity&limit={limitinc}"
                    response_text = await self.fetch_data(session, url)

                    soup = BeautifulSoup(response_text, 'html.parser')
                    animelist = soup.find_all('tr', class_='ranking-list')

                    for item in animelist:
                        index += 1
                        a_tag = item.find('a', class_='hoverinfo_trigger')
                        if a_tag:
                            url = a_tag['href']

                        img_tag = item.find('img', class_='lazyload')
                        if img_tag:
                            thumbnail = img_tag['data-src']

                        h3_tag = item.find('h3', class_='hoverinfo_trigger')
                        if h3_tag:
                            title = h3_tag.get_text()

                        otherinfo = item.find('div', class_='information')
                        otherinfo = otherinfo.get_text().split('\n')

                        type = otherinfo[1].strip()
                        year = otherinfo[2].strip()
                        members = otherinfo[3].strip()

                        score = item.find('span', class_='score-label').get_text()

                        pattern = r"/(\d+)/"
                        match = re.search(pattern, url)
                        if match:
                            anime_id = match.group(1)
                            id = anime_id
                        else:
                            id = None

                        data.append({
                            "index": index,
                            "id": id,
                            "title": title,
                            "smallthumbnail": thumbnail,
                            "type": type,
                            "year": year,
                            "members": members,
                            "score": score,
                            "url": url,
                        })

                    limitinc += 50

        self.loop.run_until_complete(_popularity())

        return json.dumps(data[:limit], indent=4)



    def airing(self, limit=10):
        data = []
        index = 0
        limitinc = 0

        async def _airing():
            nonlocal limitinc
            nonlocal index
            async with aiohttp.ClientSession() as session:
                while len(data) < limit:
                    url = f"https://myanimelist.net/topanime.php?type=airing&limit={limitinc}"
                    response_text = await self.fetch_data(session, url)

                    soup = BeautifulSoup(response_text, 'html.parser')
                    animelist = soup.find_all('tr', class_='ranking-list')

                    for item in animelist:
                        index += 1
                        a_tag = item.find('a', class_='hoverinfo_trigger')
                        if a_tag:
                            url = a_tag['href']

                        img_tag = item.find('img', class_='lazyload')
                        if img_tag:
                            thumbnail = img_tag['data-src']

                        h3_tag = item.find('h3', class_='hoverinfo_trigger')
                        if h3_tag:
                            title = h3_tag.get_text()

                        otherinfo = item.find('div', class_='information')
                        otherinfo = otherinfo.get_text().split('\n')

                        type = otherinfo[1].strip()
                        year = otherinfo[2].strip()
                        members = otherinfo[3].strip()

                        score = item.find('span', class_='score-label').get_text()

                        pattern = r"/(\d+)/"
                        match = re.search(pattern, url)
                        if match:
                            anime_id = match.group(1)
                            id = anime_id
                        else:
                            id = None

                        data.append({
                            "index": index,
                            "id": id,
                            "title": title,
                            "smallthumbnail": thumbnail,
                            "type": type,
                            "year": year,
                            "members": members,
                            "score": score,
                            "url": url,
                        })

                    limitinc += 50

        self.loop.run_until_complete(_airing())

        return json.dumps(data[:limit], indent=4)
    

    def upcoming(self, limit=10):
        data = []
        index = 0
        limitinc = 0

        async def _airing():
            nonlocal limitinc
            nonlocal index
            async with aiohttp.ClientSession() as session:
                while len(data) < limit:
                    url = f"https://myanimelist.net/topanime.php?type=airing&limit={limitinc}"
                    response_text = await self.fetch_data(session, url)

                    soup = BeautifulSoup(response_text, 'html.parser')
                    animelist = soup.find_all('tr', class_='ranking-list')

                    for item in animelist:
                        index += 1
                        a_tag = item.find('a', class_='hoverinfo_trigger')
                        if a_tag:
                            url = a_tag['href']

                        img_tag = item.find('img', class_='lazyload')
                        if img_tag:
                            thumbnail = img_tag['data-src']

                        h3_tag = item.find('h3', class_='hoverinfo_trigger')
                        if h3_tag:
                            title = h3_tag.get_text()

                        otherinfo = item.find('div', class_='information')
                        otherinfo = otherinfo.get_text().split('\n')

                        type = otherinfo[1].strip()
                        year = otherinfo[2].strip()
                        members = otherinfo[3].strip()

                        pattern = r"/(\d+)/"
                        match = re.search(pattern, url)
                        if match:
                            anime_id = match.group(1)
                            id = anime_id
                        else:
                            id = None

                        data.append({
                            "index": index,
                            "id": id,
                            "title": title,
                            "smallthumbnail": thumbnail,
                            "type": type,
                            "year": year,
                            "members": members,
                            "url": url,
                        })

                    limitinc += 50

        self.loop.run_until_complete(_airing())

        return json.dumps(data[:limit], indent=4)

mal = MALScraper()
popularity = mal.popularity
airing = mal.airing
upcoming = mal.upcoming