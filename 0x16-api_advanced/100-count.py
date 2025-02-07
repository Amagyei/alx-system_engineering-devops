#!/usr/bin/python3
"""Function that queries the Reddit API recursively and prints a sorted count of given keywords."""
import re
import requests


def count_words(subreddit, word_list, counts=None, after="", count=0):
    """
    Queries the Reddit API and prints a sorted count of given keywords
    found in the titles of all hot posts on a given subreddit.

    Parameters:
      subreddit (str): The subreddit to query.
      word_list (list): A list of keywords to count (case-insensitive).
         Duplicates in this list are taken into account.
      counts (dict): Used internally to accumulate counts (do not supply).
      after (str): Used internally for pagination (do not supply).
      count (int): Used internally for pagination (do not supply).

    If the subreddit is invalid or no posts match, prints nothing.
    """
    # On the first call, initialize the dictionaries
    if counts is None:
        # Create frequency dictionary: count duplicates in word_list (all lower-case)
        freq = {}
        for word in word_list:
            w = word.lower()
            freq[w] = freq.get(w, 0) + 1
        # Initialize counts for each keyword (set to zero initially)
        counts = {w: 0 for w in freq}
        # Save frequency dictionary in counts under a reserved key
        counts["_freq"] = freq

    url = "https://www.reddit.com/r/{}/hot/.json".format(subreddit)
    headers = {
        "User-Agent": "linux:0x16.api.advanced:v1.0.0 (by /u/yourusername)"}
    params = {"after": after, "count": count, "limit": 100}
    response = requests.get(url, headers=headers,
                            params=params, allow_redirects=False)

    # If the subreddit is invalid or some error occurred, return None (and print nothing)
    if response.status_code != 200:
        return None

    data = response.json().get("data")
    if not data:
        return None

    after = data.get("after")
    count += data.get("dist", 0)

    # Process each post in the "children" list
    for child in data.get("children", []):
        title = child.get("data", {}).get("title", "")
        # Extract only words (only letters) in lowercase
        words = re.findall(r"[a-zA-Z]+", title.lower())
        for w in words:
            if w in counts and w != "_freq":
                # Each occurrence counts as many times as the frequency in the word list.
                counts[w] += counts["_freq"][w]

    # If there is more data (pagination), recurse
    if after:
        return count_words(subreddit, word_list, counts, after, count)
    else:
        # Remove the reserved key before printing the results
        freq = counts.pop("_freq")
        # Filter out words with 0 count
        result = {word: cnt for word, cnt in counts.items() if cnt > 0}
        if not result:
            return
        # Sort by count (descending) and alphabetically (ascending) if counts are equal
        sorted_result = sorted(result.items(), key=lambda kv: (-kv[1], kv[0]))
        for word, cnt in sorted_result:
            print(f"{word}: {cnt}")
        return


# For testing purposes, you can call the function as follows:
if __name__ == "__main__":
    # Example usage:
    # python3 100-count.py programming "react python java javascript scala no_results_for_this_one"
    import sys
    if len(sys.argv) < 3:
        print("Usage: {} <subreddit> <list of keywords>".format(sys.argv[0]))
    else:
        # Split the second argument on whitespace to form the word_list
        count_words(sys.argv[1], sys.argv[2].split())
