import pandas as pd
import argparse
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def setup_argparse():
    """
    Sets up command-line argument parsing.
    """
    parser = argparse.ArgumentParser(
        description="Parse and analyze log files for patterns and generate reports."
    )
    parser.add_argument(
        "logfile", type=str, help="Path to the log file to be analyzed."
    )
    parser.add_argument(
        "--output", type=str, default="report.csv", help="Path to save the analysis report (default: report.csv)."
    )
    parser.add_argument(
        "--pattern", type=str, default="", help="Optional string pattern to filter log entries."
    )
    return parser

def parse_log_file(file_path, pattern=""):
    """
    Parses the log file and filters lines based on the provided pattern.
    
    :param file_path: Path to the log file.
    :param pattern: Optional string pattern to filter log entries.
    :return: A DataFrame containing the parsed log entries.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Log file '{file_path}' does not exist.")

    try:
        with open(file_path, "r") as file:
            # Read log file into a list of lines
            lines = file.readlines()
        
        # Filter lines by pattern if provided
        if pattern:
            lines = [line for line in lines if pattern in line]

        # Convert lines to a DataFrame (example assumes space-separated logs)
        data = [line.strip().split() for line in lines]
        df = pd.DataFrame(data, columns=["Timestamp", "Level", "Message"])
        return df
    except Exception as e:
        logger.error(f"Error while parsing the log file: {e}")
        raise

def analyze_logs(df):
    """
    Analyzes the log DataFrame and generates basic statistics.
    
    :param df: DataFrame containing log data.
    :return: A summary DataFrame with analysis results.
    """
    try:
        summary = df["Level"].value_counts().reset_index()
        summary.columns = ["Log Level", "Count"]
        return summary
    except Exception as e:
        logger.error(f"Error while analyzing the logs: {e}")
        raise

def main():
    """
    Main function to handle log file parsing and analysis.
    """
    parser = setup_argparse()
    args = parser.parse_args()

    try:
        logger.info(f"Parsing log file: {args.logfile}")
        df = parse_log_file(args.logfile, args.pattern)

        logger.info("Analyzing logs...")
        summary = analyze_logs(df)

        logger.info(f"Saving analysis report to: {args.output}")
        summary.to_csv(args.output, index=False)

        logger.info("Analysis completed successfully.")
        print(f"Analysis report saved to: {args.output}")
    except FileNotFoundError as fnf_error:
        logger.error(f"File not found: {fnf_error}")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

# Usage Example:
# Run this script from the command line:
# python main.py /path/to/logfile.log --output output_report.csv --pattern ERROR

if __name__ == "__main__":
    main()