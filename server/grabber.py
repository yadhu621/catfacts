import string
import requests
import json

class Grabber:
    """Provide methods to grab data from API"""
    def grab(self, url, filename):
        """
        Usage: grab(URL=url-of-API, filename=path-to-file)

        This method grabs catfacts data from external API.
        It then filters data with the specified condition ( Starting with A, C, E etc.) 
        and saves data to a local file.

        :param :url URL of the API
        :type url: str
        :param filename: Name of the file to save data in.
        :type filename: str
        """
        alphabets = string.ascii_lowercase
        allowed_alphabets = list(alphabets[::2])  # ['a', 'c', 'e', 'g', 'i', 'k', 'm', 'o', 'q', 's', 'u', 'w', 'y']

        proxies = {
            "http": None,
            "https": None,
        }

        # get facts from API
        response = requests.get(url=url, proxies=proxies).json()
        catfacts = response['all']

        # filter catfacts
        filtered_catfacts = []
        for catfact in catfacts:
            if 'user' in catfact and catfact['user']['name']['first'][0].lower() in allowed_alphabets:
                filtered_catfacts.append(catfact)

        # write to file
        print("Total num of catfacts is ", len(catfacts))
        print("Total num of filtered catfacts is ", len(filtered_catfacts))
        with open(filename, 'w') as writer:
            json.dump(filtered_catfacts, writer)
