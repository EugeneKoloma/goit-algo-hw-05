# String Search Benchmark Results

Generated: 2025-10-02 09:56:33

This report compares three classic string-search algorithms on two text files for two patterns (a known correct match in the texts, and a deliberately absent pattern). Times are wall-clock runtimes for a single search call.

| Algorithm | Text | Pattern | Time (ms) |
|:---------:|:-----|:--------|----------:|
| KMP | Topic 1 | Correct | 0.620 |
| KMP | Topic 1 | Wrong | 0.766 |
| KMP | Topic 2 | Correct | 1.228 |
| KMP | Topic 2 | Wrong | 1.020 |
| Boyer–Moore | Topic 1 | Correct | 0.185 |
| Boyer–Moore | Topic 1 | Wrong | 0.125 |
| Boyer–Moore | Topic 2 | Correct | 0.383 |
| Boyer–Moore | Topic 2 | Wrong | 0.150 |
| Rabin–Karp | Topic 1 | Correct | 1.391 |
| Rabin–Karp | Topic 1 | Wrong | 2.017 |
| Rabin–Karp | Topic 2 | Correct | 2.874 |
| Rabin–Karp | Topic 2 | Wrong | 2.778 |

## Summary and Analysis

- Topic 1 with correct pattern: fastest is Boyer–Moore (0.185 ms); slowest is Rabin–Karp (1.391 ms) — about 7.53× difference.
- Topic 1 with wrong pattern: fastest is Boyer–Moore (0.125 ms); slowest is Rabin–Karp (2.017 ms) — about 16.17× difference.
- Topic 2 with correct pattern: fastest is Boyer–Moore (0.383 ms); slowest is Rabin–Karp (2.874 ms) — about 7.50× difference.
- Topic 2 with wrong pattern: fastest is Boyer–Moore (0.150 ms); slowest is Rabin–Karp (2.778 ms) — about 18.51× difference.

### About the Searching Methods

- Knuth–Morris–Pratt (KMP): Preprocesses the pattern to build an LPS (longest prefix-suffix) table. Guarantees O(N+M) time; stable performance even when the pattern is absent. Suitable for streaming and Unicode-safe comparisons.
- Boyer–Moore (BM): Skips ahead using bad-character and good-suffix heuristics. Often the fastest in practice on large alphabets and when the pattern is not found, due to large jumps. Worst-case can degrade but average is excellent.
- Rabin–Karp (RK): Uses rolling hash to compare substrings; average O(N+M), but can suffer from hash collisions depending on implementation. Effective for multiple-pattern search.

Notes: Actual timings depend on text size, character set, and whether the pattern appears early or not at all. Running multiple iterations and averaging can reduce noise; here we show a single run for simplicity.
