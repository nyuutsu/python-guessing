from third_party.graphics import color_rgb, GraphWin, Point, Rectangle, Text
import json
import math
import random
import string
import time

def gen_secrets(squares_count):
  secrets = []
  for char in string.ascii_uppercase:
    secrets.append(char)
    secrets.append(char)
  truncated_secrets = secrets[0:squares_count]
  #random.shuffle(truncated_secrets)  #turn off shuffle to test matching
  return iter(truncated_secrets)

class GameManager:
  """A round of the game "Concentration"

  To operate, call, in order:
    constructor
    boot()
    game_loop()
  """
  def __init__(self, width=500, height=500, squares_count=16, gap=25):
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
    self.HALF_FONT_SIZE = self.FONT_SIZE // 2
    self.FONT_FACE = 'courier'
    color_file = open ('color_file.json')
    self.colors = json.load(color_file)
    self.SQ_STROKE_WIDTH = 5
     # with correct play you only need 0.8n cards of guesses
     # https://www.tandfonline.com/doi/abs/10.4169/amer.math.monthly.120.09.787
    self.MAX_GUESSES = int(math.ceil(self.SQUARES_COUNT * 0.8))
    self.remaining_guesses = self.MAX_GUESSES 
    self.FAIL_COOLDOWN = 1.5  # seconds
    self.window = None

  def boot(self):
    self.secrets = gen_secrets(self.SQUARES_COUNT)
    self.gen_squares()
    self.create_window()
    self.draw_squares()
    #color_rgb(*self.colors['square'])
   # helper for create_one_row()
  def create_one_square(self, p1, p2):
    square = Rectangle(p1, p2)
    square.setOutline(color_rgb(*self.colors['square_outline']))
    square.setFill(color_rgb(*self.colors['square']))
    square.setWidth(self.SQ_STROKE_WIDTH)
    secret = next(self.secrets)
    self.squares.append((square, secret))

   # helper for gen_squares()
  def create_one_row(self, quantity, width, displacement = 0):
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
    for obj in self.squares:
      obj[0].draw(self.window)

  def reveal_and_return(self, rect_secret_tuple):
    """Reveals text
    takes (Rectangle, string)
    notices where you clicked and draws the corresponding secret (tuple[1]) in a Text at the center of the containing square (tuple[0])
    returns the Text
    """
    center = rect_secret_tuple[0].getCenter()
    text = Text(center, rect_secret_tuple[1])
    text.setSize(self.FONT_SIZE)
    text.setFace(self.FONT_FACE)
    text.setTextColor(color_rgb(*self.colors['background']))
    text.draw(self.window)
    return text

   # takes a Point object
   # assumes Point is within one of the square tuples in self.squares
   # returns that tuple
  def contents_of_square(self, data):
      click_x = data.getX()
      click_y = data.getY()

      for square in self.squares:
        p1 = square[0].getP1()
        p1x, p1y = p1.getX(), p1.getY()

        p2 = square[0].getP2()
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
      
  def get_second_square(self, first_square):
    while True:
      point_clicked = self.window.getMouse()  # Point
      second_square = self.contents_of_square(point_clicked)
      if second_square == None:
        continue  # must be in a square
      if first_square[0] is second_square[0]:
        continue  # must not be the same square
      return second_square

  def meditate(self):
    time.sleep(self.FAIL_COOLDOWN)

   # reasonable values to use to decenter buttons: 0.5, 1.5
  def generate_gutter_text(self, text, gutter_factor, horizontal_factor = 1.0):
    point = Point(
      int(math.ceil((self.WIDTH / 2) * horizontal_factor)),
      int(math.ceil(self.HEIGHT * (0.25 * gutter_factor))))
    text = Text(point, text)
    text.setTextColor(color_rgb(*self.colors['square']))
    text.setSize(self.FONT_SIZE)
    return text

  def game_loop(self):
    """
    interpret results:
      match:
        leave match text revealed, discard Text references
          we can no longer hide the text, which is good!
        outline match Rectangle borders, discard (Rectangle, text) references
          we can no longer detect these Rectangles, simplifying our square-matching algorithm
          we can use whether any detectable (Rectangle, text)s to check wins
      nomatch:
        outline nomatch Rectangle borders as incorrect
        allow player to meditate briefly
        hide unmatched Texts
        outline nomatch Rectangle borders as neutral
      finally:
        deduct a guess
    """
    title_text = self.generate_gutter_text(f'{self.SQUARES_COUNT} tiles! Match them!', 1)
    title_text.draw(self.window)
     # while user has guesses and guessables
    while self.remaining_guesses > 0 and len(self.squares) != 0:
       # display currently remaining guesses
      guesses_text = self.generate_gutter_text(f'Guesses remaining: {self.remaining_guesses}', 3)
      guesses_text.draw(self.window)

       # prompt for a valid guess; reveal
      square_one = self.get_first_square()
      text_one = self.reveal_and_return(square_one)
      square_one[0].setOutline(color_rgb(*self.colors['square_maybe_outline']))
      
       # prompt for a valid other guess; reveal
      square_two = self.get_second_square(square_one)
      text_two = self.reveal_and_return(square_two)

      if square_one[1] == square_two[1]:  # match
        squares = [square_one, square_two]
        [s[0].setOutline(color_rgb(*self.colors['square_yes_outline'])) for s in squares]
        for square in squares:
          self.squares.remove(square)
      else:  # nomatch
        squares = [square_one, square_two]
        [s[0].setOutline(color_rgb(*self.colors['square_no_outline'])) for s in squares]
        self.meditate()  # reflect on your choices
        [s[0].setOutline(color_rgb(*self.colors['square_outline'])) for s in squares]
        texts = [text_one, text_two]
        for text in texs:
          text.undraw()
      self.remaining_guesses -= 1
      guesses_text.undraw()
     # can identify a win or loss based on whether there are detectable squares
    if len(self.squares) == 0:
      self.generate_gutter_text('You Win!', 2).draw(self.window)
    else:
      outcome = self.generate_gutter_text('You Lose!', 2)
      outcome.draw(self.window)
    self.window.getMouse()

   # TODO
  def play_again_buttons (self):
    buttons = [\
      self.generate_gutter_text('Yes', 2, 0.5), \
      self.generate_gutter_text('No', 2, 1.5)]
    for button in buttons:
      button.draw(self.window)  

def main():
  while True:
    game_instance = GameManager()
    game_instance.boot()
    game_instance.game_loop()
    
if __name__ == '__main__':
  main()

"""
TODO:
  high score track + display
  ask if play again
  cut down on repetition in game_loop & am_in_square + contents_of_square
"""
