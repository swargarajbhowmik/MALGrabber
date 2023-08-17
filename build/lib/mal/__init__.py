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

    def search(self, query, limit=10, type="anime"):
        data = []
        index = 0
        limitinc = 0

        async def _search():
            nonlocal type
            nonlocal limitinc
            nonlocal index
            async with aiohttp.ClientSession() as session:
                while len(data) < limit:
                    url = f"https://myanimelist.net/{type}.php?q={query}&cat={type}&show={limitinc}"
                    response_text = await self.fetch_data(session, url)

                    soup = BeautifulSoup(response_text, 'html.parser')
                    target_rows = soup.find_all('tr')

                    for row in target_rows[10:]:
                        index += 1
                        anime_link = row.select_one('a.hoverinfo_trigger')['href']
                        image_url = row.select_one('img')['data-src']
                        score = row.find_all('td', class_=['borderClass', 'ac'])[4].text.strip()
                        episodes = row.find_all('td', class_=['borderClass', 'ac'])[3].text.strip()
                        type_of_anime = row.find_all('td', class_=['borderClass', 'ac'])[2].text.strip()
                        title = row.select_one('a.hoverinfo_trigger strong').text.strip()
                        description = row.find('div', class_='pt4').text.strip().replace("read more.", "")

                        data.append({
                            "index": index,
                            "id": re.search(r"/.*?/(\d+)/", anime_link).group(1),
                            "title": title,
                            "description": description,
                            "smallthumbnail": image_url,
                            "type": type_of_anime,
                            "episodes": episodes,
                            "score": score,
                            "url": anime_link,
                        })

                    limitinc += 50

        self.loop.run_until_complete(_search())

        return json.dumps(data[:limit], indent=4)



    def topanime(self, limit=10, type=None):
        data = []
        index = 0
        limitinc = 0

        async def _topanime():
            nonlocal type
            nonlocal limitinc
            nonlocal index
            async with aiohttp.ClientSession() as session:
                while len(data) < limit:
                    if type==None:
                        url = f"https://myanimelist.net/topanime.php?limit={limitinc}"
                    else:
                        url = f"https://myanimelist.net/topanime.php?type={type}&limit={limitinc}"
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

                        pv = item.find('a', class_='mal-icon')
                        if pv:
                            pv = pv['href']
                        else:
                            pv = None

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
                            "pv": pv,
                            "url": url,
                        })

                    limitinc += 50

        self.loop.run_until_complete(_topanime())

        return json.dumps(data[:limit], indent=4)


    def genres(self):
        data = []
        index = 0

        async def _genres():
            nonlocal index
            async with aiohttp.ClientSession() as session:
                response_text = await self.fetch_data(session, "https://myanimelist.net/anime.php")

                soup = BeautifulSoup(response_text, 'html.parser')
                genrelist = soup.find_all('a', class_='genre-name-link')

                for genre in genrelist:
                    if "genre" in genre['href']:
                        data.append({
                            "index": index,
                            "id":  re.search(r'/anime/genre/(\d+)/', genre['href']).group(1),
                            "genre": genre.text.split(" ")[0],
                            "count": genre.text.split(" ")[-1][1:-1].replace(",", ""),
                            "url": "https://myanimelist.net"+genre['href'],
                        })

                    index += 1

        self.loop.run_until_complete(_genres())
        
        return json.dumps(data, indent=4)


    def studios(self):
        data = []
        index = 0

        async def _studios():
            nonlocal index
            async with aiohttp.ClientSession() as session:
                response_text = await self.fetch_data(session, "https://myanimelist.net/anime/producer")

                soup = BeautifulSoup(response_text, 'html.parser')
                producerlist = soup.find_all('a', class_='genre-name-link')

                for producer in producerlist:
                    if "producer" in producer['href']:
                        data.append({
                            "index": index,
                            "id":  re.search(r'/anime/producer/(\d+)/', producer['href']).group(1),
                            "name": producer.text.split(" ")[0],
                            "count": producer.text.split(" ")[-1][1:-1].replace(",", ""),
                            "url": "https://myanimelist.net"+producer['href'],
                        })

                    index += 1

        self.loop.run_until_complete(_studios())
        
        return json.dumps(data, indent=4)

    def seasons(self):
        data = []
        index = 0

        async def _seasons():
            nonlocal index
            async with aiohttp.ClientSession() as session:
                response_text = await self.fetch_data(session, "https://myanimelist.net/anime/season/archive")

                soup = BeautifulSoup(response_text, 'html.parser')
                for row in soup.select('table.anime-seasonal-byseason tr'):
                    cells = row.select('td')
                    for cell in cells:
                        link = cell.find('a')
                        if link:
                            season_year = link.get_text(strip=True)
                            href = link['href']
                            data.append({
                                "index": index,
                                "season": season_year.split(" ")[0],
                                "year": season_year.split(" ")[1],
                                "url": href
                            })
                        index += 1

        self.loop.run_until_complete(_seasons())
        
        return json.dumps(data, indent=4)

mal = MALScraper()
search = mal.search
topanime = mal.topanime
genres = mal.genres
studios = mal.studios
seasons = mal.seasons