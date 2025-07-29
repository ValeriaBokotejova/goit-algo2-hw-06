# MapReduce Word Count Homework 🚀
_repo: goit-algo2-hw-06_

Process large texts in parallel with Python's MapReduce paradigm and visualize the top N words.

---

## ⚙️ Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

## 🔨 Usage

```bash
python mapreduce_wordcount.py <TEXT_URL> [--top N]
```

- <TEXT_URL> — URL of the text file to analyze
- `--top N` (optional) — number of top words to display (default: 10)

**Example:**

```bash
python mapreduce_wordcount.py https://www.gutenberg.org/files/1342/1342-0.txt --top 15
```
