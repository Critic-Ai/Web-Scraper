import requests
import json
import time


def main():
    url = "https://opencritic-api.p.rapidapi.com/reviews/game/"
    count = 0
    # go through the games.json file and get the code for each game
    with open('games.json') as json_file:
        gamesList = json.load(json_file)
        for key, value in gamesList.items():

            time.sleep(1)

            gameCode = value['Code']
            gameName = value['Name']
            print("Getting reviews for", gameName,
                  "(", count+1, "of", len(gamesList), ")")

            if count <= 31:
                count += 1
                print("skipping")
                continue

            url += gameCode
            querystring = {"sort": "blend"}

            headers = {
                "X-RapidAPI-Key": "3bd92d4f44mshda83084edcc95c9p14849ajsncbb623fc8712",
                "X-RapidAPI-Host": "opencritic-api.p.rapidapi.com"
            }

            response = requests.get(url, headers=headers, params=querystring)

            reviews = {}
            reviews["0"] = {
                "Code": gameCode,
                "Name": gameName
            }
            _ = 0
            for review in response.json():
                temp = {}
                _ += 1
                print(_, "of", len(response.json()))
                ExternalUrl = review["externalUrl"]
                OutletName = review['Outlet']["name"]
                temp = {'ExternalUrl': ExternalUrl,
                        'OutletName': OutletName
                        }
                reviews[_] = temp

            with open('ReviewsJSON/' + gameCode + '.json', 'w') as outfile:
                json.dump(reviews, outfile)

            url = "https://opencritic-api.p.rapidapi.com/reviews/game/"

            count += 1

        # close the json file
        json_file.close()


if __name__ == "__main__":
    # url = "https://opencritic-api.p.rapidapi.com/reviews/game/463"

    # querystring = {"sort": "blend"}

    # headers = {
    #     "X-RapidAPI-Key": "3bd92d4f44mshda83084edcc95c9p14849ajsncbb623fc8712",
    #     "X-RapidAPI-Host": "opencritic-api.p.rapidapi.com"
    # }

    # response = requests.get(url, headers=headers, params=querystring)

    # print(response.json())
    main()
