#!/usr/bin/python3
"""Function to print hot posts on a given Reddit subreddit."""
import requests


def top_ten(subreddit):
    """Print the titles of the 10 hottest posts on a given subreddit.

    If an invalid subreddit is given, print "None".
    """
    url = "https://www.reddit.com/r/{}/hot/.json".format(subreddit)
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"
    }
    params = {
        "limit": 10
    }

    try:
        response = requests.get(url, headers=headers,
                                params=params, allow_redirects=False)
        # If the response is not 200, then the subreddit is likely invalid.
        if response.status_code != 200:
            print("None")
            return

        # Try to parse the JSON data and get the 'children' list
        data = response.json().get("data")
        if not data:
            print("None")
            return

        children = data.get("children")
        if not children:
            print("None")
            return

        # Print the title for each of the 10 posts
        for child in children:
            # Safely navigate the nested structure
            title = child.get("data", {}).get("title")
            if title:
                print(title)
    except Exception:
        # If any error occurs (e.g., invalid JSON), print "None"
        print("None")


# For manual testing:
if __name__ == "__main__":
    # Replace 'programming' with any subreddit you wish to test.
    top_ten("programming")
