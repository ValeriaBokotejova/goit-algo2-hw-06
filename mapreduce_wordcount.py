"""
mapreduce_wordcount.py

Fetch text from URL (or default), count word frequencies in parallel,
and show top N words.
"""

import argparse
import re
import requests
import multiprocessing as mp
from collections import Counter
import matplotlib.pyplot as plt

def fetch_text(url: str) -> str:
    r = requests.get(url, timeout=10)
    r.raise_for_status()
    return r.text

def preprocess(text: str) -> list:
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', ' ', text)
    return text.split()

def map_worker(words_slice: list) -> Counter:
    return Counter(words_slice)

def reduce_counters(counters: list) -> Counter:
    total = Counter()
    for c in counters:
        total.update(c)
    return total

def visualize_top_words(counts: Counter, top_n: int):
    most_common = counts.most_common(top_n)
    words, freqs = zip(*most_common)
    plt.figure(figsize=(10, 6))
    plt.barh(words, freqs)
    plt.xlabel("Frequency")
    plt.title(f"Top {top_n} Words")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "url",
        nargs="?",
        default="https://www.gutenberg.org/files/1342/1342-0.txt",
        help="Text URL (default: Pride & Prejudice)"
    )
    parser.add_argument("--top", type=int, default=10,
                        help="How many top words to show")
    args = parser.parse_args()

    text = fetch_text(args.url)
    words = preprocess(text)
    if not words:
        print("No words found.")
        return

    # split for Map
    cpu = mp.cpu_count()
    size = len(words) // cpu + 1
    slices = [words[i*size:(i+1)*size] for i in range(cpu)]

    with mp.Pool(cpu) as pool:
        partial = pool.map(map_worker, slices)

    total = reduce_counters(partial)
    visualize_top_words(total, args.top)

if __name__ == "__main__":
    main()
