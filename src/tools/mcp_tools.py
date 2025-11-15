from typing import Dict, Any, List


def get_mcp_tools() -> List[Dict[str, Any]]:
    reddit_fetch_tool = {
        'name': 'reddit_fetch',
        'description': 'Fetch Reddit-style comments from a local file or URL.',
        'input_schema': {
            'type': 'object',
            'properties': {
                'source': {'type': 'string', 'description': 'Either file or url'},
                'path': {'type': 'string', 'description': 'File path or URL'},
            },
            'required': ['source', 'path'],
        },
    }
    return [reddit_fetch_tool]
