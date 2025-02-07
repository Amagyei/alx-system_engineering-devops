#!/usr/bin/python3
"""Function to query subscribers on a given Reddit subreddit."""
import requests

def number_of_subscribers(subreddit):
    """Return the total number of subscribers on a given subreddit.
    If an invalid subreddit is given, return 0.
    """
    url = "https://www.reddit.com/r/{}/about.json".format(subreddit)
    headers = {"User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"}
    response = requests.get(url, headers=headers, allow_redirects=False)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        return 0

    # Try to get the data and then the subscribers value
    try:
        results = response.json().get("data")
        if results is None:
            return 0
        subscribers = results.get("subscribers")
        if subscribers is None:
            return 0
        return subscribers
    except Exception:
        return 0
