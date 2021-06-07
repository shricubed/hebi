import requests
import os
import json
from PIL import Image
import networkx as nx

class API():

    
    def __init__(self):
        res = requests.get("https://raw.githubusercontent.com/manami-project/anime-offline-database/master/anime-offline-database.json")

        self.j = res.json()
        self.G = nx.Graph()

    def print_help(self, s):
        return json.dumps(s, indent=2)

    def series(self, name):
        for s in self.j['data']:
            if s['title'] == name or name in s['synonyms']:
                return json.dumps(s, indent=2)

        return None

    def season_list(self, season, year):
        animes = []
        for s in self.j['data']:
            if s['animeSeason']['season'] == season and s['animeSeason']['year'] == year:
                animes.append(self.print_help(s))

        return animes

    def getFromId(self, malId):
        for s in self.j['data']:
            for st in s['sources']:
                if st.endswith("/anime/" + str(malId)):
                    return self.print_help(s)

        return None

    def getFromUrl(self, url):
        for s in self.j['data']:
            if url in s['sources']:
                return s['title']


    def hasKeyword(self, tag):
        animes = []
        for s in self.j['data']:
            if tag in s['tags']:
                animes.append(self.print_help(s))
        return animes

    def getpic(self, title):
        ser = json.loads(self.series(title))
        if ser is not None:
            url = ser['picture']
            im = Image.open(requests.get(url, stream=True).raw)
            im.show()

    def getRelations(self, title, level):
        if level == 0:
            return
        ser = json.loads(self.series(title))
        for r in ser['relations']:
            curr = self.getFromUrl(r)
            self.G.add_edge(title, curr)
            self.getRelations(curr, level-1)



            












   
    





    

    



