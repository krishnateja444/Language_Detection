# Language_Detection
Multilingual language detection system built using Data Structures and Algorithms. Features Trie-based word lookup, Dynamic Programming (Levenshtein Edit Distance) for typo-tolerant matching, Hash Map frequency scoring, and Heap-based language ranking for English, French, and Hindi detection.
This project implements a multilingual language detection system using fundamental Data Structures and Algorithms concepts. The system leverages Trie-based dictionaries for efficient word searches, Dynamic Programming for Levenshtein Edit Distance calculations, Hash Maps for frequency-based scoring, and Heap/Priority Queues for ranking candidate languages. It supports English, French, and Hindi language identification while handling minor spelling errors through fuzzy matching techniques. The project demonstrates practical applications of trees, dynamic programming, hashing, heaps, and string-processing algorithms in a real-world text classification problem.
Time Complexity

• Trie Search: O(L)
  - L = length of the input word.
    
• Edit Distance: O(m × n)
  - m = length of the input word.
  - n = length of the dictionary word being compared.
    
• Heap Ranking: O(k log N)
  - k = number of top language predictions returned.
  - N = total number of supported languages.
