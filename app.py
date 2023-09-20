import requests
import re

# Your webhook URL
webhook_url = "redacted"

def get_site_rank(url):
    response = requests.get(url)
    response.raise_for_status()  # Check for HTTP errors

    pattern = r"Site Rank: <a href='/globalRanking\.php\?s=\d+&t=\d+&o=(\d+)'>#([\d,]+)</a>"

    # Search for the pattern in the response text
    match = re.search(pattern, response.text)

    # Check if a match was found
    if match:
        # Extract the value next to the "#" symbol and remove commas
        rank_value = match.group(2).replace(',', '')
        return int(rank_value)  # Convert to an integer
    else:
        print("Pattern not found in the string.")
        return None

def save_last_rank(rank_value, filename="last_rank.txt"):
    with open(filename, "w") as file:
        file.write(str(rank_value))  # Write the rank as a string
        print(f"Rank value saved to {filename}")

def compare_ranks(current_rank):
    try:
        with open("last_rank.txt", "r") as file:
            last_rank = int(file.read())  # Read the last rank from the file as an integer

        if current_rank > last_rank:
            msg = f"Congratulations! Your rank has increased from {last_rank} to {current_rank}."
            rank_changed = True
        elif current_rank < last_rank:
            msg = f"Your rank has decreased from {last_rank} to {current_rank}. Keep up the good work!"
            rank_changed = True
        else:
            msg = f"Your rank remains the same at {current_rank}."
            rank_changed = False
        if rank_changed:
            send_webhook_message(msg)
            save_last_rank(current_rank)
    except FileNotFoundError:
        print("The 'last_rank' file does not exist. Saving current rank.")
    except ValueError:
        print("Error reading rank from the 'last_rank' file.")

def send_webhook_message(msg):
    try:
        response = requests.post(webhook_url, data={'content': msg})
        response.raise_for_status()  # Check for HTTP errors
        print("Webhook message sent successfully.")
    except requests.exceptions.RequestException as e:
        print("HTTP Request Error:", e)
    except Exception as e:
        print("Error sending webhook message:", e)

if __name__ == "__main__":
    url = "https://retroachievements.org/user/Lahey"
    
    try:
        current_rank = get_site_rank(url)
        
        if current_rank is not None:
            compare_ranks(current_rank)
    except requests.exceptions.RequestException as e:
        print("HTTP Request Error:", e)
    except Exception as e:
        print("Error:", e)
