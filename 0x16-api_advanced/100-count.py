#!/usr/bin/python3
"""Function to count words in all hot posts of a given Reddit subreddit."""
import requests


def count_words(subreddit, word_list, instances=None, after="", count=0):
    """
    Prints counts of given words found in hot posts of a given subreddit.

    Args:
        subreddit (str): The subreddit to search.
        word_list (list): The list of words to search for in post titles.
        instances (dict): A dictionary with words (in lowercase) as keys and counts as values.
        after (str): The parameter for pagination.
        count (int): The current count of posts fetched.
    """
    if instances is None:
        instances = {}

    url = "https://www.reddit.com/r/{}/hot/.json".format(subreddit)
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/bdov_)"
    }
    params = {
        "after": after,
        "count": count,
        "limit": 100
    }

    response = requests.get(url, headers=headers,
                            params=params, allow_redirects=False)
    # If the status code is not 200, then the subreddit is likely invalid.
    if response.status_code != 200:
        print("")
        return

    try:
        results = response.json().get("data")
    except Exception:
        print("")
        return

    # Update pagination info
    after = results.get("after")
    count += results.get("dist", 0)

    # Process each post title in the "children" list
    for child in results.get("children", []):
        # Get the title and convert it to lowercase for case-insensitive matching
        title = child.get("data", {}).get("title", "").lower().split()
        for word in word_list:
            # Compare using lowercase
            if word.lower() in title:
                # Count how many times this word (in lowercase) appears in the title
                times = title.count(word.lower())
                # Use the lower-case version of the word as the key
                if word.lower() in instances:
                    instances[word.lower()] += times
                else:
                    instances[word.lower()] = times

    # If there's a next page, recurse; otherwise, sort and print the results
    if after is not None:
        count_words(subreddit, word_list, instances, after, count)
    else:
        if not instances:
            print("")
            return
        # Sort: first by count descending, then alphabetically ascending
        sorted_instances = sorted(
            instances.items(), key=lambda kv: (-kv[1], kv[0]))
        for word, cnt in sorted_instances:
            print(f"{word}: {cnt}")


# For testing purposes:
if __name__ == "__main__":
    # Example usage; replace "programming" and word list as needed.
    count_words("programming", ["Python", "javascript", "java"])
