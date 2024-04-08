import sys
import argparse
import logging
import time

try:
    from termcolor import colored
    TERM_COLOR_AVAILABLE = True
except ImportError:
    TERM_COLOR_AVAILABLE = False

def setup_logging():
    """
    Set up logging configuration.

    Returns:
        logger (Logger): Configured logger object.
    """
    log_format = "%(message)s"
    logging.basicConfig(level=logging.INFO, format=log_format)
    return logging.getLogger(__name__)

def read_file(file_name):
    """
    Read the content of a file.

    Args:
        file_name (str): The name of the file to read.

    Returns:
        list or None: A list of lines if the file exists, else None.
    """
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            return file.readlines()
    except FileNotFoundError as e:
        logger.error(f"File not found: {file_name}\n")
        logger.error("Please make sure the two .txt files are in the same folder as this script.")
        logger.error("Copy the Follow/Followers lists from the Instagram Website.")
        logger.error("follow.txt -> people you follow")
        logger.error("followers.txt -> people following you")
        sys.exit(1)
    except Exception as e:
        logger.error(f"An error occurred while reading the file: {e}")
        sys.exit(1)

def get_username_list(lines):
    """
    Extract a list of usernames from a list of lines.

    Args:
        lines (list): List of lines from which to extract usernames.

    Returns:
        list: List of usernames.
    """
    username_list = []
    profilbild_flag = False

    for i, line in enumerate(lines):
        line = line.strip()

        # Skip the line if it contains "Suchen" and it's the first line
        if i == 0 and "Suchen" in line:
            continue

        if "Profilbild" in line:
            profilbild_flag = True
        elif profilbild_flag:
            username_list.append(line)
            profilbild_flag = False

        # Check if the first line doesn't contain "Profilbild" and add the next line to username_list
        if i == 0 and "Profilbild" not in line:
            username_list.append(line)

    return username_list


def find_non_followers(follow_list, followers_list):
    """
    Find users in the follow list who are not in the followers list.

    Args:
        follow_list (list): List of users being followed.
        followers_list (list): List of users who follow back.

    Returns:
        list: Users in the follow list not in the followers list.
    """
    return [user for user in follow_list if user not in followers_list]

def find_non_follows(follow_list, followers_list):
    """
    Find users in the followers list who are not in the follow list.

    Args:
        follow_list (list): List of users being followed.
        followers_list (list): List of users who follow back.

    Returns:
        list: Users in the followers list not in the follow list.
    """
    return [user for user in followers_list if user not in follow_list]

def print_colored_list(title, user_list, color='white'):
    """
    Print a colored list.

    Args:
        title (str): Title for the list.
        user_list (list): List of items to print.
        color (str): Color for the items.

    Returns:
        None
    """
    logger.info(f"{colored(title, 'green')} ({colored(len(user_list), 'cyan')}):")
    for user in user_list:
        logger.info(f"  - {colored(user, color)}")
    logger.info("")

def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Instagram Follow Analytics Script")
    parser.add_argument("follow_file", help="File containing people you follow -> follow.txt")
    parser.add_argument("followers_file", help="File containing people who follow you -> follower.txt")
    parser.add_argument("-v", "--verbose", action="store_true", help="Print followers and follow lists")
    return parser.parse_args()

def main():
    global logger
    logger = setup_logging()

    if not TERM_COLOR_AVAILABLE:
        logger.error("The 'termcolor' module is not installed. Please install it using 'pip install termcolor'")
        sys.exit(1)

    args = parse_arguments()
    
    follow_list = get_username_list(read_file(args.follow_file))
    followers_list = get_username_list(read_file(args.followers_file))

    if follow_list is None or followers_list is None:
        logger.error("Please make sure the .txt files are not empty and in the same folder as this script.")
        sys.exit(1)

    logger.info("Analyzing Your Social Media Presence...")
    logger.info(f"You follow {colored(len(follow_list), 'cyan')} people, and you have {colored(len(followers_list), 'cyan')} follower.")
    
    time.sleep(2)

    if args.verbose:
        print_colored_list("People you follow:", follow_list, 'blue')
        print_colored_list("People following you:", followers_list, 'magenta')

    # compute and print the results
    print_colored_list("People you are not following back:", find_non_follows(follow_list, followers_list), 'yellow')
    print_colored_list("People not following you back:", find_non_followers(follow_list, followers_list), 'red')

if __name__ == "__main__":
    main()
