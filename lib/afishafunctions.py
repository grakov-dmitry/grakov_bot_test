import requests
from bs4 import BeautifulSoup

def getKinoAfisha():
    headers = requests.utils.default_headers()
    headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/69.0'})
    url = "https://afisha.tut.by/film-mogilev/"
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    variable = soup.find("div", {"id":"schedule-table"}) 
    dateAfisha = variable.contents[0].contents[1].contents[0]
    KinoteatrId = 1
    conterKinoteatr = len(variable)
    text = 'Афиша на ' + str(dateAfisha) + ":\n"
    while (KinoteatrId) < conterKinoteatr:
        KinoteatrName = variable.contents[KinoteatrId].contents[1].contents[1].contents[1].contents[1].contents[0]
        text = text + "\n*" + str(KinoteatrName) + "*\n"
        filmId = 1
        conterFilms = len(variable.contents[KinoteatrId].contents[1].contents[3].contents[1]) - 1
        while filmId < conterFilms:
            filmTitle = variable.contents[KinoteatrId].contents[1].contents[3].contents[1].contents[filmId].contents[1].contents[1].contents[1].contents[1].contents[1].contents[0]
            text = text + '🎞' + str(filmTitle) + "  *"
            filmTimeId = 1
            counterTimeId = len(variable.contents[KinoteatrId].contents[1].contents[3].contents[1].contents[filmId].contents[1].contents[3].contents[1].contents[1])
            while filmTimeId < counterTimeId:
                time = variable.contents[KinoteatrId].contents[1].contents[3].contents[1].contents[filmId].contents[1].contents[3].contents[1].contents[1].contents[filmTimeId].contents[1].contents[0]
                text = text + str(time) + "; "
                filmTimeId = filmTimeId + 2 
            text = text + "*\n"
            filmId = filmId + 1
        filmId = 0
        KinoteatrId = KinoteatrId + 1 
    return(text)