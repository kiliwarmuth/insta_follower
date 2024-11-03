"""Instagram follower analysis script"""

import sys
import argparse
import logging

# Configure logging at the top with the desired format
LOG_FORMAT = "\n[%(levelname)s] - %(asctime)s - %(message)s"
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, datefmt='%H:%M')


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
        logging.error("%s - %s\n", e, file_name)
        logging.error("Please make sure the two .txt files are in the same"
                      " folder as this script.")
        logging.error("Copy the Follow/Followers lists from the Instagram"
                      " Website.")
        logging.error("follow.txt -> accounts you follow")
        logging.error("followers.txt -> accounts following you")
        sys.exit(1)
    except IOError as err:
        logging.error("An I/O error occurred while reading the file: %s",
                      err)
        sys.exit(1)
    except UnicodeDecodeError as err:
        logging.error("A decoding error occurred while reading the file: %s",
                      err)
        sys.exit(1)


def get_username_list(lines):
    """
    Extract a list of usernames from a list of lines.

    Args:
        lines (list): List of lines from which to extract usernames.

    Returns:
        list: List of usernames.
    """
    skip_words = {"Entfernen", "Remove", "Suchen", "Search"}
    username_list = []
    next_is_username = False

    for i, line in enumerate(lines):
        line = line.strip()

        # Skip empty lines and irrelevant lines
        if line in skip_words:
            continue

        # Process possible empty first line
        if i == 0 and not line:
            next_is_username = True
            continue

        # Add username
        if next_is_username:
            next_is_username = False
            username_list.append(line)
            continue

        # If the line contains "Profilbild" or "profile picture",
        # the next line is a username
        if "Profilbild" in line or "profile picture" in line:
            next_is_username = True

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


def color_text(text, color):
    """
    Color the given text with the specified ANSI color code.

    Args:
        text (str): Text to color.
        color (str): ANSI color code.

    Returns:
        str: Colored text.
    """
    colors = {
        'green': '\033[92m',
        'cyan': '\033[96m',
        'yellow': '\033[93m',
        'red': '\033[91m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    return f"{colors.get(color, colors['white'])}{text}{colors['reset']}"


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
    print(f"{color_text(title, 'green')} "
          f"({color_text(len(user_list), 'cyan')}):")
    for user in user_list:
        print(f"  - {color_text(user, color)}")
    print("")


def parse_arguments():
    """
    Parse command-line arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Instagram Follow Analytics"
                                     " Script")
    parser.add_argument("--following_file", default="following.txt",
                        help="File containing accounts you follow ->"
                        " following.txt")
    parser.add_argument("--followers_file", default="followers.txt",
                        help="File containing accounts who follow you ->"
                        " followers.txt")
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Print followers and following lists")
    return parser.parse_args()


def main():
    """
    Main function to execute the Instagram follower analysis.

    This function reads the following and followers lists from provided files,
    analyzes the lists to identify users who don't follow back and those who
    are not followed back, and then prints the results with color-coded output.

    Command-line arguments are used to specify the input files and verbosity.
    """
    args = parse_arguments()

    follow_list = get_username_list(read_file(args.following_file))
    followers_list = get_username_list(read_file(args.followers_file))

    if follow_list is None or followers_list is None:
        logging.error("Please make sure the .txt files are not empty and in"
                      " the same folder as this script.")
        sys.exit(1)

    logging.info("Analyzing Your Social Media Presence...")

    # Compute non-followers and non-follows
    non_follows = find_non_follows(follow_list, followers_list)
    non_followers = find_non_followers(follow_list, followers_list)

    logging.info("Printing Summary Info...")
    logging.info("You follow %s accounts, and you have %s followers.",
                 color_text(len(follow_list), 'cyan'),
                 color_text(len(followers_list), 'cyan'))
    count_non_followers = len(non_followers)
    logging.info("%s account %s not following you back.",
                 color_text(count_non_followers, 'yellow'),
                 "is" if count_non_followers == 1 else "are")
    logging.info("You are not following back %s account(s).",
                 color_text(len(non_follows), 'red'))

    if args.verbose:
        print_colored_list("Accounts you follow:",
                           follow_list, 'blue')
        print_colored_list("Accounts following you:",
                           followers_list, 'magenta')

    # Print the results
    print_colored_list("\nAccounts you are not following back:",
                       non_follows, 'yellow')
    print_colored_list("Accounts not following you back:",
                       non_followers, 'red')


if __name__ == "__main__":
    main()
