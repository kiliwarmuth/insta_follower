# Instagram Follow Analytics Script

This script analyzes your Instagram follow and follower lists to provide insights into your social media presence. It identifies users you follow but who don't follow you back, as well as users who follow you but whom you don't follow back.

## Prerequisites

- Python 3.x
- `termcolor` module (install it using `pip install termcolor`)

## Usage

1. Clone this repository or download the script.

2. Navigate to your Instagram profile on the Instagram website.

3. Click on the "Followers" tab to view your followers or the "Following" tab to view the people you follow.

4. On the page displaying your followers or people you follow, select all entries by clicking and dragging your mouse to highlight them.

5. Once all entries are selected, right-click and choose "Copy" or use the keyboard shortcut (Ctrl+C on Windows or Command+C on macOS).

6. Paste the copied list into a text file named `followers.txt` for your followers or `follow.txt` for the people you follow.

7. Save the text file in the same directory as the script.

8. Run the script from the command line using the following format:


- `follow.txt`: File containing the usernames of people you follow.
- `followers.txt`: File containing the usernames of people who follow you.
- `-v` or `--verbose`: Optional flag to print the full follow and followers lists.

## Output

The script provides the following output:

- The total number of people you follow and the total number of followers you have.
- Lists of people you are not following back and people not following you back, each with colored highlighting for easy identification.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

