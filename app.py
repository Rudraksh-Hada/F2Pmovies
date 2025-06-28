from flask import Flask, render_template, request, redirect, session, send_file, jsonify
import csv
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'


# ✅ Home & Web both serve web.html (must be outside templates!)
@app.route('/')
def home():
    return send_file('web.html')

@app.route('/web')
def web():
    return send_file('web.html')


# ✅ Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('nav-links/register.html')

    if request.is_json:
        data = request.get_json()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()
        password = data.get('password', '')
    else:
        username = request.form['username'].strip()
        email = request.form['email'].strip()
        password = request.form['password']
        confirm = request.form['confirm']
        if password != confirm:
            return "<h3>❌ Passwords do not match. <a href='/register'>Try again</a></h3>"

    file_exists = os.path.exists('users.csv')
    with open('users.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Username', 'Email', 'Password'])
        writer.writerow([username, email, password])

    return jsonify({"status": "success", "redirect": "/"}) if request.is_json else redirect('/')


# ✅ Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username'].strip()
        password = request.form['password'].strip()
        try:
            with open('users.csv', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['Username'] == username and row['Password'] == password:
                        session['user'] = username
                        return redirect('/web')
        except FileNotFoundError:
            pass
        return "<h3>❌ Invalid username or password. <a href='/login'>Try again</a></h3>"

    return render_template('nav-links/login.html')


# ✅ API to get username
@app.route('/api/username')
def get_username():
    return jsonify({'username': session['user']}) if 'user' in session else jsonify({'username': None})


# ✅ Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# ✅ Nav links
@app.route('/about us')
def about_us():
    return render_template('nav-links/about us.html')

@app.route('/contacts')
def contacts():
    return render_template('nav-links/contacts.html')

@app.route('/all')
def all():
    return render_template('category/all.html')


# ✅ Categories
@app.route('/movies')
def movies():
    return render_template('category/movies.html')

@app.route('/live-shows')
def live_shows():
    return render_template('category/live-shows.html')

@app.route('/tv-shows')
def tv_shows():
    return render_template('category/tv-shows.html')

@app.route('/anime')
def anime():
    return render_template('category/anime.html')

@app.route('/sports')
def sports():
    return render_template('category/sports.html')





names = [
    "nebula drift", "quantum shadows", "the last algorithm", "echoes of tomorrow",
    "starlight protocol", "phantom circuit", "shadowed whispers", "edge of silence",
    "lost in the wilds", "hearts unwritten", "laugh riot", "broken strings",
    "galactic drift", "mystic realms", "urban pursuit", "midnight evidence",
    "the vanished key", "homebound tales", "pixel dreams", "hidden truths",
    "beyond the veil", "campus diaries", "silent frontlines", "echoes of time",
    "rhythm street", "victory lane", "critical pulse", "justice bound",
    "power play", "crown & shadows", "covert signals", "dusty trails",
    "roommates united", "spectral files", "tales unfolded", "love & laughter",
    "mind maze", "growing pains", "summer olympics", "winter olympics",
    "fifa world cup", "uefa european championship", "cricket world cup",
    "rugby world cup", "icc t20 world cup", "african cup of nations",
    "asian games", "commonwealth games", "pan american games", "super bowl",
    "nba finals", "stanley cup finals", "world series", "indian premier league",
    "afc asian cup", "afl grand final", "olympic marathon", "boston marathon",
    "tour de france", "giro d'italia", "wimbledon", "us open (tennis)",
    "french open", "australian open", "the masters (golf)", "ryder cup",
    "formula one grand prix", "monaco grand prix", "24 hours of le mans",
    "boxing heavyweight championship", "aurora nights", "echoes of eden",
    "phantom encore", "velvet horizon", "sonic voyage", "stellar parade",
    "moonlit groove", "urban pulse", "galaxy jam", "echo chamber",
    "skyline sessions", "retro spectrum", "zenith fest", "solstice sound",
    "nebula nights", "limelight legends", "aurora pulse", "echo summit",
    "sonic bloom", "stellar stage", "phantom groove",
    "urban rhythm", "galaxy groove", "echo fest", "skyline groove",
    "retro nights", "zenith groove", "solstice jam", "nebula groove",
    "limelight jam", "aurora groove", "kaiba", "planet with", "houseki no kuni",
    "flip flappers", "kyousougiga", "haibane renmei", "texhnolyze", "ergo proxy",
    "mawaru penguindrum", "uchouten kazoku", "kemono no souja erin",
    "kanata no astra", "tsuritama", "kyoukai no kanata", "zarathustra",
    "akatsuki no yona", "aria the animation", "kareshi kanojo no jijou",
    "angel's egg", "serial experiments lain", "mononoke", "dennou coil",
    "sonny boy", "kaiji", "planetes", "hoshi no samidare", "kaiketsu zorori",
    "space dandy", "giant killing", "kemurikusa", "akiba's trip",
    "kyoushoku soukou guyver", "shadowed dreams", "monsoon melody",
    "emerald city", "lotus in the mist", "saffron skies", "echoes of mumbai",
    "golden promise", "velvet dusk", "royal rendezvous", "whispering hearts",
    "urban raga", "crimson moon", "stellar horizon", "phantom protocol",
    "iron legacy", "echo valley", "quantum fate", "obsidian code",
    "last frontier", "blue inferno", "zero hour", "hidden spectrum",
    "thunder veeran", "maaya chitra", "diamond dynasty", "velvet vimanam",
    "teakwood tales", "lotus warrior", "echoes of chennai", "pearl horizon",
    "saffron saga", "monsoon mirage", "celestial harmony", "arcane blossom"
]

# Register 1 route for each
for name in names:
    route_path = f'/{name}'
    endpoint_name = name.replace(' ', '_').replace("'", "").replace('&', 'and')
    template_path = f'download/{name}.html'

    def make_view(template_path):
        def view():
            return render_template(template_path)
        return view

    app.add_url_rule(route_path, endpoint_name, make_view(template_path))

@app.route('/api/search')
def api_search():
    query = request.args.get('query', '').lower().strip()
    matches = []

    if query:
        for name in names:
            if query in name.lower():
                matches.append({
                    'title': name.title(),      # Capitalize nicely
                    'url': f'/{name}'           # Direct link to your dynamic route
                })

    return jsonify(matches)



if __name__ == '__main__':
    app.run(debug=True)
