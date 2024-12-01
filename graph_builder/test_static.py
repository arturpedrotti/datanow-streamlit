@app.route('/test_static')
def test_static():
    return '''
    <h1>Testing Static Assets</h1>
    <img src="{}" alt="Logo">
    <img src="{}" alt="Footer Logo">
    '''.format(
        url_for('static', filename='shared_assets/shared_images/pic01.jpg'),
        url_for('static', filename='shared_assets/shared_images/pic03.jpg')
    )

