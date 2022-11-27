import guessing_game
import math
import pytest

game_instance = guessing_game.GameManager()
game_instance.boot()

assert game_instance.WIDTH == game_instance.HEIGHT
assert game_instance.WIDTH % 2 == 0
assert game_instance.GAP % 2 == 0
assert game_instance.SQUARES_COUNT % 2 == 0
assert math.sqrt(game_instance.SQUARES_COUNT) == int(game_instance.SQUARES_PER_ROW)
