import requests
from bs4 import BeautifulSoup

def getBestBankCource(bankBuyId, bankSellId, currency):
    bankList = getBankList()
    listBestBanks = sortFunction('UP', bankList, bankBuyId)
    text = '*Лучшие курсы покупки ' + str(currency) + 'в Могилеве*'
    for bankNum in listBestBanks:
        text = text + '\n\n' + str(bankList[bankNum][0])[1:-1] + '\n' + str(bankList[bankNum][1])[1:-1] + '\n*' + str(bankList[bankNum][bankBuyId] + '* BYN')

    listBestBanks = sortFunction('DOWN', bankList, bankSellId)
    text = text + '\n\n\n*Лучшие курсы продажи ' + str(currency) + 'в Могилеве*'
    for bankNum in listBestBanks:
        text = text + '\n\n' + str(bankList[bankNum][0])[1:-1] + '\n' + str(bankList[bankNum][1])[1:-1] + '\n*' + str(bankList[bankNum][bankSellId] + '* BYN')
    return(text)

def getBankList():
    headers = requests.utils.default_headers()
    headers.update({ 'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/69.0'})
    url = "https://select.by/kurs/mogilev/"
    req = requests.get(url, headers)
    soup = BeautifulSoup(req.content, 'html.parser')
    variable = soup.find("table", {"class":"tablesorter"}) 
    bankIndex = 2
    bankList = []
    bankInList = 0
    lengntBanks = len(variable.contents[1])
    while bankIndex<lengntBanks:
        bankName = variable.contents[1].contents[bankIndex].contents[0].contents[0].contents[0].contents
        bankAdres = variable.contents[1].contents[bankIndex].contents[0].contents[2].contents
        usdBuy = variable.contents[1].contents[bankIndex].contents[1].contents[0]
        usdSell = variable.contents[1].contents[bankIndex].contents[2].contents[0]
        eurBuy = variable.contents[1].contents[bankIndex].contents[3].contents[0]
        eurSell = variable.contents[1].contents[bankIndex].contents[4].contents[0]
        rubBuy = variable.contents[1].contents[bankIndex].contents[5].contents[0]
        rubSell = variable.contents[1].contents[bankIndex].contents[6].contents[0]
        bankArray = []
        usdBuy = usdBuy.replace(',', '.')
        usdSell = usdSell.replace(',', '.')
        eurBuy = eurBuy.replace(',', '.')
        eurSell = eurSell.replace(',', '.')
        rubBuy = rubBuy.replace(',', '.')
        rubSell = rubSell.replace(',', '.')
        bankArray.insert(0, bankName)
        bankArray.insert(1, bankAdres)
        bankArray.insert(2, usdBuy)
        bankArray.insert(3, usdSell)
        bankArray.insert(4, eurBuy)
        bankArray.insert(5, eurSell)
        bankArray.insert(6, rubBuy)
        bankArray.insert(7, rubSell)
        bankList.insert(bankIndex, bankArray)
        bankIndex = bankIndex + 1
        bankInList = bankInList +1
    return(bankList)

def sortFunction(direction, sortObj, bankId):
    if (direction == 'UP'):
        listBestBanks = [0,0,0]
        listBwstBanksValues = [0,0,0]
        bankIndex = 0
        for oneBank in sortObj:
            if float(oneBank[bankId]) > float(listBwstBanksValues[0]):
                listBwstBanksValues[2] = listBwstBanksValues[1]
                listBwstBanksValues[1] = listBwstBanksValues[0]
                listBwstBanksValues[0] = oneBank[6]
                listBestBanks[2] = listBestBanks[1]
                listBestBanks[1] = listBestBanks[0]
                listBestBanks[0] = bankIndex
            elif float(oneBank[bankId]) > float(listBwstBanksValues[1]):
                listBwstBanksValues[2] = listBwstBanksValues[1]
                listBwstBanksValues[1] = oneBank[6]
                listBestBanks[2] = listBestBanks[1]
                listBestBanks[1] = bankIndex
            elif float(oneBank[bankId]) > float(listBwstBanksValues[2]):
                listBwstBanksValues[2] = oneBank[6]
                listBestBanks[2] = bankIndex
            bankIndex = bankIndex + 1
        return listBestBanks
    elif (direction == 'DOWN'):
        listBestBanks = [0,0,0]
        listBwstBanksValues = [9999,9999,9999]
        bankIndex = 0
        for oneBank in sortObj:
            if float(oneBank[bankId]) < float(listBwstBanksValues[0]):
                listBwstBanksValues[2] = listBwstBanksValues[1]
                listBwstBanksValues[1] = listBwstBanksValues[0]
                listBwstBanksValues[0] = oneBank[7]
                listBestBanks[2] = listBestBanks[1]
                listBestBanks[1] = listBestBanks[0]
                listBestBanks[0] = bankIndex
            elif float(oneBank[7]) < float(listBwstBanksValues[1]):
                listBwstBanksValues[2] = listBwstBanksValues[1]
                listBwstBanksValues[1] = oneBank[7]
                listBestBanks[2] = listBestBanks[1]
                listBestBanks[1] = bankIndex
            elif float(oneBank[7]) < float(listBwstBanksValues[2]):
                listBwstBanksValues[2] = oneBank[7]
                listBestBanks[2] = bankIndex
            bankIndex = bankIndex + 1
        return listBestBanks