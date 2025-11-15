from typing import List, Dict, Any, Tuple
from src.observability.metrics import Metrics
from src.memory.memory_bank import MemoryBank
from src.memory.session_memory import SessionMemory
from src.models.domain_models import SentimentSummary
import logging


class SentimentAnalysisAgent:
    def __init__(
        self,
        logger: logging.Logger,
        metrics: Metrics,
        memory_bank: MemoryBank,
        session_memory: SessionMemory,
    ) -> None:
        self.logger = logger
        self.metrics = metrics
        self.memory_bank = memory_bank
        self.session_memory = session_memory

        self.positive_words = {'great','amazing','good','love','fantastic','brilliant','excellent','win'}
        self.negative_words = {'bad','terrible','awful','hate','worst','poor','lose','loss'}

    def _score_comment(self, text: str) -> int:
        text_lower = text.lower()
        score = 0
        for w in self.positive_words:
            if w in text_lower:
                score += 1
        for w in self.negative_words:
            if w in text_lower:
                score -= 1
        return score

    def _label_from_score(self, score: int) -> str:
        if score > 0:
            return 'positive'
        if score < 0:
            return 'negative'
        return 'neutral'

    def run(self, comments: List[Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], SentimentSummary]:
        positive = 0
        negative = 0
        neutral = 0

        for c in comments:
            score = self._score_comment(c.get('text', ''))
            label = self._label_from_score(score)
            c['score'] = score
            c['sentiment'] = label

            if label == 'positive':
                positive += 1
            elif label == 'negative':
                negative += 1
            else:
                neutral += 1

        self.metrics.increment('comments_scored', len(comments))
        self.logger.info(f'SentimentAnalysisAgent: scored {len(comments)} comments')

        summary = SentimentSummary(positive=positive, negative=negative, neutral=neutral)
        self.session_memory.set('sentiment_summary', summary.__dict__)
        self.memory_bank.append_entry(
            {'type': 'sentiment_summary', 'positive': positive, 'negative': negative, 'neutral': neutral}
        )
        return comments, summary
