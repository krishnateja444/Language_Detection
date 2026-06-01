import os
import string
import heapq


# ---------------------------
# Trie Data Structure
# ---------------------------

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.frequency = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, frequency):
        node = self.root

        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()

            node = node.children[char]

        node.is_end = True
        node.frequency = frequency

    def search(self, word):
        node = self.root

        for char in word:
            if char not in node.children:
                return None

            node = node.children[char]

        if node.is_end:
            return node.frequency

        return None


# ---------------------------
# Text Processing
# ---------------------------

def tokenize(text):
    translator = str.maketrans('', '', string.punctuation)

    words = []

    for word in text.split():
        word = word.translate(translator).lower()

        if len(word) > 1:
            words.append(word)

    return words


# ---------------------------
# Dynamic Programming
# Edit Distance
# ---------------------------

def edit_distance(a, b):
    m = len(a)
    n = len(b)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i

    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):

            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]

            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # delete
                    dp[i][j - 1],      # insert
                    dp[i - 1][j - 1]   # replace
                )

    return dp[m][n]


# ---------------------------
# Load Dictionaries
# ---------------------------

def load_dictionaries(folder):
    language_tries = {}
    language_words = {}

    for filename in os.listdir(folder):

        if not filename.endswith(".txt"):
            continue

        language = filename[:-4]

        trie = Trie()
        words = {}

        filepath = os.path.join(folder, filename)

        with open(filepath, "r", encoding="utf-8") as f:

            for line in f:

                parts = line.strip().split()

                if len(parts) != 2:
                    continue

                word, freq = parts

                try:
                    freq = int(freq)
                except ValueError:
                    continue

                word = word.lower()

                trie.insert(word, freq)
                words[word] = freq

        language_tries[language] = trie
        language_words[language] = words

    return language_tries, language_words


# ---------------------------
# Language Detection
# ---------------------------

def detect_language(sentence, language_tries, language_words):

    words = tokenize(sentence)

    if not words:
        return None

    scores = {lang: 0 for lang in language_tries}

    for word in words:

        for language in language_tries:

            trie = language_tries[language]

            # Exact Match Using Trie
            freq = trie.search(word)

            if freq is not None:
                scores[language] += 10 + freq
                continue

            # Fuzzy Matching Using Edit Distance
            best_score = 0

            for dict_word in language_words[language]:

                if abs(len(word) - len(dict_word)) > 2:
                    continue

                dist = edit_distance(word, dict_word)

                if dist <= 2:
                    best_score = max(best_score, 3 - dist)

            scores[language] += best_score

    return scores


# ---------------------------
# Top-K Languages using Heap
# ---------------------------

def top_languages(scores, k=3):

    heap = []

    for language, score in scores.items():
        heapq.heappush(heap, (-score, language))

    result = []

    while heap and len(result) < k:
        score, language = heapq.heappop(heap)
        result.append((language, -score))

    return result


# ---------------------------
# Main
# ---------------------------

def main():

    folder = "dictionaries"

    language_tries, language_words = load_dictionaries(folder)

    sentence = input("Enter a sentence: ")

    scores = detect_language(
        sentence,
        language_tries,
        language_words
    )

    if not scores:
        print("Detected Language: Unknown")
        return

    ranking = top_languages(scores)

    total = sum(scores.values())

    print("\nLanguage Rankings:")

    for language, score in ranking:

        confidence = (
            score / total * 100
            if total > 0 else 0
        )

        print(
            f"{language:<10} "
            f"Score = {score:<5} "
            f"Confidence = {confidence:.2f}%"
        )

    print(f"\nDetected Language: {ranking[0][0]}")


if __name__ == "__main__":
    main()