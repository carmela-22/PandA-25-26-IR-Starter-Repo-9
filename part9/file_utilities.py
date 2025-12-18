from typing import List
import json
import os
import urllib.request
import urllib.error


from models import Configuration, Sonnet
from constants import POETRYDB_URL, CACHE_FILENAME


DEFAULT_CONFIG = Configuration()

def module_relative_path(name: str) -> str:
    return os.path.join(os.path.dirname(__file__), name)

def fetch_sonnets_from_api() -> List[Sonnet]:
    sonnets = []
    try:
        with urllib.request.urlopen(POETRYDB_URL, timeout=10) as response:
            status = getattr(response, "status", None)
            if status not in (None, 200):
                raise RuntimeError(f"Request failed with HTTP status {status}")

            try:
                sonnets = json.load(response)
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"Failed to decode JSON: {exc}") from exc

    except (urllib.error.HTTPError,
            urllib.error.URLError,
            TimeoutError) as exc:
        raise RuntimeError(f"Network-related error occured: {exc}")

    return sonnets

def load_sonnets() -> List[Sonnet]:
    sonnets_path = module_relative_path(CACHE_FILENAME)

    if os.path.exists(sonnets_path):
        try:
            with open(sonnets_path, "r", encoding="utf-8") as f:
                try:
                    sonnets = json.load(f)
                except json.JSONDecodeError as exc:
                    raise RuntimeError(f"Corrupt cache file (invalid JSON): {exc}") from exc
        except (OSError, IOError) as exc:
            raise RuntimeError(f"Failed to read cache file: {exc}") from exc

        print("Loaded sonnets from the cache.")
    else:
        sonnets = fetch_sonnets_from_api()
        try:
            with open(sonnets_path, "w", encoding="utf-8") as f:
                try:
                    json.dump(sonnets, f, indent=2, ensure_ascii=False)
                except (TypeError, ValueError) as exc:
                    raise RuntimeError(f"Failed to serialize JSON for cache: {exc}") from exc
        except (OSError, IOError) as exc:
            raise RuntimeError(f"Failed to write cache file: {exc}") from exc

        print("Downloaded sonnets from PoetryDB.")

    return [Sonnet(data) for data in sonnets]


def load_config() -> Configuration:
    config_file_path = module_relative_path("config.json")

    cfg = DEFAULT_CONFIG.copy()
    try:
        with open(config_file_path) as config_file:
            cfg.update(json.load(config_file))
    except FileNotFoundError:
        print("No config.json found. Using default configuration.")
        return cfg
    except json.JSONDecodeError:
        print("config.json is invalid. Using default configuration.")
        return cfg
    except OSError:
        print("Could not read config.json. Using default configuration.")
        return cfg

    return cfg