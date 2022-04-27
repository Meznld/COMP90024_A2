from flask import Flask, render_template
import folium

app = Flask(__name__)

@app.route('/')
def index():
    map = folium.Map(
        location=[-37.840935,144.946457]
    )
    
    folium.Marker(
        location=[-37.823364,144.95633],
        popup="<b>100</b>",
        tooltip="South Bank"
    ).add_to(map)
    folium.Marker(
        location=[-37.81794,145.12369],
        popup="<b>80</b>",
        tooltip="Box Hill"
    ).add_to(map)

    folium.Marker(
        location=[-38.148991411100134, 144.35844532757642],
        popup="<b>50</b>",
        tooltip="Geelong"
    ).add_to(map)

    folium.Marker(
        location=[-37.912430478752995, 144.9905811928703],
        popup="<b>50</b>",
        tooltip="Brighton"
    ).add_to(map)
    
    map.save('templates/map.html')
    return render_template('Page1.html')

@app.route('/map')
def map():
    return render_template('map.html')

@app.route('/features')
def features():
    return render_template('Page2.html')

if __name__ == '__main__':
    app.run(debug=True)