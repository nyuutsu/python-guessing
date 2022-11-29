from third_party.graphics import color_rgb, GraphWin, Point, Rectangle, Text
import json
import math
import random
import string
import time

def gen_secrets(squares_count: int):
  secrets = []
  for char in string.ascii_uppercase:
    secrets.append(char)
    secrets.append(char)
  truncated_secrets = secrets[0:squares_count]
  #random.shuffle(truncated_secrets)  #turn off shuffle to test matching
  return iter(truncated_secrets)

class Square(Rectangle):
  def __init__(self, p1, p2, secret):
    Rectangle.__init__(self, p1, p2)
    self.secret = secret

class GameManager:
  """A round of the game "Concentration"

  To operate, call, in order:
    constructor
    boot()
    game_loop()
  """
  def __init__(self, width: int=500, height: int=500, squares_count: int=16, gap: int=25):
     # arg constants
    self.WIDTH = width  # window width
    self.HEIGHT = height  # window height
    self.SQUARES_COUNT = squares_count
    self.GAP = gap
     # computed constants  
    self.SQUARES_PER_ROW = int(math.floor(math.sqrt(self.SQUARES_COUNT)))
    self.MAX_SQUARE_WIDTH = self.WIDTH // self.SQUARES_PER_ROW
    self.squares = []
     # more constants
    self.FONT_SIZE = 30
    self.FONT_FACE = 'courier'
    self.SQ_STROKE_WIDTH = 5
     # with correct play you only need 0.8n cards of guesses
     # https://www.tandfonline.com/doi/abs/10.4169/amer.math.monthly.120.09.787
    self.MAX_GUESSES = int(math.ceil(self.SQUARES_COUNT * 0.8))
    self.remaining_guesses = self.MAX_GUESSES 
    self.FAIL_COOLDOWN = 1.5  # seconds
    color_file = open('color_file.json')
    self.colors = json.load(color_file)
    self.window = None

  def boot(self):
    self.secrets = gen_secrets(self.SQUARES_COUNT)
    self.gen_squares()
    self.create_window()
    self.draw_squares()
    
   # helper for create_one_row()
  def create_one_square(self, p1: Point, p2: Point):
    square = Square(p1, p2, next(self.secrets))
    square.setOutline(color_rgb(*self.colors['square_outline']))
    square.setFill(color_rgb(*self.colors['square']))
    square.setWidth(self.SQ_STROKE_WIDTH)
    self.squares.append(square)

   # helper for gen_squares()
  def create_one_row(self, quantity: int, width: int, displacement: int=0):
    x1 = 0
    y1 = displacement
    x2 = width
    y2 = displacement + width

    for item in range(quantity):
      self.create_one_square(Point(x1 + self.GAP, y1 + self.GAP), 
                             Point(x2 - self.GAP, y2 - self.GAP))
      x1 += width
      x2 += width

  def gen_squares(self):
    displacement = 0
    for row in range(self.SQUARES_PER_ROW):
      self.create_one_row(self.SQUARES_PER_ROW, self.MAX_SQUARE_WIDTH, displacement)
      displacement += self.MAX_SQUARE_WIDTH
  
  def create_window(self):
    self.window = GraphWin("My Window", self.WIDTH, self.HEIGHT)
    self.window.setBackground(color_rgb(*self.colors['background']))
  
  def draw_squares(self):
    for square in self.squares:
      square.draw(self.window)

  def reveal_and_return(self, square: Square):
    """Reveals text
    takes Square
    notices where you clicked and draws the corresponding secret (tuple[1]) in a Text at the center of the containing square (tuple[0])
    returns the Text
    """
    center = square.getCenter()
    text = Text(center, square.secret)
    text.setSize(self.FONT_SIZE)
    text.setFace(self.FONT_FACE)
    text.setTextColor(color_rgb(*self.colors['background']))
    text.draw(self.window)
    return text

  def contents_of_square(self, point: Point):
      click_x = point.getX()
      click_y = point.getY()

      for square in self.squares:
        p1 = square.getP1()
        p1x, p1y = p1.getX(), p1.getY()

        p2 = square.getP2()
        p2x, p2y = p2.getX(), p2.getY()

        if p1x <= click_x <= p2x and p1y <= click_y <= p2y:
          return square
      return None

   # listens for a click, looks at the list of [remaining] (Rectangle, string) for a cmpatible Rectangle, repeats this until match, returns tuple
  def get_first_square(self):
    while True:
      point_clicked = self.window.getMouse()  # Point
      square = self.contents_of_square(point_clicked)
      if square == None:
        continue  # must be in a square
      first_square = square
      return first_square
      
  def get_second_square(self, first_square: Square):
    while True:
      point_clicked = self.window.getMouse()  # Point
      second_square = self.contents_of_square(point_clicked)
      if second_square == None:
        continue  # must be in a square
      if first_square is second_square:
        continue  # must not be the same square
      return second_square

  def meditate(self):
    time.sleep(self.FAIL_COOLDOWN)

   # reasonable values to use to decenter buttons: 0.5, 1.5
  def generate_gutter_text(self, text: str, gutter_factor: float, horizontal_factor: float = 1.0):
    point = Point(
      int(math.ceil((self.WIDTH / 2) * horizontal_factor)),
      int(math.ceil(self.HEIGHT * (0.25 * gutter_factor))))
    text = Text(point, text)
    text.setTextColor(color_rgb(*self.colors['square']))
    text.setSize(self.FONT_SIZE)
    return text

  def flash_high_score(self, sleep_for: int=3):
    score_file = open('high_score.json')
    score = json.load(score_file)
    text = self.generate_gutter_text(f"High Score: {score['score']} moves", 3)
    text.draw(self.window)
    time.sleep(sleep_for)
    text.undraw()
    return score['score']

  def flash_taunt(self, sleep_for=3):
    text = self.generate_gutter_text(f"See if you can do better!", 3)
    text.draw(self.window)
    time.sleep(sleep_for)
    text.undraw()
    return text

  def update_high_score(self, new_score: int):
    with open('high_score.json', "r+") as score_file:
      data = json.load(score_file)
      data["score"] = new_score
      score_file.seek(0)
      json.dump(data, score_file, indent=2)
      score_file.truncate()

  def game_loop(self):
    """
    interpret results:
      match:
        leave match text revealed, discard Text references
          we can no longer hide the text, which is good!
        outline match Square borders, discard Square references
          we can no longer detect these Squares, simplifying our square-matching algorithm
          we can use whether any detectable Squares to check wins
      nomatch:
        outline nomatch Squares borders as incorrect
        allow player to meditate briefly
        hide unmatched Texts
        outline nomatch Squares borders as neutral
      finally:
        deduct a guess
    """
    title_text = self.generate_gutter_text(f'{self.SQUARES_COUNT} tiles! Match them!', 1)
    title_text.draw(self.window)

    high_score = self.flash_high_score()
     # while user has guesses and guessables
    while self.remaining_guesses > 0 and len(self.squares) != 0:
       # display currently remaining guesses
      guesses_text = self.generate_gutter_text(f'Guesses remaining: {self.remaining_guesses}', 3)
      guesses_text.draw(self.window)

       # prompt for a valid guess; reveal
      square_one = self.get_first_square()
      text_one = self.reveal_and_return(square_one)
      square_one.setOutline(color_rgb(*self.colors['square_maybe_outline']))
      
       # prompt for a valid other guess; reveal
      square_two = self.get_second_square(square_one)
      text_two = self.reveal_and_return(square_two)

      if square_one.secret == square_two.secret:  # match
        squares = [square_one, square_two]
        [s.setOutline(color_rgb(*self.colors['square_yes_outline'])) for s in squares]
        for square in squares:
          self.squares.remove(square)
      else:  # nomatch
        squares = [square_one, square_two]
        [s.setOutline(color_rgb(*self.colors['square_no_outline'])) for s in squares]
        self.meditate()  # reflect on your choices
        [s.setOutline(color_rgb(*self.colors['square_outline'])) for s in squares]
        texts = [text_one, text_two]
        for text in texts:
          text.undraw()
      self.remaining_guesses -= 1
      guesses_text.undraw()
     # can identify a win or loss based on whether there are detectable squares
    if len(self.squares) == 0:
      self.generate_gutter_text('You Win!', 2).draw(self.window)
      if self.remaining_guesses <= high_score:
        self.update_high_score(self.MAX_GUESSES - self.remaining_guesses)
        self.flash_high_score()
    else:
      outcome = self.generate_gutter_text('You Lose!', 2)
      outcome.draw(self.window)
    self.flash_taunt()
    #self.window.getMouse()

  """
  def play_again_buttons (self):
    buttons = [
      self.generate_gutter_text('✔️', 2, 0.5),
      self.generate_gutter_text('❌', 2, 1.5)]
    [button.draw(self.window) for button in buttons]
  """

def main():
  while True:
    game_instance = GameManager()
    game_instance.boot()
    game_instance.game_loop()
    
if __name__ == '__main__':
  main()