"""Assignment 3: Tweet Analysis"""

from typing import List, Dict, TextIO, Tuple

HASH_SYMBOL = '#'
MENTION_SYMBOL = '@'
URL_START = 'http'
EOT = "<<<EOT"
DETECT_FAIL = "unknown"

# Order of data in the file
FILE_DATE_INDEX = 0
FILE_LOCATION_INDEX = 1
FILE_SOURCE_INDEX = 2
FILE_FAVOURITE_INDEX = 3
FILE_RETWEET_INDEX = 4

# Order of data in a tweet tuple
TWEET_TEXT_INDEX = 0
TWEET_DATE_INDEX = 1
TWEET_SOURCE_INDEX = 2
TWEET_FAVOURITE_INDEX = 3
TWEET_RETWEET_INDEX = 4


# Helper functions.

def first_alnum_substring(text: str) -> str:
    """Return all alphanumeric characters in text from the beginning up to the
    first non-alphanumeric character, or, if text does not contain any
    non-alphanumeric characters, up to the end of text."
    >>> first_alnum_substring('')
    ''
    >>> first_alnum_substring('IamIamIam')
    'iamiamiam'
    >>> first_alnum_substring('IamIamIam!!')
    'iamiamiam'
    >>> first_alnum_substring('IamIamIam!!andMore')
    'iamiamiam'
    >>> first_alnum_substring('$$$money')
    ''
    """

    index = 0
    while index < len(text) and text[index].isalnum():
        index += 1
    return text[:index].lower()


def clean_word(word: str) -> str:
    """Return all alphanumeric characters from word, in the same order as
    they appear in word, converted to lowercase.
    >>> clean_word('')
    ''
    >>> clean_word('AlreadyClean?')
    'alreadyclean'
    >>> clean_word('very123mes$_sy?')
    'very123messy'
    """

    cleaned_word = ''
    for char in word.lower():
        if char.isalnum():
            cleaned_word = cleaned_word + char
    return cleaned_word


# TODO:
# Required functions

def extract_mentions(text: str) -> List[str]:
    """Return a list of all mentions in text,
    converted to lowercase, with duplicates included.
    >>> extract_mentions('Hi @UofT do you like @cats @CATS #meowmeow')
    ['uoft', 'cats', 'cats']
    >>> extract_mentions('@cats are #cute @cats @cat meow @meow')
    ['cats', 'cats', 'cat', 'meow']
    >>> extract_mentions('@many @cats$extra @meow?!')
    ['many', 'cats', 'meow']
    >>> extract_mentions('No valid mentions @! here?')
    []
    """
    all_mentions = []
    tweet_words = text.strip().split()
    for i in range(len(tweet_words)):
        if tweet_words[i].startswith(MENTION_SYMBOL):
            tweet_words[i] = first_alnum_substring(tweet_words[i][1:])
            if len(tweet_words[i]) > 0:
                all_mentions.append(tweet_words[i])
    return all_mentions


def extract_hashtags(text: str) -> List[str]:
    """return  a list containing all of the
    unique hash_tags in the text,
    in the order they appear in the text,
    converted to lowercase.
    >>> extract_hashtags('Hi #UofT do you like @cats @CATS #meowmeow')
    ['uoft', 'meowmeow']
    >>> extract_hashtags('@cats are #cute @cats #cute meow @meow')
    ['cute']
    >>> extract_hashtags('@many #cats$extra #meow?!')
    ['cats', 'meow']
    >>> extract_hashtags('No valid mentions #! here?')
    []

    """
    all_hashtags = []
    n_text = text.split(" ")
    for i in range(len(n_text)):
        if HASH_SYMBOL in n_text[i]:
            hashtag = n_text[i][1:]
            if not (first_alnum_substring(hashtag)) == "":
                if first_alnum_substring(hashtag) not in all_hashtags:
                    all_hashtags.append(first_alnum_substring(hashtag))
    return all_hashtags


def count_words(text: str, words_count: Dict[str, int]) -> None:
    """
    >>> before = {"nick":0, "forest":0,"google":0, "brain":0, "researcher":0, "by":0, "day":0, "singer":0, "night":1}
    >>> count_words("#UofT Nick Forest: Google Brain re-searcher by day, singer @goodkidband by night!", before)
    >>> expected = {"nick":1, "forest":1,"google":1, "brain":1, "researcher":1, "by":2, "day":1, "singer":1, "night":2}
    >>> before == expected
    True
    """
    split_t = text.split(" ")
    for i in range(len(split_t)):
        if not (HASH_SYMBOL in split_t[i]) and \
                not (MENTION_SYMBOL in split_t[i]) and \
                not (URL_START in split_t[i]):
            if clean_word(split_t[i]) not in words_count:
                words_count[clean_word(split_t[i])] = 1
            else:
                words_count[clean_word(split_t[i])] = \
                    words_count[clean_word(split_t[i])] + 1


def common_words(words_count: Dict[str, int], n: int) -> None:
    """
    Update the given dictionary so that
    it only includes the most common words
    >>> before =  {"nick":1, "forest":1,"google":1, "brain":1, "researcher":1, \
    "by":2, "day":1, "singer":1, "night":1}
    >>> common_words(before, 1)
    >>> expected = {"by":2}
    >>> expected == before
    True
    """

    words = []
    for i in words_count:
        words.append([words_count[i], i])
    words.sort(reverse=True)
    tmp = words[:n]
    if n < len(words):
        i = len(tmp) - 1
        while i >= 0 and tmp[i][0] == words[n][0]:
            i -= 1
        tmp = tmp[:i + 1]
    words_count.clear()
    for i in tmp:
        words_count[i[1]] = i[0]


def read_tweets(fp: TextIO) -> Dict[str, List[tuple]]:
    """
    Read all of the data from the given file into a dictionary
    """
    tweets_d = {}
    i = 0
    tweets_lines = fp.readlines()
    user = ""

    while i < len(tweets_lines):
        if tweets_lines[i].strip()[-1] == ":":
            user = tweets_lines[i].strip().replace(":", "")
        else:
            tweet_lst = tweets_lines[i].strip().split(",")
            text = ""
            flag = True
            while flag:
                i += 1
                if EOT in tweets_lines[i]:
                    flag = False
                else:
                    text += tweets_lines[i]
            if user not in tweets_d:
                tweets_d[user] = []
            tweets_d[user].append((text.strip(), int(tweet_lst[FILE_DATE_INDEX]),
                                   tweet_lst[FILE_SOURCE_INDEX],
                                   int(tweet_lst[FILE_FAVOURITE_INDEX]),
                                   int(tweet_lst[FILE_RETWEET_INDEX])))
        i += 1
    return tweets_d


def most_popular(tweets_d: Dict[str, List[tuple]], begin_date: int, end_date: int) -> str:
    """
    Return a list of the most popular candidates
    between begin_date and end_date
    >>> most_popular({'people1':[( 'text1', 104,'android', 2, 3), \
                                 ( 'text2', 105, 'android', 4, 5)],\
                      'people2':[( 'text1', 102, 'android', 1, 0),\
                                 ( 'text2', 106, 'android', 6, 7)]},0, 105)
    'people1'
    >>> most_popular({'people1':[( 'text1', 104,'android', 2, 3), \
                                 ( 'text2', 105, 'android', 4, 5)],\
                      'people2':[( 'text1', 102, 'android', 1, 0),\
                                 ( 'text2', 106, 'android', 6, 7)]},0, 106)
    'tie'
    >>> most_popular({'people1':[( 'text1', 104,'android', 2, 3), \
                                 ( 'text2', 105, 'android', 4, 5)],\
                      'people2':[( 'text1', 102, 'android', 1, 0),\
                                 ( 'text2', 106, 'android', 6, 7)]},105, 106)
    'people2'
    """
    words_count = []
    for user in tweets_d:
        user_pop = 0
        for i in range(len(tweets_d[user])):
            if begin_date <= tweets_d[user][i][TWEET_DATE_INDEX] and \
                            tweets_d[user][i][TWEET_DATE_INDEX] <= end_date:
                user_pop += tweets_d[user][i][TWEET_FAVOURITE_INDEX]
                user_pop += tweets_d[user][i][TWEET_RETWEET_INDEX]
        if user_pop > 0:
            words_count.append((user_pop, user))
    words_count.sort(reverse=True)
    if len(words_count) == 0 or \
                            len(words_count) > 1 and \
                            words_count[0][0] == words_count[1][0]:
        return "tie"
    return words_count[0][1]


def detect_author(tweets_d: Dict[str, List[tuple]], to_detect: str) -> str:
    """
    Return of most likely author of the tweet
    using the hash_tags in tweets_d.
    >>> detect_author({'people1':[( '#hello #love', 104,'android', 2, 3), \
                                 ( 'text2', 105, 'android', 4, 5)],\
                      'people2':[( '#nice', 102, 'android', 1, 0),\
                                 ( 'text2', 106, 'android', 6, 7)]},"#hello world #love")
    'people1'
    >>> detect_author({'people1':[( '#hello #love', 104,'android', 2, 3), \
                                 ( 'text2', 105, 'android', 4, 5)],\
                      'people2':[( '#hello', 102, 'android', 1, 0),\
                                 ( 'text2', 106, 'android', 6, 7)]},"#hello world #love")
    'unknown'

    """
    all_hash_tags = {}
    for user in tweets_d:
        for i in range(len(tweets_d[user])):
            hash_tags = extract_hashtags(tweets_d[user][i][TWEET_TEXT_INDEX])
            for j in range(len(hash_tags)):
                if hash_tags[j] not in all_hash_tags:
                    all_hash_tags[hash_tags[j]] = []
                all_hash_tags[hash_tags[j]].append(user)
    hash_tags = extract_hashtags(to_detect)
    if len(hash_tags) == 0:
        return DETECT_FAIL
    for i in range(len(hash_tags)):
        if hash_tags[i] in all_hash_tags:
            if len(all_hash_tags[hash_tags[i]]) > 1:
                return DETECT_FAIL
            else:
                if all_hash_tags[hash_tags[i]][0] != all_hash_tags[hash_tags[0]][0]:
                    return DETECT_FAIL
        else:
            return DETECT_FAIL
    return all_hash_tags[hash_tags[0]][0]


if __name__ == '__main__':
    pass





    # If you add any function calls for testing, put them here.
    # Make sure they are indented, so they are within the if statement body.
    # That includes all calls on print, open, and doctest.

    # import doctest
    # doctest.testmod()
