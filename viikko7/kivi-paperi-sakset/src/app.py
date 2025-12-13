from flask import Flask, render_template, request, session, redirect, url_for
from luo_peli import luo_peli
from tuomari import Tuomari
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

# Store game state in session


def get_or_create_game():
    if 'game_type' not in session:
        return None

    if 'tuomari' not in session:
        session['tuomari'] = {
            'ekan_pisteet': 0,
            'tokan_pisteet': 0,
            'tasapelit': 0
        }

    return session['game_type']


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/new_game', methods=['POST'])
def new_game():
    game_type = request.form.get('game_type')
    session['game_type'] = game_type
    session['tuomari'] = {
        'ekan_pisteet': 0,
        'tokan_pisteet': 0,
        'tasapelit': 0
    }
    session['game_history'] = []
    # Initialize AI state
    if game_type == 'b':
        session['ai_state'] = {'siirto': 0}
    elif game_type == 'c':
        session['ai_state'] = {'muisti': [],
                               'vapaa_muisti_indeksi': 0, 'muistin_koko': 10}
    return redirect(url_for('play'))


@app.route('/play')
def play():
    game_type = get_or_create_game()
    if game_type is None:
        return redirect(url_for('index'))

    game_type_names = {
        'a': 'Pelaaja vastaan Pelaaja',
        'b': 'Pelaaja vastaan Tekoäly',
        'c': 'Pelaaja vastaan Parannettu Tekoäly'
    }

    tuomari_data = session.get('tuomari', {})
    history = session.get('game_history', [])

    return render_template('play.html',
                           game_type=game_type,
                           game_type_name=game_type_names.get(game_type, ''),
                           tuomari=tuomari_data,
                           history=history)


@app.route('/make_move', methods=['POST'])
def make_move():
    game_type = get_or_create_game()
    if game_type is None:
        return redirect(url_for('index'))

    player1_move = request.form.get('player1_move')

    if not player1_move or player1_move not in ['k', 'p', 's']:
        return redirect(url_for('play'))

    # Get AI move for game types b and c
    if game_type == 'b':
        # Simple AI - cycles through moves
        ai_state = session.get('ai_state', {'siirto': 0})
        siirto = ai_state['siirto']
        siirto = (siirto + 1) % 3
        ai_state['siirto'] = siirto
        session['ai_state'] = ai_state

        if siirto == 0:
            player2_move = "k"
        elif siirto == 1:
            player2_move = "p"
        else:
            player2_move = "s"
    elif game_type == 'c':
        # Enhanced AI - remembers player moves
        ai_state = session.get(
            'ai_state', {'muisti': [], 'vapaa_muisti_indeksi': 0, 'muistin_koko': 10})
        muisti = ai_state['muisti']
        vapaa_muisti_indeksi = ai_state['vapaa_muisti_indeksi']
        muistin_koko = ai_state['muistin_koko']

        # Calculate AI move based on memory
        if vapaa_muisti_indeksi == 0 or vapaa_muisti_indeksi == 1:
            player2_move = "k"
        else:
            viimeisin_siirto = muisti[vapaa_muisti_indeksi - 1]
            k = 0
            p = 0
            s = 0

            for i in range(0, vapaa_muisti_indeksi - 1):
                if viimeisin_siirto == muisti[i]:
                    seuraava = muisti[i + 1]
                    if seuraava == "k":
                        k = k + 1
                    elif seuraava == "p":
                        p = p + 1
                    else:
                        s = s + 1

            if k > p or k > s:
                player2_move = "p"
            elif p > k or p > s:
                player2_move = "s"
            else:
                player2_move = "k"

        # Store player move in memory
        if vapaa_muisti_indeksi == muistin_koko:
            muisti = muisti[1:] + [player1_move]
            vapaa_muisti_indeksi = vapaa_muisti_indeksi - 1
        else:
            muisti.append(player1_move)

        vapaa_muisti_indeksi = vapaa_muisti_indeksi + 1
        ai_state['muisti'] = muisti
        ai_state['vapaa_muisti_indeksi'] = vapaa_muisti_indeksi
        session['ai_state'] = ai_state
    else:
        # Player vs Player
        player2_move = request.form.get('player2_move')
        if not player2_move or player2_move not in ['k', 'p', 's']:
            return redirect(url_for('play'))

    # Update tuomari
    tuomari = Tuomari()
    tuomari.ekan_pisteet = session['tuomari']['ekan_pisteet']
    tuomari.tokan_pisteet = session['tuomari']['tokan_pisteet']
    tuomari.tasapelit = session['tuomari']['tasapelit']

    tuomari.kirjaa_siirto(player1_move, player2_move)

    session['tuomari'] = {
        'ekan_pisteet': tuomari.ekan_pisteet,
        'tokan_pisteet': tuomari.tokan_pisteet,
        'tasapelit': tuomari.tasapelit
    }

    # Add to history
    move_names = {'k': 'Kivi', 'p': 'Paperi', 's': 'Sakset'}
    if 'game_history' not in session:
        session['game_history'] = []

    history = session['game_history']
    history.append({
        'player1': move_names[player1_move],
        'player2': move_names[player2_move],
        'player1_raw': player1_move,
        'player2_raw': player2_move
    })
    session['game_history'] = history
    session.modified = True

    return redirect(url_for('play'))


@app.route('/reset')
def reset():
    session.clear()
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True, port=5000)
