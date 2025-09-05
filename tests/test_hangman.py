import pytest
import time
from unittest.mock import patch, mock_open
from src.hangman import HangmanGame, GameLevel


class TestHangmanGame:
    def test_hangman_initialization_basic_level(self):
        game = HangmanGame(GameLevel.BASIC)
        assert game.level == GameLevel.BASIC
        assert game.max_lives == 6
        assert game.current_lives == 6
        assert game.time_limit == 15
        assert game.guessed_letters == set()
        assert game.game_over is False
        assert game.won is False

    def test_hangman_initialization_intermediate_level(self):
        game = HangmanGame(GameLevel.INTERMEDIATE)
        assert game.level == GameLevel.INTERMEDIATE
        assert game.max_lives == 6
        assert game.current_lives == 6

    @patch('builtins.open', mock_open(read_data='apple\norange\nbanana'))
    def test_load_words_basic_level(self):
        game = HangmanGame(GameLevel.BASIC)
        words = game._load_dictionary()
        assert 'apple' in words
        assert 'orange' in words
        assert 'banana' in words

    @patch('builtins.open', mock_open(read_data='hello world\nunit testing'))
    def test_load_phrases_intermediate_level(self):
        game = HangmanGame(GameLevel.INTERMEDIATE)
        phrases = game._load_dictionary()
        assert 'hello world' in phrases
        assert 'unit testing' in phrases

    def test_select_word_basic_level(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['apple', 'orange']):
            game = HangmanGame(GameLevel.BASIC)
            game._select_target()
            assert game.target_word in ['apple', 'orange']
            assert game.display_word == ['_'] * len(game.target_word)

    def test_select_phrase_intermediate_level(self):
        with patch.object(HangmanGame, '_load_dictionary',
                          return_value=['hello world', 'unit testing']):
            game = HangmanGame(GameLevel.INTERMEDIATE)
            game._select_target()
            assert game.target_word in ['hello world', 'unit testing']
            expected_display = []
            for char in game.target_word:
                expected_display.append('_' if char.isalpha() else char)
            assert game.display_word == expected_display

    def test_valid_guess_correct_letter(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['apple']):
            game = HangmanGame(GameLevel.BASIC)
            game._select_target()

            result = game.make_guess('a')
            assert result is True
            assert 'a' in game.guessed_letters
            assert game.display_word[0] == 'a'
            assert game.current_lives == 6

    def test_valid_guess_wrong_letter(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['apple']):
            game = HangmanGame(GameLevel.BASIC)
            game._select_target()

            result = game.make_guess('z')
            assert result is False
            assert 'z' in game.guessed_letters
            assert 'z' not in game.display_word
            assert game.current_lives == 5

    def test_invalid_guess_already_guessed(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['apple']):
            game = HangmanGame(GameLevel.BASIC)
            game._select_target()
            game.make_guess('a')

            with pytest.raises(ValueError, match="Letter 'a' has already been guessed"):
                game.make_guess('a')

    def test_invalid_guess_non_letter(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['apple']):
            game = HangmanGame(GameLevel.BASIC)
            game._select_target()

            with pytest.raises(ValueError, match="Please enter a single letter"):
                game.make_guess('123')

    def test_game_won_condition(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['cat']):
            game = HangmanGame(GameLevel.BASIC)
            game._select_target()

            game.make_guess('c')
            game.make_guess('a')
            game.make_guess('t')

            assert game.is_won() is True
            assert game.won is True

    def test_game_lost_condition(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['cat']):
            game = HangmanGame(GameLevel.BASIC)
            game._select_target()

            wrong_letters = ['x', 'y', 'z', 'w', 'v', 'u']
            for letter in wrong_letters:
                game.make_guess(letter)

            assert game.current_lives == 0
            assert game.is_game_over() is True
            assert game.won is False

    def test_timer_functionality(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['apple']):
            game = HangmanGame(GameLevel.BASIC)
            game._select_target()
            game.start_timer()

            time.sleep(0.1)
            remaining_time = game.get_remaining_time()
            assert remaining_time < 15
            assert remaining_time > 14.8

    def test_timer_expired(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['apple']):
            game = HangmanGame(GameLevel.BASIC)
            game._select_target()
            game.start_timer()

            with patch('time.time', return_value=game.start_time + 16):
                assert game.is_time_up() is True

    def test_get_display_string_basic(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['apple']):
            game = HangmanGame(GameLevel.BASIC)
            game._select_target()

            assert game.get_display_string() == "_ _ _ _ _"

            game.make_guess('a')
            assert game.get_display_string() == "a _ _ _ _"

    def test_get_display_string_intermediate_with_spaces(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['hello world']):
            game = HangmanGame(GameLevel.INTERMEDIATE)
            game._select_target()

            expected = "_ _ _ _ _   _ _ _ _ _"
            assert game.get_display_string() == expected

    def test_phrase_handling_spaces_preserved(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['hello world']):
            game = HangmanGame(GameLevel.INTERMEDIATE)
            game._select_target()

            game.make_guess('h')
            expected = "h _ _ _ _   _ _ _ _ _"
            assert game.get_display_string() == expected

    def test_get_hangman_drawing(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['apple']):
            game = HangmanGame(GameLevel.BASIC)
            game._select_target()

            assert "Lives remaining: 6" in game.get_hangman_drawing()

            game.make_guess('z')
            drawing = game.get_hangman_drawing()
            assert "Lives remaining: 5" in drawing
            assert "Wrong guesses: z" in drawing

    def test_reset_game(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['apple']):
            game = HangmanGame(GameLevel.BASIC)
            game._select_target()
            game.make_guess('z')

            game.reset_game()
            assert game.current_lives == 6
            assert game.guessed_letters == set()
            assert game.game_over is False
            assert game.won is False

    def test_file_not_found_fallback_basic(self):
        with patch('builtins.open', side_effect=FileNotFoundError):
            game = HangmanGame(GameLevel.BASIC)
            # Should use fallback words
            assert 'python' in game.dictionary
            assert 'programming' in game.dictionary

    def test_file_not_found_fallback_intermediate(self):
        with patch('builtins.open', side_effect=FileNotFoundError):
            game = HangmanGame(GameLevel.INTERMEDIATE)
            # Should use fallback phrases
            assert 'hello world' in game.dictionary
            assert 'unit testing' in game.dictionary

    def test_game_status_messages(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['cat']):
            game = HangmanGame(GameLevel.BASIC)
            game._select_target()
            game.start_timer()

            # Test winning status
            game.make_guess('c')
            game.make_guess('a')
            game.make_guess('t')
            status = game.get_game_status()
            assert "Congratulations" in status
            assert game.target_word in status

    def test_game_status_time_up(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['cat']):
            game = HangmanGame(GameLevel.BASIC)
            game._select_target()
            game.start_timer()

            # Mock time being up
            with patch('time.time', return_value=game.start_time + 16):
                status = game.get_game_status()
                assert "Time's up" in status
                assert game.target_word in status

    def test_game_status_game_over(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['cat']):
            game = HangmanGame(GameLevel.BASIC)
            game._select_target()

            # Lose all lives
            wrong_letters = ['x', 'y', 'z', 'w', 'v', 'u']
            for letter in wrong_letters:
                game.make_guess(letter)

            status = game.get_game_status()
            assert "Game over" in status
            assert game.target_word in status

    def test_body_part_methods(self):
        with patch.object(HangmanGame, '_load_dictionary', return_value=['test']):
            game = HangmanGame(GameLevel.BASIC)
            game._select_target()

            # Test different life states
            assert "   " in game._get_body_part()  # No damage
            assert "   " in game._get_legs_part()

            game.current_lives = 5  # 1 wrong guess
            assert "|" in game._get_body_part()

            game.current_lives = 4  # 2 wrong guesses
            assert "/|" in game._get_body_part()

            game.current_lives = 3  # 3 wrong guesses
            assert "/|\\" in game._get_body_part()

            game.current_lives = 2  # 4 wrong guesses
            assert "/" in game._get_legs_part()

            game.current_lives = 1  # 5 wrong guesses
            assert "/ \\" in game._get_legs_part()
