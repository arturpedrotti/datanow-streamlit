from flask import Flask, render_template, redirect, url_for
import subprocess

app = Flask(__name__)

# Landing page route
@app.route('/')
def landing_page():
    return render_template('landing_page.html')

# Redirect to Data Insights sub-app
@app.route('/data_insights/')
def data_insights():
    # Start the Data Insights app if needed
    subprocess.Popen(['python', 'data_insights/app.py'], close_fds=True)
    return redirect("http://127.0.0.1:8050")

# Redirect to Graph Builder sub-app
@app.route('/graph_builder/')
def graph_builder():
    # Start the Graph Builder app if needed
    subprocess.Popen(['python', 'graph_builder/app.py'], close_fds=True)
    return redirect("http://127.0.0.1:8060")

if __name__ == '__main__':
    app.run(debug=True)
