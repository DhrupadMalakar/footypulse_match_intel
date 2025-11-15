import json
from typing import List, Dict, Any
import os
import urllib.request


class RedditFetcher:
    def load_from_file(self, path: str) -> List[Dict[str, Any]]:
        if not os.path.exists(path):
            raise FileNotFoundError(f'Sample file not found: {path}')
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('comments', [])

    def fetch_from_url(self, url: str) -> List[Dict[str, Any]]:
        with urllib.request.urlopen(url) as response:
            text = response.read().decode('utf-8')
        data = json.loads(text)
        return data.get('comments', [])
