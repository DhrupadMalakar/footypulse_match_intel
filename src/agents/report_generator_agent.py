from typing import List, Dict, Any
from src.observability.metrics import Metrics
from src.memory.memory_bank import MemoryBank
from src.memory.session_memory import SessionMemory
from src.models.domain_models import PlayerImpact, SentimentSummary
import logging
import os


class ReportGeneratorAgent:
    def __init__(
        self,
        logger: logging.Logger,
        metrics: Metrics,
        memory_bank: MemoryBank,
        session_memory: SessionMemory,
        output_path: str,
    ) -> None:
        self.logger = logger
        self.metrics = metrics
        self.memory_bank = memory_bank
        self.session_memory = session_memory
        self.output_path = output_path

    def run(
        self,
        comments_with_sentiment: List[Dict[str, Any]],
        sentiment_summary: SentimentSummary,
        player_impacts: List[PlayerImpact],
        match_summary: str,
    ) -> str:
        os.makedirs(os.path.dirname(self.output_path), exist_ok=True)

        lines: List[str] = []
        lines.append('# FootyPulse Match Intelligence Report\n')
        lines.append('## 1. High-level Summary\n')
        lines.append(match_summary + '\n')

        lines.append('## 2. Crowd Sentiment Overview\n')
        lines.append(
            f'- Positive: {sentiment_summary.positive}\n'
            f'- Negative: {sentiment_summary.negative}\n'
            f'- Neutral: {sentiment_summary.neutral}\n'
        )

        lines.append('## 3. Player Impact Scores\n')
        if player_impacts:
            lines.append('| Player | Team | Goals | Assists | Cards | Sentiment | Impact |\n')
            lines.append('|--------|------|-------|---------|-------|-----------|--------|\n')
            for p in player_impacts:
                lines.append(
                    f'| {p.player_name} | {p.team} | {p.goals} | {p.assists} | {p.cards} | '
                    f'{p.sentiment_score} | {p.impact_score} |\n'
                )
        else:
            lines.append('Player impact data not available.\n')

        lines.append('## 4. Sample Fan Comments\n')
        for c in comments_with_sentiment[:10]:
            author = c.get('author', 'unknown')
            sentiment = c.get('sentiment', 'unknown')
            text = c.get('text', '').replace('\n', ' ')
            lines.append(f'- **{author}** ({sentiment}): {text}\n')

        with open(self.output_path, 'w', encoding='utf-8') as f:
            f.writelines(lines)

        self.metrics.increment('reports_created', 1)
        self.logger.info(f'ReportGeneratorAgent: report written to {self.output_path}')
        self.memory_bank.append_entry({'type': 'report_created', 'path': self.output_path})
        self.session_memory.set('last_report_path', self.output_path)
        return self.output_path
