import reviewCollector
import csvCreator
import gameListCreator
import json

if __name__ == "__main__":
    url = "https://opencritic.com/browse/all/all-time/num-reviews"
    games = {}
    for i in range(1, 4):
        if i == 1:
            url = "https://opencritic.com/browse/all/all-time/num-reviews"
        else:
            url = "https://opencritic.com/browse/all/all-time/num-reviews?page=" + \
                str(i)
        temp = gameListCreator.main(url)
        # add the new games to the games dictionary
        games.update(temp)

    # count = 0
    # for obj in games:
    #     count += 1
    #     print("Game number", count, "of", len(games))
    #     gameName = obj['Name']
    #     url = obj['URL']
    #     print("Getting reviews for", gameName)
    #     reviewList = reviewCollector.main(url)
    #     csvCreator.main(gameName, reviewList)

    # conver the games dictionary to a json file
    with open('games.json', 'w') as outfile:
        json.dump(games, outfile)
