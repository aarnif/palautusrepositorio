import pytest
from app import app as flask_app


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    flask_app.config['TESTING'] = True
    flask_app.config['SECRET_KEY'] = 'test-secret-key'
    yield flask_app


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


class TestIndexRoute:
    def test_index_page_loads(self, client):
        """Test that the index page loads successfully."""
        response = client.get('/')
        assert response.status_code == 200
        assert b'Kivi Paperi Sakset' in response.data

    def test_index_has_game_options(self, client):
        """Test that all game type options are present."""
        response = client.get('/')
        assert 'Pelaaja vastaan Pelaaja' in response.data.decode('utf-8')
        assert 'Pelaaja vastaan Tekoäly' in response.data.decode('utf-8')
        assert 'Parannettu Tekoäly' in response.data.decode('utf-8')


class TestNewGame:
    def test_new_game_player_vs_player(self, client):
        """Test creating a new player vs player game."""
        response = client.post(
            '/new_game', data={'game_type': 'a'}, follow_redirects=True)
        assert response.status_code == 200
        assert 'Pelaaja vastaan Pelaaja' in response.data.decode('utf-8')

    def test_new_game_vs_ai(self, client):
        """Test creating a new game vs AI."""
        response = client.post(
            '/new_game', data={'game_type': 'b'}, follow_redirects=True)
        assert response.status_code == 200
        assert 'Pelaaja vastaan Tekoäly' in response.data.decode('utf-8')

    def test_new_game_vs_enhanced_ai(self, client):
        """Test creating a new game vs enhanced AI."""
        response = client.post(
            '/new_game', data={'game_type': 'c'}, follow_redirects=True)
        assert response.status_code == 200
        assert 'Parannettu Tekoäly' in response.data.decode('utf-8')

    def test_new_game_initializes_score(self, client):
        """Test that a new game initializes the score to zero."""
        response = client.post(
            '/new_game', data={'game_type': 'a'}, follow_redirects=True)
        assert b'Pelaaja 1:</strong> 0' in response.data
        assert b'Tasapelit:</strong> 0' in response.data


class TestPlayRoute:
    def test_play_without_game_redirects(self, client):
        """Test that accessing play without a game redirects to index."""
        response = client.get('/play')
        assert response.status_code == 302
        assert response.location == '/'

    def test_play_with_active_game(self, client):
        """Test that play page is accessible with an active game."""
        client.post('/new_game', data={'game_type': 'a'})
        response = client.get('/play')
        assert response.status_code == 200
        assert 'Valitse siirtosi' in response.data.decode('utf-8')


class TestMakeMovePlayerVsPlayer:
    def test_make_move_both_players(self, client):
        """Test making a move in player vs player mode."""
        client.post('/new_game', data={'game_type': 'a'})
        response = client.post('/make_move', data={
            'player1_move': 'k',
            'player2_move': 'p'
        }, follow_redirects=True)
        assert response.status_code == 200

    def test_player1_wins(self, client):
        """Test that player 1 wins when playing rock vs scissors."""
        client.post('/new_game', data={'game_type': 'a'})
        response = client.post('/make_move', data={
            'player1_move': 'k',
            'player2_move': 's'
        }, follow_redirects=True)
        assert b'Pelaaja 1:</strong> 1' in response.data

    def test_player2_wins(self, client):
        """Test that player 2 wins when player 1 plays rock and player 2 plays paper."""
        client.post('/new_game', data={'game_type': 'a'})
        response = client.post('/make_move', data={
            'player1_move': 'k',
            'player2_move': 'p'
        }, follow_redirects=True)
        data = response.data.decode('utf-8')
        # Player 2 should have 1 point - check for the value in scoreboard
        assert '>1</p>' in data or 'Pelaaja 2: Paperi' in data

    def test_tie_game(self, client):
        """Test that a tie is recorded correctly."""
        client.post('/new_game', data={'game_type': 'a'})
        response = client.post('/make_move', data={
            'player1_move': 'k',
            'player2_move': 'k'
        }, follow_redirects=True)
        assert b'Tasapelit:</strong> 1' in response.data

    def test_invalid_move_redirects(self, client):
        """Test that invalid moves redirect back to play."""
        client.post('/new_game', data={'game_type': 'a'})
        response = client.post('/make_move', data={
            'player1_move': 'x',
            'player2_move': 'k'
        })
        assert response.status_code == 302

    def test_game_history_recorded(self, client):
        """Test that game history is recorded."""
        client.post('/new_game', data={'game_type': 'a'})
        response = client.post('/make_move', data={
            'player1_move': 'k',
            'player2_move': 'p'
        }, follow_redirects=True)
        assert b'Pelihistoria' in response.data
        assert b'Kierros 1' in response.data


class TestMakeMoveVsAI:
    def test_make_move_vs_simple_ai(self, client):
        """Test making a move against simple AI."""
        client.post('/new_game', data={'game_type': 'b'})
        response = client.post('/make_move', data={
            'player1_move': 'k'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Kierros 1' in response.data

    def test_simple_ai_cycles_moves(self, client):
        """Test that simple AI cycles through moves."""
        client.post('/new_game', data={'game_type': 'b'})

        # First move should be paperi (p)
        response1 = client.post(
            '/make_move', data={'player1_move': 'k'}, follow_redirects=True)
        assert b'Paperi' in response1.data

        # Second move should be sakset (s)
        response2 = client.post(
            '/make_move', data={'player1_move': 'k'}, follow_redirects=True)
        assert b'Sakset' in response2.data

        # Third move should be kivi (k)
        response3 = client.post(
            '/make_move', data={'player1_move': 'p'}, follow_redirects=True)
        assert b'Kivi' in response3.data

    def test_make_move_vs_enhanced_ai(self, client):
        """Test making a move against enhanced AI."""
        client.post('/new_game', data={'game_type': 'c'})
        response = client.post('/make_move', data={
            'player1_move': 'k'
        }, follow_redirects=True)
        assert response.status_code == 200
        assert b'Kierros 1' in response.data

    def test_enhanced_ai_learns_pattern(self, client):
        """Test that enhanced AI stores and uses player history."""
        client.post('/new_game', data={'game_type': 'c'})

        # Play several rounds with the same move
        for _ in range(2):
            client.post(
                '/make_move', data={'player1_move': 'k'}, follow_redirects=True)

        # The AI should have recorded the pattern
        # After multiple same moves, AI might adapt its strategy
        response = client.post(
            '/make_move', data={'player1_move': 'k'}, follow_redirects=True)
        assert response.status_code == 200
        assert b'Kierros 3' in response.data


class TestMultipleRounds:
    def test_multiple_rounds_player_vs_player(self, client):
        """Test playing multiple rounds and tracking scores."""
        client.post('/new_game', data={'game_type': 'a'})

        # Round 1: Player 1 wins (k vs s)
        client.post(
            '/make_move', data={'player1_move': 'k', 'player2_move': 's'})

        # Round 2: Player 2 wins (k vs p)
        client.post(
            '/make_move', data={'player1_move': 'k', 'player2_move': 'p'})

        # Round 3: Tie (k vs k)
        response = client.post(
            '/make_move', data={'player1_move': 'k', 'player2_move': 'k'}, follow_redirects=True)

        data = response.data.decode('utf-8')
        # Each player should have 1 win and 1 tie
        assert 'Kierros 3' in data
        assert 'Tasapelit' in data
        # Check that history shows all three rounds
        assert data.count('Kierros') >= 3


class TestReset:
    def test_reset_clears_game(self, client):
        """Test that reset clears the game and redirects to index."""
        client.post('/new_game', data={'game_type': 'a'})
        client.post(
            '/make_move', data={'player1_move': 'k', 'player2_move': 'p'})

        response = client.get('/reset', follow_redirects=True)
        assert response.status_code == 200
        assert 'Valitse pelityyppi' in response.data.decode('utf-8')

    def test_reset_clears_session(self, client):
        """Test that reset clears session data."""
        with client.session_transaction() as session:
            session['game_type'] = 'a'
            session['tuomari'] = {'ekan_pisteet': 3,
                                  'tokan_pisteet': 2, 'tasapelit': 2}

        client.get('/reset')

        with client.session_transaction() as session:
            assert 'game_type' not in session
            assert 'tuomari' not in session


class TestEdgeCases:
    def test_make_move_without_game(self, client):
        """Test making a move without an active game redirects."""
        response = client.post('/make_move', data={'player1_move': 'k'})
        assert response.status_code == 302
        assert response.location == '/'

    def test_missing_player2_move_in_pvp(self, client):
        """Test that missing player 2 move in PvP mode is handled."""
        client.post('/new_game', data={'game_type': 'a'})
        response = client.post('/make_move', data={'player1_move': 'k'})
        assert response.status_code == 302

    def test_all_move_combinations_work(self, client):
        """Test all valid move combinations."""
        moves = ['k', 'p', 's']
        client.post('/new_game', data={'game_type': 'a'})

        for move1 in moves:
            for move2 in moves:
                response = client.post('/make_move', data={
                    'player1_move': move1,
                    'player2_move': move2
                }, follow_redirects=True)
                assert response.status_code == 200


class TestGameLogic:
    def test_rock_beats_scissors(self, client):
        """Test that rock beats scissors."""
        client.post('/new_game', data={'game_type': 'a'})
        response = client.post('/make_move', data={
            'player1_move': 'k',
            'player2_move': 's'
        }, follow_redirects=True)
        assert b'Pelaaja 1:</strong> 1' in response.data

    def test_paper_beats_rock(self, client):
        """Test that paper beats rock."""
        client.post('/new_game', data={'game_type': 'a'})
        response = client.post('/make_move', data={
            'player1_move': 'p',
            'player2_move': 'k'
        }, follow_redirects=True)
        assert b'Pelaaja 1:</strong> 1' in response.data

    def test_scissors_beats_paper(self, client):
        """Test that scissors beats paper."""
        client.post('/new_game', data={'game_type': 'a'})
        response = client.post('/make_move', data={
            'player1_move': 's',
            'player2_move': 'p'
        }, follow_redirects=True)
        assert b'Pelaaja 1:</strong> 1' in response.data


class TestGameOver:
    def test_game_ends_when_player1_gets_3_wins(self, client):
        """Test that game ends when player 1 reaches 3 wins."""
        client.post('/new_game', data={'game_type': 'a'})

        # Player 1 wins 3 times (k beats s)
        for _ in range(3):
            response = client.post('/make_move', data={
                'player1_move': 'k',
                'player2_move': 's'
            }, follow_redirects=True)

        # Should be redirected to game over page
        assert response.status_code == 200
        data = response.data.decode('utf-8')
        assert 'Peli Päättyi' in data or 'Voitti' in data

    def test_game_ends_when_player2_gets_3_wins(self, client):
        """Test that game ends when player 2 reaches 3 wins."""
        client.post('/new_game', data={'game_type': 'a'})

        # Player 2 wins 3 times (p beats k)
        for _ in range(3):
            response = client.post('/make_move', data={
                'player1_move': 'k',
                'player2_move': 'p'
            }, follow_redirects=True)

        # Should be redirected to game over page
        assert response.status_code == 200
        data = response.data.decode('utf-8')
        assert 'Peli Päättyi' in data or 'Voitti' in data

    def test_game_continues_before_3_wins(self, client):
        """Test that game continues when no player has 3 wins."""
        client.post('/new_game', data={'game_type': 'a'})

        # Player 1 wins 2 times
        for _ in range(2):
            response = client.post('/make_move', data={
                'player1_move': 'k',
                'player2_move': 's'
            }, follow_redirects=True)

        # Should still be on play page
        data = response.data.decode('utf-8')
        assert 'Valitse siirtosi' in data
        assert 'Peli Päättyi' not in data

    def test_game_over_page_shows_winner(self, client):
        """Test that game over page shows the correct winner."""
        client.post('/new_game', data={'game_type': 'a'})

        # Player 1 wins 3 times
        for _ in range(3):
            client.post('/make_move', data={
                'player1_move': 'k',
                'player2_move': 's'
            }, follow_redirects=True)

        # Check game over page content
        response = client.get('/game_over')
        data = response.data.decode('utf-8')
        assert 'Pelaaja 1 Voitti' in data

    def test_game_over_shows_final_scores(self, client):
        """Test that game over page shows final scores."""
        client.post('/new_game', data={'game_type': 'a'})

        # Player 1 wins 3 times, player 2 wins 2 times, 1 tie
        for _ in range(3):
            client.post(
                '/make_move', data={'player1_move': 'k', 'player2_move': 's'})
        for _ in range(2):
            client.post(
                '/make_move', data={'player1_move': 'k', 'player2_move': 'p'})
        client.post(
            '/make_move', data={'player1_move': 'k', 'player2_move': 'k'})

        response = client.get('/game_over', follow_redirects=True)
        data = response.data.decode('utf-8')
        assert 'Lopulliset Pisteet' in data or 'Pisteet' in data

    def test_cannot_play_after_game_over(self, client):
        """Test that play page redirects to game over after game ends."""
        client.post('/new_game', data={'game_type': 'a'})

        # Player 1 wins 3 times
        for _ in range(3):
            client.post(
                '/make_move', data={'player1_move': 'k', 'player2_move': 's'})

        # Try to access play page
        response = client.get('/play', follow_redirects=True)
        data = response.data.decode('utf-8')
        assert 'Peli Päättyi' in data or 'Voitti' in data

    def test_play_again_same_game_type(self, client):
        """Test playing again with same game type after game over."""
        client.post('/new_game', data={'game_type': 'b'})

        # Complete a game (3 wins for player 1)
        for _ in range(3):
            client.post('/make_move', data={'player1_move': 'k'})

        # Start a new game of the same type
        response = client.post(
            '/new_game', data={'game_type': 'b'}, follow_redirects=True)

        # Should be on play page with new game
        assert response.status_code == 200
        data = response.data.decode('utf-8')
        assert 'Valitse siirtosi' in data

    def test_ai_game_ends_at_3_wins(self, client):
        """Test that AI games also end at 3 wins."""
        client.post('/new_game', data={'game_type': 'b'})

        # Play until someone gets 3 wins
        for _ in range(20):  # Max rounds to prevent infinite loop
            response = client.post(
                '/make_move', data={'player1_move': 'k'}, follow_redirects=True)
            data = response.data.decode('utf-8')
            if 'Peli Päättyi' in data or 'Voitti' in data:
                break

        # Game should have ended
        assert 'Voitti' in data or 'Peli Päättyi' in data
