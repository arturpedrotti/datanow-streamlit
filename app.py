from flask import Flask, render_template, redirect, url_for
import subprocess
import socket

app = Flask(__name__)

# Function to dynamically get the local IP address
def get_local_ip():
    try:
        # Get the local IP address of the current machine
        return socket.gethostbyname(socket.gethostname())
    except Exception as e:
        print(f"Error getting local IP: {e}")
        return "127.0.0.1"

# Landing page route
@app.route('/')
def landing_page():
    """
    Render the main landing page.
    """
    return render_template('landing_page.html')

# Redirect to Data Insights sub-app
@app.route('/data_insights/')
def data_insights():
    """
    Start the Data Insights app if not already running
    and redirect to its URL.
    """
    subprocess.Popen(['python', 'data_insights/app.py'], close_fds=True)
    local_ip = get_local_ip()
    return redirect(f"http://{local_ip}:8050")

# Redirect to Graph Builder sub-app
@app.route('/graph_builder/')
def graph_builder():
    """
    Start the Graph Builder app if not already running
    and redirect to its URL.
    """
    subprocess.Popen(['python', 'graph_builder/app.py'], close_fds=True)
    local_ip = get_local_ip()
    return redirect(f"http://{local_ip}:8060")

if __name__ == '__main__':
    # Run the main Flask app on all interfaces and port 5000
    app.run(host="0.0.0.0", port=5000, debug=True)
