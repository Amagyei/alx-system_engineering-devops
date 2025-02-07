#!/usr/bin/python3
"""Function to query a list of all hot posts on a given Reddit subreddit."""
import requests


def recurse(subreddit, hot_list=None, after="", count=0):
    """Returns a list of titles of all hot posts on a given subreddit.

    If the subreddit is invalid or an error occurs, returns None.
    """
    if hot_list is None:
        hot_list = []

    url = "https://www.reddit.com/r/{}/hot/.json".format(subreddit)
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"
    }
    params = {
        "after": after,
        "count": count,
        "limit": 100
    }

    # Make the HTTP GET request without following redirects
    response = requests.get(url, headers=headers,
                            params=params, allow_redirects=False)

    # If the status code is not 200, the subreddit might be invalid or another error occurred.
    if response.status_code != 200:
        return None

    # Attempt to parse the JSON data and extract the "data" key.
    data = response.json().get("data")
    if data is None:
        return None

    # Update the 'after' parameter and 'count'
    after = data.get("after")
    count += data.get("dist", 0)

    # Append the title from each post in the "children" list
    for child in data.get("children", []):
        # Use nested .get() calls with defaults to avoid errors if keys are missing
        title = child.get("data", {}).get("title")
        if title:
            hot_list.append(title)

    # If there's another page (after is not None), recurse to get more posts
    if after is not None:
        return recurse(subreddit, hot_list, after, count)

    return hot_list


# Example usage for testing:
if __name__ == "__main__":
    subreddit_name = "programming"  # Change as needed
    titles = recurse(subreddit_name)
    if titles is None:
        print("None")
    else:
        for title in titles:
            print(title)
