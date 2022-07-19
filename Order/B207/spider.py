import re
import cfscrape
import openpyxl
import asyncio
import json
import time
import concurrent.futures

scraper = cfscrape.create_scraper()
pageAmount = int(scraper.get("https://search-app.prod.ecommerce.elsevier.com/api/search", params={"labels": "journals", "locale": "global"}).json()["pagination"]["totalNumberOfPages"])
month = {"January": "1", "February": "2", "March": "3", "April": "4", "May": "5", "June": "6", "July": '7', "August": "8", "September": "9", "October": "10", "November": "11", "December": "12"}
year = [2019, 2020, 2021]
allData = []
errorPages = []


def api1(pageNumber):
    time.sleep(1)
    return scraper.get("https://search-app.prod.ecommerce.elsevier.com/api/search", params={"labels": "journals", "page": pageNumber, "locale": "global"}).json()["hits"]


def api2(journalISSN, year):
    time.sleep(1)
    return scraper.get(f"https://www.sciencedirect.com/journal/{journalISSN}/year/{year}/issues").json()["data"]


def api3(journalISSN, tempTitle, uriLookup):
    time.sleep(2)
    try:
        return scraper.get(f"https://www.sciencedirect.com/journal/{journalISSN}/issue/articles", params={"path": f"/journal/{tempTitle}{uriLookup}", "title": tempTitle}).json()["data"]["issueBody"]["issueSec"]
    except:
        return [scraper.get(f"https://www.sciencedirect.com/journal/{journalISSN}/issue/articles", params={"path": f"/journal/{tempTitle}{uriLookup}", "title": tempTitle}).json()["data"]["issueBody"]]


def api4(articleHref):
    time.sleep(5)
    return scraper.get(f"https://www.sciencedirect.com{articleHref}").text


def getCountry(data):
    for m in data:
        if m["#name"] == "affiliation":
            for z in m["$$"]:
                if z["#name"] == "affiliation":
                    for x in z["$$"]:
                        if x["#name"] == "country":
                            return x["_"]
    return ""


def transferDate(date):
    if date == "":
        return date
    date = date.split(" ")
    date.reverse()
    date[1] = month[date[1]]
    return "/".join(date)


async def crawl(pageNumber):
    try:
        loop = asyncio.get_running_loop()
        future1 = loop.run_in_executor(None, api1, pageNumber)
        data = await future1
        for i in data:
            journalTitle = i["title"]
            tempTitle = journalTitle.replace(",", "").replace(":", "").replace(" ", "-").replace("&", "and").lower()
            journalISSN = i["issn"].replace("-", "")
            for y in year:
                try:
                    future2 = loop.run_in_executor(None, api2, journalISSN, y)
                    data2 = await future2
                except:
                    continue
                for j in data2:
                    uriLookup = j["uriLookup"]
                    volume = j["volumeFirst"]
                    print(f"page:{pageNumber} issn:{journalISSN} year:{y} volume:{volume}")
                    future3 = loop.run_in_executor(None, api3, journalISSN, tempTitle, uriLookup)
                    try:
                        data3 = await future3
                    except:
                        continue
                    for k in data3:
                        try:
                            tempk = k["includeItem"]
                            if len(tempk) == 0:
                                raise Exception
                        except:
                            continue
                        for l in tempk:
                            articleHref = l["href"]
                            articleTitle = l["title"]
                            future4 = loop.run_in_executor(None, api4, articleHref)
                            data4 = await future4
                            data4temp = json.loads(re.findall('<script type="application/json" data-iso-key="_0">(.*?)</script>', data4)[0])
                            try:
                                data4temp2 = data4temp["authors"]["content"][0]["$$"]
                                authorCountry = getCountry(data4temp2)
                            except:
                                authorCountry = ""
                            data4temp3 = data4temp["article"]["dates"]
                            receivedDate = transferDate(data4temp3.get("Received", ""))
                            revisedDate = data4temp3.get("Revised", [])
                            for m in range(len(revisedDate)):
                                revisedDate[m] = transferDate(revisedDate[m])
                            acceptedDate = transferDate(data4temp3.get("Accepted", ""))
                            availableOnlineDate = transferDate(data4temp3.get("Available online", ""))
                            versionOfRecordDate = transferDate(data4temp3.get("Version of Record", ""))
                            dataList = ["ELSEVIER", journalTitle, y, volume, articleTitle, authorCountry, receivedDate,
                                        ",".join(revisedDate), acceptedDate, availableOnlineDate, versionOfRecordDate, "", ""]
                            allData.append(dataList)
        return 1
    except:
        print(f"[Fatal Error]page:{pageNumber}")
        errorPages.append(pageNumber)
        return 0


async def main():
    taskList = [asyncio.create_task(crawl(p)) for p in range(1, pageAmount + 1)]
    done, pending = await asyncio.wait(taskList)
    print(errorPages)
    WorkBook = openpyxl.load_workbook('1.xlsx')
    Sheet = WorkBook.active
    Sheet.append(allData)
    WorkBook.save("1.xlsx")

asyncio.run(main())
