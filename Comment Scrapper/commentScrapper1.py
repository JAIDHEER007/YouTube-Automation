import os
import json
import requests

# Url to get comments list
baseURL = "https://www.googleapis.com/youtube/v3/commentThreads"
baseURL = baseURL.__add__("?part=replies,snippet&maxResults=100&textFormat=html")


def saveCommentsJson(fileCount = 0, **kwargs):
    url = baseURL[:]
    try:
        videoId = kwargs['videoID']
        key = kwargs['API_KEY']

        # print(type(key))

        url = url.__add__("&videoId=")
        url = url.__add__(videoId)
        url = url.__add__("&key=")
        url = url.__add__(key)

    except KeyError as ke:
        raise Exception('Missing {element}'.format(element = ke))

    # Check for the next page token
    try:
        pageToken = kwargs['pageToken']
        url = url.__add__("&pageToken=")
        url = url.__add__(pageToken)
    except KeyError:
        pass

    req = requests.get(url)
    reqData = req.text

    if req.status_code != 200:
        try: 
            errorData = json.loads(reqData)["error"]
        except KeyError:
            raise Exception("Error Occured. Cehck the URL")
        except json.JSONDecodeError:
            raise Exception("Cannot Parse the Request Data. Check the URL")
        
        raise Exception(errorData["message"])
    
    commentData = json.loads(reqData)
    with open(os.path.join(fpath, "commentsJSON{fileCount}.json".format(fileCount = fileCount)), "w") as fileHandle:
        json.dump(commentData, fileHandle)

    try:
        nextPageToken = commentData['nextPageToken']
        saveCommentsJson((fileCount + 1), videoID = videoId, API_KEY = key, pageToken = nextPageToken)
    except: pass

    


if __name__ == '__main__':
    # Current Working Directory
    cwd = os.path.dirname(__file__)

    baseDir = os.path.join(cwd, '..')

    # # Enter your api key
    # API_KEY =   ""          

    try:
        with open(os.path.join(baseDir, "apikey.txt")) as fileHandle:
            API_KEY = fileHandle.readline().strip()
    
        # Enter vedio id
        videoID = "UxJt5xaE3OA"    

        # Folder Path
        fpath = os.path.join(cwd, videoID)

        # Create a folder
        if not os.path.exists(fpath):
            os.mkdir(fpath)

        try:
            saveCommentsJson(videoID = videoID, API_KEY = API_KEY)
        except Exception as exp:
            print(exp)
    
    except FileNotFoundError:
        print("Cannot Find the API KEY text file. Create One as apikey.txt")

    




