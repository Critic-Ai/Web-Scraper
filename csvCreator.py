''' a module that creates a csv file with the review data
call the main function to achieve functionality
'''
from bs4 import BeautifulSoup as BS
import requests
import json
from csv import writer


def get_soup(url):
    ''' a function that goes through the pages and makes the soup
    parameters:
    url: the url of the page
    returns: the text buffer
    '''
    try:
        # print("in get_soup function of csvCreator.py")
        # get the html content of the page
        r = requests.get(url)
        content = r.content
        # parse the html content
        soup = BS(content, "html.parser")

        # pass the soup to get_review_text function
        textBuffer = get_review_text(soup)
        return textBuffer
    except:
        return None


def get_review_text(soup):
    ''' a function that gets the review text
    parameters:
    soup: the soup of the page
    returns: the text buffer
    '''
    # print("in get_review_text function of csvCreator.py")
    textBuffer = ""
    reviews = soup.find_all('p')
    for review in reviews:
        text = review.text
        textBuffer += text
    return textBuffer


def fileCreator(fileName, reviewList):
    ''' a function that creates a csv file with the review data
    parameters:
    fileName: the name of the file
    textBuffer: the text buffer
    '''
    # print("in fileCreator function of csvCreator.py")
    with open('ReviewsCSV/' + fileName, "a", encoding='utf-8-sig', newline='') as file:
        csv_writer = writer(file)

        for review in reviewList:
            textBuffer = None
            textBuffer = get_soup(review[1])
            if textBuffer is not None:
                # print("is not none")
                csv_writer.writerow([review[0], textBuffer])
            else:
                print("Could not get the review for",
                      review[0] + ". Skipping...")
        file.close()
    return


def main(gameName, reviewList):
    ''' a function that creates a csv file with the review data
    parameters:
    gameName: the name of the game
    reviewList: a list of reviews
    returns: nothing
    '''
    # print("in main function of csvCreator.py")
    fileName = gameName + ".csv"
    fileCreator(fileName, reviewList)
    return


if __name__ == "__main__":
    with open('games.json') as json_file:
        gamesList = json.load(json_file)
        gameCount = 0
        start = 61
        end = 61
        for key, value in gamesList.items():
            gameCount += 1
            if gameCount < start or gameCount > end:
                print(gameCount, "). skipping", value['Name'])
                continue
            gameName = value['Name']
            if ":" in gameName:
                gameName = gameName.replace(":", "")
            gameCode = value['Code']
            print("__________________________________________________________")
            print(gameCount, "). Getting reviews for", gameName)

            with open('ReviewsCSV/' + gameName + '.csv', "a", encoding='utf-8-sig', newline='') as file:
                header = ["Outlet", "Review"]
                csv_writer = writer(file)
                csv_writer.writerow(header)
                file.close()

            with open('ReviewsJSON/' + gameCode + '.json') as url_file:
                count = 0
                urlList = json.load(url_file)

                for key, value in urlList.items():
                    if key == "0":
                        count += 1
                        continue
                    # if outlet name has IGN in its name, skip it
                    if "IGN" in value['OutletName']:
                        count += 1
                        print("skipping", value['OutletName'])
                        continue
                    elif "Easy" in value['OutletName']:
                        count += 1
                        print("skipping", value['OutletName'])
                        continue
                    elif "Sixth" in value['OutletName']:
                        count += 1
                        print("skipping", value['OutletName'])
                        continue
                    elif "Areajugones" in value['OutletName']:
                        count += 1
                        print("skipping", value['OutletName'])
                        continue
                    elif "Hobby Consolas" in value['OutletName']:
                        count += 1
                        print("skipping", value['OutletName'])
                        continue

                    reviewList = [[value['OutletName'], value['ExternalUrl']]]
                    print("getting reviews for", value['OutletName'], count)
                    main(gameName, reviewList)
                    count += 1

                print("CSV file created for", gameName)
                url_file.close()

        json_file.close()

    # gameName = "cyberpunk-2077"
    # url = "https://www.eurogamer.net/articles/2020-12-10-cyberpunk-2077-review-intoxicating-potential-half-undermined-half-met"
    # print("running csvCreator.py for " + gameName + " and url " + url)
    # reviewList = [["Author", "Outlet", url]]
    # main(gameName, reviewList)
    # print("csv file created")
