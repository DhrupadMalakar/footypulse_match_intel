import json
from typing import List, Dict, Any
import os
from src.observability.metrics import Metrics
from src.memory.memory_bank import MemoryBank
from src.memory.session_memory import SessionMemory
from src.models.domain_models import PlayerImpact
import logging


class PlayerImpactAgent:
    def __init__(
        self,
        logger: logging.Logger,
        metrics: Metrics,
        memory_bank: MemoryBank,
        session_memory: SessionMemory,
        sample_stats_path: str,
        demo_mode: bool,
    ) -> None:
        self.logger = logger
        self.metrics = metrics
        self.memory_bank = memory_bank
        self.session_memory = session_memory
        self.sample_stats_path = sample_stats_path
        self.demo_mode = demo_mode

    def _load_stats(self) -> Dict[str, Any]:
        if not os.path.exists(self.sample_stats_path):
            raise FileNotFoundError(f'Stats file not found: {self.sample_stats_path}')
        with open(self.sample_stats_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def run(self, comments_with_sentiment: List[Dict[str, Any]]) -> List[PlayerImpact]:
        stats = self._load_stats()
        players_raw = stats.get('players', [])

        sentiment_by_player: Dict[str, int] = {}
        for c in comments_with_sentiment:
            text = c.get('text', '').lower()
            score = c.get('score', 0)
            for player in players_raw:
                name_lower = player.get('name', '').lower()
                if name_lower and name_lower in text:
                    sentiment_by_player[name_lower] = sentiment_by_player.get(name_lower, 0) + score

        player_impacts: List[PlayerImpact] = []
        for player in players_raw:
            name = player.get('name', 'unknown')
            team = player.get('team', 'unknown')
            goals = int(player.get('goals', 0))
            assists = int(player.get('assists', 0))
            cards = int(player.get('cards', 0))
            sentiment_score = sentiment_by_player.get(name.lower(), 0)
            impact_score = goals * 3 + assists * 2 - cards + sentiment_score

            player_impacts.append(
                PlayerImpact(
                    player_name=name,
                    team=team,
                    goals=goals,
                    assists=assists,
                    cards=cards,
                    sentiment_score=sentiment_score,
                    impact_score=impact_score,
                )
            )

        self.metrics.increment('players_scored', len(player_impacts))
        self.logger.info(f'PlayerImpactAgent: computed impact for {len(player_impacts)} players')

        top_sorted = sorted(player_impacts, key=lambda p: p.impact_score, reverse=True)
        top_names = [p.player_name for p in top_sorted[:3]]
        self.memory_bank.append_entry({'type': 'player_impact', 'top_players': top_names})
        self.session_memory.set('player_impacts', [p.__dict__ for p in player_impacts])
        return player_impacts
