from typing import List
from src.models.domain_models import SentimentSummary, PlayerImpact
from src.observability.metrics import Metrics
from src.memory.memory_bank import MemoryBank
from src.memory.session_memory import SessionMemory
import logging


class MatchSummaryAgent:
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

    def run(self, sentiment_summary: SentimentSummary, player_impacts: List[PlayerImpact]) -> str:
        total = sentiment_summary.positive + sentiment_summary.negative + sentiment_summary.neutral
        if total == 0:
            mood_line = 'Fans did not share many thoughts about this match.'
        else:
            if sentiment_summary.positive > sentiment_summary.negative:
                mood = 'overall positive'
            elif sentiment_summary.negative > sentiment_summary.positive:
                mood = 'mostly frustrated'
            else:
                mood = 'mixed'
            mood_line = f'Fan mood was {mood}, based on {total} comments.'

        if player_impacts:
            sorted_players = sorted(player_impacts, key=lambda p: p.impact_score, reverse=True)
            top_player = sorted_players[0]
            top_line = (
                f'The standout player was {top_player.player_name} for {top_player.team}, '
                f'with an impact score of {top_player.impact_score}.'
            )
        else:
            top_line = 'Player impact data was limited for this match.'

        summary = f'{mood_line} {top_line}'

        self.metrics.increment('summaries_created', 1)
        self.logger.info('MatchSummaryAgent: created summary')

        self.memory_bank.append_entry({'type': 'match_summary', 'summary': summary})
        self.session_memory.set('match_summary', summary)
        return summary
