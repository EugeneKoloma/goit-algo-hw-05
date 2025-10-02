from kmp import kmp_search
from bm import boyer_moore_search
from rk import rabin_karp_search
from timeit import timeit
from datetime import datetime

if __name__ == "__main__":
    correct_pattern = "кожному кроці"
    wrong_pattern = "this is the wrong pattern"

    # Load texts with encoding fallback
    with open('topic_1.txt', 'rb') as t1, open('topic_2.txt', 'rb') as t2:
        data_1 = t1.read()
        data_2 = t2.read()

    try:
        text_1 = data_1.decode('utf-8')
        text_2 = data_2.decode('utf-8')
    except UnicodeDecodeError:
        # Fall back to cp1251
        text_1 = data_1.decode('cp1251')
        text_2 = data_2.decode('cp1251')

    algorithms = [
        ("KMP", kmp_search),
        ("Boyer–Moore", boyer_moore_search),
        ("Rabin–Karp", rabin_karp_search),
    ]

    topics = [
        ("Topic 1", text_1),
        ("Topic 2", text_2),
    ]

    patterns = [
        ("Correct", correct_pattern),
        ("Wrong", wrong_pattern),
    ]

    # Collect timings
    results = []  # list of dicts: algorithm, topic, pattern, time_s
    for algo_name, algo in algorithms:
        for topic_name, text in topics:
            for pattern_name, patt in patterns:
                t = timeit(lambda: algo(text, patt), number=1)
                results.append({
                    "algorithm": algo_name,
                    "topic": topic_name,
                    "pattern": pattern_name,
                    "time_s": t,
                })

    # Prepare analysis helpers
    def ms(v):
        return v * 1000.0

    # Compute per-(topic,pattern) fastest/slowest
    summary = {}
    for topic_name, _ in topics:
        for pattern_name, _ in patterns:
            subset = [r for r in results if r["topic"] == topic_name and r["pattern"] == pattern_name]
            fastest = min(subset, key=lambda r: r["time_s"]) if subset else None
            slowest = max(subset, key=lambda r: r["time_s"]) if subset else None
            if fastest and slowest and slowest["time_s"] > 0:
                factor = slowest["time_s"] / fastest["time_s"] if fastest["time_s"] > 0 else float('inf')
            else:
                factor = 1.0
            summary[(topic_name, pattern_name)] = (fastest, slowest, factor)

    # Write a richer Markdown report
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open("results.md", "w", encoding="utf-8") as f:
        f.write(f"# String Search Benchmark Results\n\n")
        f.write(f"Generated: {now}\n\n")
        f.write("This report compares three classic string-search algorithms on two text files for two patterns (a known correct match in the texts, and a deliberately absent pattern). Times are wall-clock runtimes for a single search call.\n\n")

        # Table header
        f.write("| Algorithm | Text | Pattern | Time (ms) |\n")
        f.write("|:---------:|:-----|:--------|----------:|\n")

        # Table rows
        for r in results:
            f.write(
                f"| {r['algorithm']} | {r['topic']} | {r['pattern']} | {ms(r['time_s']):.3f} |\n"
            )

        # Summary and Analysis
        f.write("\n## Summary and Analysis\n\n")
        for (topic_name, pattern_name), (fastest, slowest, factor) in summary.items():
            if fastest and slowest:
                f.write(
                    f"- {topic_name} with {pattern_name.lower()} pattern: fastest is {fastest['algorithm']} "
                    f"({ms(fastest['time_s']):.3f} ms); slowest is {slowest['algorithm']} "
                    f"({ms(slowest['time_s']):.3f} ms) — about {factor:.2f}× difference.\n"
                )

        f.write("\n### About the Searching Methods\n\n")
        f.write("- Knuth–Morris–Pratt (KMP): Preprocesses the pattern to build an LPS (longest prefix-suffix) table. Guarantees O(N+M) time; stable performance even when the pattern is absent. Suitable for streaming and Unicode-safe comparisons.\n")
        f.write("- Boyer–Moore (BM): Skips ahead using bad-character and good-suffix heuristics. Often the fastest in practice on large alphabets and when the pattern is not found, due to large jumps. Worst-case can degrade but average is excellent.\n")
        f.write("- Rabin–Karp (RK): Uses rolling hash to compare substrings; average O(N+M), but can suffer from hash collisions depending on implementation. Effective for multiple-pattern search.\n\n")
        f.write("Notes: Actual timings depend on text size, character set, and whether the pattern appears early or not at all. Running multiple iterations and averaging can reduce noise; here we show a single run for simplicity.\n")