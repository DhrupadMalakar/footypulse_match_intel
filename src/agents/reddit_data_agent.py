from typing import List, Dict, Any
from src.tools.reddit_fetcher import RedditFetcher
from src.models.domain_models import map_comments_from_raw
from src.observability.metrics import Metrics
from src.memory.memory_bank import MemoryBank
from src.memory.session_memory import SessionMemory
import logging


class RedditDataAgent:
    def __init__(
        self,
        logger: logging.Logger,
        metrics: Metrics,
        memory_bank: MemoryBank,
        session_memory: SessionMemory,
        demo_mode: bool,
        sample_path: str,
    ) -> None:
        self.logger = logger
        self.metrics = metrics
        self.memory_bank = memory_bank
        self.session_memory = session_memory
        self.demo_mode = demo_mode
        self.sample_path = sample_path
        self.fetcher = RedditFetcher()

    def run(self) -> List[Dict[str, Any]]:
        if self.demo_mode:
            self.logger.info('RedditDataAgent: loading sample data from file')
            raw_comments = self.fetcher.load_from_file(self.sample_path)
        else:
            self.logger.info('RedditDataAgent: demo_mode is False, using sample file for now')
            raw_comments = self.fetcher.load_from_file(self.sample_path)

        self.metrics.increment('comments_loaded', len(raw_comments))
        self.logger.info(f'RedditDataAgent: loaded {len(raw_comments)} comments')

        comments = map_comments_from_raw(raw_comments)
        self.session_memory.set('raw_comments', raw_comments)

        self.memory_bank.append_entry({'type': 'reddit_fetch', 'num_comments': len(raw_comments)})

        comments_dicts = []
        for c in comments:
            comments_dicts.append(
                {
                    'author': c.author,
                    'text': c.text,
                    'team': c.team,
                    'sentiment': c.sentiment,
                    'score': c.score,
                }
            )
        return comments_dicts
