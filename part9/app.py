#!/usr/bin/env python3
"""
Part 9 starter CLI.

WHAT'S NEW IN PART 9
Our very first new module! And... we are finally again adding new functionality.
"""

# ToDo 1: You will need to move and change some imports
from typing import List
import time
from constants import BANNER, HELP
from models import SearchResult
from file_utilities import load_config, load_sonnets


# ToDo 0: Move find_spans to Sonnet to make this work.


# ToDo 0: You will need to move ansi_highlight to SearchResult as well.


# ToDo 0: Move search_sonnet to the Sonnet class and rename it to 'search_for'


# ToDo 0: Move combine_results to SearchResult. Rename the parameters (use a refactoring of your IDE 😉)!

def print_results(
    query: str,
    results: List[SearchResult],
    highlight: bool,
    highlight_mode: str = "DEFAULT",
    query_time_ms: float | None = None,
) -> None:
    total_docs = len(results)
    matched = [r for r in results if r.matches > 0]

    line = f'{len(matched)} out of {total_docs} sonnets contain "{query}".'
    if query_time_ms is not None:
        line += f" Your query took {query_time_ms:.2f}ms."
    print(line)

    for idx, r in enumerate(matched, start=1):
        r.print(idx, total_docs, highlight, highlight_mode)
        # ToDo 0: From here on move the printing code to SearchResult.print(...)
        #         You should then be able to call r.print(idx, highlight)



# ---------- Paths & data loading ----------
# ToDo 1: Move to file_utilities.py

# ToDo 1: Move to file_utilities.py


# ToDo 1: Move to file_utilities.py

# ------------------------- Config handling ---------------------------------
# ToDo 1: Move to file_utilities.py


# ToDo 1: Move to file_utilities.py


# ToDo 1: Move to file_utilities.py

# ---------- CLI loop ----------

def main() -> None:
    print(BANNER)
    # ToDo 1: Depending on how your imports look, you may need to adapt the call to load_config()
    config = load_config()

    # Load sonnets (from cache or API)
    start = time.perf_counter()
    # ToDo 1: Depending on how your imports look, you may need to adapt the call to load_sonnets()
    sonnets = load_sonnets()

    elapsed = (time.perf_counter() - start) * 1000
    print(f"Loading sonnets took: {elapsed:.3f} [ms]")

    print(f"Loaded {len(sonnets)} sonnets.")

    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not raw:
            continue

        # commands
        if raw.startswith(":"):
            if raw == ":quit":
                print("Bye.")
                break

            if raw == ":help":
                print(HELP)
                continue

            if raw.startswith(":highlight"):
                parts = raw.split()
                if len(parts) == 2 and parts[1].lower() in ("on", "off"):
                    config.highlight = parts[1].lower() == "on"
                    print("Highlighting", "ON" if config.highlight else "OFF")
                    config.save()
                else:
                    print("Usage: :highlight on|off")
                continue
                    # ToDo 1: Depending on how your imports look, you may need to adapt the call to save_config()
                    # ToDo 3: You need to adapt the call to save_config

            if raw.startswith(":search-mode"):
                parts = raw.split()
                if len(parts) == 2 and parts[1].upper() in ("AND", "OR"):
                    config.search_mode = parts[1].upper()
                    print("Search mode set to", config.search_mode)
                    # ToDo 3: You need to adapt the call to save_config
                    config.save()
                else:
                    print("Usage: :search-mode AND|OR")
                continue

            # ToDo 2: A new setting is added here. It's command string is ':hl-mode'.
            if raw.startswith(":hl-mode"):
                parts = raw.split()
                if len(parts) == 2 and parts[1].upper() in ("DEFAULT", "GREEN"):
                    config.highlight_mode = parts[1].upper()
                    print(f"Highlight mode set to {config.highlight_mode}")
                    config.save()
                else:
                    print("Usage: :hl-mode DEFAULT|GREEN")
                continue

            print("Unknown command. Type :help for commands.")
            continue

        # ---------- Query evaluation ----------
        words = raw.split()
        if not words:
            continue

        start = time.perf_counter()

        # query
        combined_results = []


        for word in words:
            # Searching for the word in all sonnets
            # ToDo 0:You will need to adapt the call to search_sonnet
            results = [s.search_for(word) for s in sonnets]

            if not combined_results:
                # No results yet. We store the first list of results in combined_results
                combined_results = results
            else:
                # We have an additional result, we have to merge the two results: loop all sonnets
                for i in range(len(combined_results)):
                    # Checking each sonnet individually
                    combined_result = combined_results[i]
                    result = results[i]

                    if config.search_mode == "AND":
                        if combined_result.matches > 0 and result.matches > 0:
                            # Only if we have matches in both results, we consider the sonnet (logical AND!)
                            # ToDo 0:You will need to adapt the call to combine_results
                            combined_results[i] = combined_result.combine_with(result)
                        else:
                            # Not in both. No match!
                            combined_result.matches = 0
                    elif config.search_mode == "OR":
                        # ToDo 0:You will need to adapt the call to combine_results
                        combined_results[i] = combined_result.combine_with(result)

        # Initialize elapsed_ms to contain the number of milliseconds the query evaluation took
        elapsed_ms = (time.perf_counter() - start) * 1000

        # ToDo 2: You will need to pass the new setting, the highlight_mode to print_results and use it there
        print_results(raw, combined_results, config.highlight, config.highlight_mode, elapsed_ms)

if __name__ == "__main__":
    main()
