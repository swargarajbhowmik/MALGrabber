import aiohttp
import asyncio
from bs4 import BeautifulSoup
import json
import re
import datetime

class MALScraper:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

    async def fetch_data(self, session, url):
        async with session.get(url) as response:
            return await response.text()

    def searchanimebyquery(self, query, limit=10, type=0, status=0):
        data = []
        index = 0
        limitinc = 0
        if len(query)>3:
            async def _animesearch():
                nonlocal type
                nonlocal limitinc
                nonlocal index
                async with aiohttp.ClientSession() as session:
                    while len(data) < limit:
                        url = f"https://myanimelist.net/anime.php?q={query}&cat=anime&show={limitinc}&type={type}&status={status}"
                        response_text = await self.fetch_data(session, url)

                        soup = BeautifulSoup(response_text, 'html.parser')
                        target_rows = soup.find_all('tr')

                        for row in target_rows[9:]:
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

            self.loop.run_until_complete(_animesearch())

            return data[:limit]
        else:
            return f"Query should have atleast 3 characters. Provided query has only '{len(query)}'"


    def searchanimebyletter(self, query, limit=10, type=0, status=0):
        data = []
        index = 0
        limitinc = 0
        if len(query)==1:
            async def _animesearchbyletter():
                nonlocal type
                nonlocal limitinc
                nonlocal index
                async with aiohttp.ClientSession() as session:
                    while len(data) < limit:
                        url = f"https://myanimelist.net/anime.php?letter={query}&show={limitinc}&type={type}&status={status}"
                        response_text = await self.fetch_data(session, url)

                        soup = BeautifulSoup(response_text, 'html.parser')
                        target_rows = soup.find_all('tr')

                        for row in target_rows[9:]:
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

            self.loop.run_until_complete(_animesearchbyletter())

            return data[:limit]
        else:
            return f"Letter should have atmost 1 character. Provided query has '{len(query)}'"



    def listanimebygenre(self, query, limit=10):
        
        genreandid = {'Action': 1, 'Adventure': 2, 'Avant': 5, 'Award': 46, 'Boys': 28, 'Comedy': 4, 'Drama': 8, 'Fantasy': 10, 'Girls': 26, 'Gourmet': 47, 'Horror': 14, 'Mystery': 7, 'Romance': 22, 'Sci-Fi': 24, 'Slice': 36, 'Sports': 30, 'Supernatural': 37, 'Suspense': 41, 'Ecchi': 9, 'Erotica': 49, 'Hentai': 12, 'Adult': 50, 'Anthropomorphic': 51, 'CGDCT': 52, 'Childcare': 53, 'Combat': 54, 'Crossdressing': 81, 'Delinquents': 55, 'Detective': 39, 'Educational': 56, 'Gag': 57, 'Gore': 58, 'Harem': 35, 'High': 59, 'Historical': 13, 'Idols': 60, 'Idols': 61, 'Isekai': 62, 'Iyashikei': 63, 'Love': 64, 'Magical': 65, 'Mahou': 66, 'Martial': 17, 'Mecha': 18, 'Medical': 67, 'Military': 38, 'Music': 19, 'Mythology': 6, 'Organized': 68, 'Otaku': 69, 'Parody': 20, 'Performing': 70, 'Pets': 71, 'Psychological': 40, 'Racing': 3, 'Reincarnation': 72, 'Reverse': 73, 'Romantic': 74, 'Samurai': 21, 'School': 23, 'Showbiz': 75, 'Space': 29, 'Strategy': 11, 'Super': 31, 'Survival': 76, 'Team': 77, 'Time': 78, 'Vampire': 32, 'Video': 79, 'Visual': 80, 'Workplace': 48, 'Josei': 43, 'Kids': 15, 'Seinen': 42, 'Shoujo': 25, 'Shounen': 27}
        
        data = []
        index = 0
        limitinc = 1
        
        if query.lower().capitalize() in genreandid.keys():
            async def _animesearch():
                nonlocal limitinc
                nonlocal index
                async with aiohttp.ClientSession() as session:

                    while len(data) < limit:
                        url = f"https://myanimelist.net/anime/genre/{genreandid[query.lower().capitalize()]}/{query}&page={limitinc}"
                        response_text = await self.fetch_data(session, url)

                        soup = BeautifulSoup(response_text, 'html.parser')
                        target_rows = soup.find_all('div', class_=['js-anime-category-producer'])

                        for row in target_rows:
                            index += 1
                            anime_link = title = row.select_one('a.link-title')['href']
                            title = row.select_one('a.link-title').text.strip()
                            description = row.find('p', class_='preline').text.strip().replace("[Written by MAL Rewrite]", "")
                            otherinfo = row.find_all('span', class_=['item'])

                            producer_links = {}

                            for a_tag in row.find_all('a', href=True):
                                if 'producer' in a_tag['href']:
                                    producer_links[a_tag.get_text()] = "https://myanimelist.net"+a_tag['href']

                            genre_links = {}

                            for a_tag in row.find_all('a', href=True):
                                if 'genre' in a_tag['href'] and "Add to List" not in a_tag.text:
                                    genre_links[a_tag.get_text()] = "https://myanimelist.net"+a_tag['href']

                            data.append({
                                "index": index,
                                "id": re.search(r"/.*?/(\d+)/", anime_link).group(1),
                                "title": title,
                                "description": description,
                                "thumbnail": row.find('img')['data-src'],
                                "typeandyear": otherinfo[0].text.strip(),
                                "status": otherinfo[1].text.strip(),
                                "episodes": otherinfo[2].text.split("\n")[1].strip(),
                                "durationperepisode": otherinfo[2].text.split("\n")[2].strip(),
                                "producer": producer_links,
                                "source": otherinfo[4].text.strip(),
                                "theme": genre_links,
                                "url": anime_link,
                            })

                        limitinc += 1

            self.loop.run_until_complete(_animesearch())

            return data[:limit]
        else:
            return "'{query}' genre not found"

    def listanimebyseason(self, season, year=datetime.datetime.now().year, limit=10):
        
        data = []
        index = 0
        limitinc = 1
        
        if season.lower() in ['winter', 'summer', 'spring', 'fall']:
            async def _animesearch():
                nonlocal limitinc
                nonlocal index
                async with aiohttp.ClientSession() as session:

                    url = f"https://myanimelist.net/anime/season/{year}/{season}"
                    response_text = await self.fetch_data(session, url)

                    soup = BeautifulSoup(response_text, 'html.parser')
                    target_rows = soup.find_all('div', class_=['js-anime-category-producer'])

                    for row in target_rows:
                        index += 1
                        anime_link = title = row.select_one('a.link-title')['href']
                        otherinfo = row.find_all('span', class_=['item'])

                        producer_links = {}

                        for a_tag in row.find_all('a', href=True):
                            if 'producer' in a_tag['href']:
                                producer_links[a_tag.get_text()] = "https://myanimelist.net"+a_tag['href']

                        genre_links = {}

                        for a_tag in row.find_all('a', href=True):
                            if 'genre' in a_tag['href'] and "Add to List" not in a_tag.text:
                                genre_links[a_tag.get_text()] = "https://myanimelist.net"+a_tag['href']

                        if row.find('img').get('src'):
                            thumbnail = row.find('img')['src']
                        else:
                            thumbnail = row.find('img')['data-src']

                        data.append({
                            "index": index,
                            "id": re.search(r"/.*?/(\d+)/", anime_link).group(1),
                            "title": row.find('span', 'js-title').text,
                            "description": row.find('p', 'preline').text.replace("[Written by MAL Rewrite]", ""),
                            "thumbnail": thumbnail,
                            "source": row.find_all('div', class_=['property'])[1].text.replace('\n', '').replace('Source', '').strip(),
                            "episodes": otherinfo[1].text.split(",\n")[0].strip(),
                            "durationperepisode": otherinfo[1].text.split(",\n")[1].strip(),
                            "producers": producer_links,
                            "theme": genre_links,
                            "startdate": otherinfo[0].text.strip(),
                            "members": row.find('span', 'js-members').text,
                            "score": row.find('span', 'js-score').text,
                            "url": anime_link,
                        })


            self.loop.run_until_complete(_animesearch())

            return data[:limit]
        else:
            return "'{query}' season not found"

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

        return data[:limit]

    def listgenres(self):
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
        
        return data

    def liststudios(self):
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
        
        return data

    def listseasons(self):
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
        
        return data

mal = MALScraper()

# Methods
searchanimebyquery = mal.searchanimebyquery
searchanimebyletter = mal.searchanimebyletter

listanimebygenre = mal.listanimebygenre
listanimebyseason = mal.listanimebyseason

listgenres = mal.listgenres
liststudios = mal.liststudios
listseasons = mal.listseasons

topanime = mal.topanime