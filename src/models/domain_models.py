from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class Comment:
    author: str
    text: str
    team: str
    sentiment: str = 'unknown'
    score: int = 0


@dataclass
class SentimentSummary:
    positive: int
    negative: int
    neutral: int


@dataclass
class PlayerImpact:
    player_name: str
    team: str
    goals: int
    assists: int
    cards: int
    sentiment_score: int
    impact_score: int


def map_comments_from_raw(raw_comments: List[Dict[str, Any]]) -> List[Comment]:
    mapped: List[Comment] = []
    for item in raw_comments:
        mapped.append(
            Comment(
                author=item.get('author', 'unknown'),
                text=item.get('text', ''),
                team=item.get('team', 'unknown'),
            )
        )
    return mapped
