import requests
from pywebio import start_server
from pywebio.output import put_html, put_button, put_loading
from pywebio.session import run_js

# API URL for fetching random facts
FACTS_API_URL = "https://uselessfacts.jsph.pl/random.json?language=en"

# Global variables for tracking the number of generated facts and likes
fact_count = 0
liked = False

def fetch_random_fact():
    """
    Fetches a random fact from the API.

    Returns:
        str: The text of the random fact, or an error message if the request fails.
    """
    try:
        response = requests.get(FACTS_API_URL)
        if response.status_code == 200:
            data = response.json()
            return data.get('text', 'No fact found!')
        else:
            return f"Error: Received status code {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

def fun_fact_app():
    """
    Fun Fact Web App

    This function sets up the web page with a header, introductory text, and buttons
    to generate a fun fact, toggle dark mode, refresh the page, and like/unlike the fact.
    """
    global fact_count, liked

    # Adding a simple header
    put_html("<h2> Welcome to the Fun Fact Generator! 🎉</h2>")

    # Displaying an introductory text
    put_html("<p>Click the button below to generate a fun fact and learn something new! 🤓</p>")

    # Function to handle fact generation
    def generate_fact():
        """
        Generates a new fun fact and displays it on the page.

        This function increments the fact count, fetches a new fact, plays a sound,
        and displays the fact on the page.
        """
        global fact_count
        fact_count += 1  # Increment fact count
        global liked
        liked = False  # Reset liked status when a new fact is generated
        with put_loading():  # Display a loading spinner
            fact = fetch_random_fact()  # Fetch fact

        # Display the fact
        put_html(f"""
            <p id='fact-text' style='font-size:30px; color:green;'>
                <strong>Fun Fact #{fact_count}:</strong> {fact}
            </p>
        """)
        put_html("""
            <div id="like-section" style="margin: 20px 0;">
                <button id='like-button' onclick="toggle_like()" style='font-size:24px; padding:8px 16px; margin:5px; background:#4CAF50; color:white; border:none; cursor:pointer;'>👍 Like</button>
                <button id='unlike-button' onclick="toggle_like()" style='font-size:24px; padding:8px 16px; margin:5px; background:#f44336; color:white; border:none; cursor:pointer;'>👎 Unlike</button>
            </div>
        """)
        update_like_button()

    # JavaScript functions for dark mode and like/unlike
    js_code = """
    function toggle_mode() {
        var currentMode = document.body.getAttribute('data-mode');
        if (currentMode === 'dark') {
            document.body.style.backgroundColor = '#f4f4f9';
            document.body.style.color = '#333';
            document.body.setAttribute('data-mode', 'light');
            document.getElementById('mode-toggle').innerHTML = '<i class="fas fa-moon"></i>';
            document.getElementById('mode-toggle').style.color = '#333';  // Dark mode text color
        } else {
            document.body.style.backgroundColor = '#333';
            document.body.style.color = '#fff';
            document.body.setAttribute('data-mode', 'dark');
            document.getElementById('mode-toggle').innerHTML = '<i class="fas fa-sun"></i>';
            document.getElementById('mode-toggle').style.color = '#FFD700';  // Yellow color for sun icon
        }
    }

    function toggle_like() {
        var likeButton = document.getElementById('like-button');
        var unlikeButton = document.getElementById('unlike-button');
        if (likeButton.style.backgroundColor === 'rgb(76, 175, 80)') {
            likeButton.style.backgroundColor = '#a5d6a7';
            unlikeButton.style.backgroundColor = '#f44336';
            likeButton.innerHTML = '👍 Like';
            unlikeButton.innerHTML = '👎 Unlike';
            document.getElementById('like-status').innerHTML = 'You liked this fact!';
        } else {
            likeButton.style.backgroundColor = '#4CAF50';
            unlikeButton.style.backgroundColor = '#a5d6a7';
            likeButton.innerHTML = '👍 Like';
            unlikeButton.innerHTML = '👎 Unlike';
            document.getElementById('like-status').innerHTML = 'You disliked this fact!';
        }
    }
    """

    # Initial mode setup
    run_js("document.body.setAttribute('data-mode', 'light');")

    # Add Font Awesome for icons
    put_html("""
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    """)

    # Add Dark/Light Mode toggle button with Font Awesome icons
    put_html(f"""
        <button id='mode-toggle' onclick="toggle_mode()" style='font-size:24px; padding:8px 16px; margin:10px; position:absolute; top:10px; right:10px; background:none; border:none; cursor:pointer; color:#333;'>
            <i class="fas fa-moon"></i>
        </button>
        <script>{js_code}</script>
    """)

    # Display button to generate fact
    put_button("🔄 Generate Fun Fact", onclick=generate_fact, color='success', outline=True)

    # Optional: Add a button to refresh the page with a JavaScript command
    put_button("🔁 Refresh Page", onclick=lambda: run_js('window.location.reload()'), color='warning', outline=True)

    # Add the status for like/unlike
    put_html("<p id='like-status'></p>")

def update_like_button():
    """
    Updates the like and unlike buttons based on the current liked status.
    """
    global liked
    if liked:
        run_js("document.getElementById('like-button').style.backgroundColor = '#a5d6a7';")
        run_js("document.getElementById('unlike-button').style.backgroundColor = '#f44336';")
        run_js("document.getElementById('like-button').innerHTML = '👍 Liked';")
        run_js("document.getElementById('unlike-button').innerHTML = '👎 Unlike';")
    else:
        run_js("document.getElementById('like-button').style.backgroundColor = '#4CAF50';")
        run_js("document.getElementById('unlike-button').style.backgroundColor = '#a5d6a7';")
        run_js("document.getElementById('like-button').innerHTML = '👍 Like';")
        run_js("document.getElementById('unlike-button').innerHTML = '👎 Dislike';")

if __name__ == '__main__':
    start_server(fun_fact_app, port=8080)
