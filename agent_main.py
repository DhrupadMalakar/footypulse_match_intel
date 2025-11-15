import argparse  # Import argparse to handle command-line arguments
import os  # Import os to work with file paths and directories
from src.observability.logging_utils import init_logging  # Import function to set up logging
from src.observability.metrics import Metrics  # Import Metrics class for simple counters
from src.memory.memory_bank import MemoryBank  # Import MemoryBank for long-term JSON memory
from src.memory.session_memory import SessionMemory  # Import SessionMemory for in-run storage
from src.agents.reddit_data_agent import RedditDataAgent  # Import RedditDataAgent
from src.agents.sentiment_agent import SentimentAnalysisAgent  # Import SentimentAnalysisAgent
from src.agents.player_impact_agent import PlayerImpactAgent  # Import PlayerImpactAgent
from src.agents.match_summary_agent import MatchSummaryAgent  # Import MatchSummaryAgent
from src.agents.report_generator_agent import ReportGeneratorAgent  # Import ReportGeneratorAgent


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments."""  # Short docstring for this function
    parser = argparse.ArgumentParser(description="FootyPulse Match Intelligence Agent")  # Create argument parser
    parser.add_argument(  # Add a boolean flag for demo mode
        "--demo",
        action="store_true",
        help="Run in offline demo mode using sample data.",
    )
    return parser.parse_args()  # Return parsed arguments


def ensure_directories() -> None:
    """Ensure that required directories exist."""  # Describe purpose of this function
    for folder in ["logs", "outputs/reports", "memory_store", "metrics", "data"]:  # Iterate over needed folders
        os.makedirs(folder, exist_ok=True)  # Create folder if it does not exist already


def main() -> None:
    """Main orchestration for all agents."""  # Describe main function
    args = parse_args()  # Parse command-line arguments
    ensure_directories()  # Make sure folders exist
    logger = init_logging(log_file_path="logs/app.log")  # Set up logging and get a logger
    metrics = Metrics(metrics_path="metrics/counters.json")  # Create a Metrics object
    memory_bank = MemoryBank(memory_path="memory_store/long_term_memory.json")  # Create a MemoryBank
    session_memory = SessionMemory()  # Create in-memory session object

    logger.info("Starting FootyPulse pipeline")  # Log start message
    metrics.increment("runs")  # Increment runs counter in metrics

    # Set up agents with shared dependencies
    reddit_agent = RedditDataAgent(  # Create RedditDataAgent instance
        logger=logger,
        metrics=metrics,
        memory_bank=memory_bank,
        session_memory=session_memory,
        demo_mode=args.demo,
        sample_path="data/sample_reddit_thread.json",
    )
    sentiment_agent = SentimentAnalysisAgent(  # Create SentimentAnalysisAgent instance
        logger=logger,
        metrics=metrics,
        memory_bank=memory_bank,
        session_memory=session_memory,
    )
    player_impact_agent = PlayerImpactAgent(  # Create PlayerImpactAgent instance
        logger=logger,
        metrics=metrics,
        memory_bank=memory_bank,
        session_memory=session_memory,
        sample_stats_path="data/sample_match_stats.json",
        demo_mode=args.demo,
    )
    match_summary_agent = MatchSummaryAgent(  # Create MatchSummaryAgent instance
        logger=logger,
        metrics=metrics,
        memory_bank=memory_bank,
        session_memory=session_memory,
    )
    report_agent = ReportGeneratorAgent(  # Create ReportGeneratorAgent instance
        logger=logger,
        metrics=metrics,
        memory_bank=memory_bank,
        session_memory=session_memory,
        output_path="outputs/reports/demo_match_report.md",
    )

    # Run agents sequentially
    logger.info("Running Reddit Data Fetch Agent")  # Log stage
    comments = reddit_agent.run()  # Fetch comments (list of dicts)

    logger.info("Running Sentiment Analysis Agent")  # Log stage
    comments_with_sentiment, sentiment_summary = sentiment_agent.run(comments)  # Analyze sentiment

    logger.info("Running Player Impact Agent")  # Log stage
    player_impacts = player_impact_agent.run(comments_with_sentiment)  # Compute player impacts

    logger.info("Running Match Summary Agent")  # Log stage
    match_summary = match_summary_agent.run(  # Create narrative summary
        sentiment_summary=sentiment_summary,
        player_impacts=player_impacts,
    )

    logger.info("Running Report Generator Agent")  # Log stage
    report_path = report_agent.run(  # Generate report file
        comments_with_sentiment=comments_with_sentiment,
        sentiment_summary=sentiment_summary,
        player_impacts=player_impacts,
        match_summary=match_summary,
    )

    logger.info("FootyPulse pipeline completed")  # Log completion
    logger.info(f"Report generated at: {report_path}")  # Log where report was saved
    print(f"Report generated at: {report_path}")  # Also print to console for the user


if __name__ == "__main__":  # Run main only when this file is executed directly
    main()  # Call the main function
