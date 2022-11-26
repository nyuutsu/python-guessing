from graphics import *
import math
import random
import string
import time

class GameManager:
  """A round of the game "Concentration"

  To operate, call, in order:
    constructor
    boot()
    game_loop()
  """
  def __init__(self, width=500, height=500, squares_count=16, gap=50):
    # arg constants
    self.WIDTH = width # window width
    self.HEIGHT = width # window height
    self.SQUARES_COUNT = squares_count
    self.GAP = gap
    # computed constants  
    self.HALF_GAP = self.GAP // 2
    self.SQUARES_PER_ROW = int(math.floor(math.sqrt(self.SQUARES_COUNT)))
    self.MAX_SQUARE_WIDTH = self.WIDTH // self.SQUARES_PER_ROW
    self.HALF_SQUARE_WIDTH = self.MAX_SQUARE_WIDTH // 2
    self.SQUARES = [] # should this be CONSTANTCAPPED or no
    # more constants
    self.FONT_SIZE = 30
    self.HALF_FONT_SIZE = self.FONT_SIZE // 2
    self.FONT_FACE = 'courier'
    self.BG_COLOR = color_rgb(0, 43, 54)
    self.SQ_COLOR = color_rgb(253, 246, 227)
    self.SQ_STROKE = color_rgb(108, 113, 196)
    self.YES_STROKE = color_rgb(133, 153, 0)
    self.MAYBE_STROKE = color_rgb(181, 137, 0)
    self.NO_STROKE = color_rgb(211, 54, 130)
    self.SQ_STROKE_WIDTH = 5
    # with correct play you only need 0.8n cards of guesses
    # https://www.tandfonline.com/doi/abs/10.4169/amer.math.monthly.120.09.787
    self.MAX_GUESSES = int(math.ceil(self.SQUARES_COUNT * 0.8))
    self.remaining_guesses = self.MAX_GUESSES 
    self.FAIL_COOLDOWN = 1.5 # seconds

    """
    # sanity check
    assert width == height
    assert width % 2 == 0
    assert gap % 2 == 0
    assert self.SQUARES_COUNT % 2 == 0
    assert math.sqrt(self.SQUARES_COUNT) == int(self.SQUARES_PER_ROW)
    """

  def boot(self):
    self.secrets = self.gen_secrets(self.SQUARES_COUNT)
    self.gen_squares()
    self.create_window()
    self.draw_squares()

  # helper for create_one_square()
  @classmethod
  def gen_secrets(cls, squares_count):
    secrets = []
    for char in string.ascii_uppercase:
      secrets.append(char)
      secrets.append(char) # we want these to come in pairs. better way?
    truncated_secrets = secrets[0:squares_count]
    random.shuffle(truncated_secrets) #turn off shuffle to test matching
    return iter(truncated_secrets)
  
  # helper for create_one_row()
  def create_one_square(self, p1, p2):
    square = Rectangle(p1, p2)
    square.setOutline(self.SQ_STROKE)
    square.setFill(self.SQ_COLOR)
    square.setWidth(self.SQ_STROKE_WIDTH)
    secret = next(self.secrets)
    self.SQUARES.append((square, secret))

  # helper for gen_squares()
  def create_one_row(self, quantity, width, displacement = 0):
    x1 = 0
    y1 = displacement
    x2 = width
    y2 = displacement + width

    for item in range(quantity):
      self.create_one_square(Point(x1 + self.HALF_GAP, y1 + self.HALF_GAP), Point(x2 - self.HALF_GAP, y2 - self.HALF_GAP))
      x1 += width
      x2 += width

  def gen_squares(self):
    displacement = 0
    for row in range(self.SQUARES_PER_ROW):
      self.create_one_row(self.SQUARES_PER_ROW, self.MAX_SQUARE_WIDTH, displacement)
      displacement += self.MAX_SQUARE_WIDTH
  
  def create_window(self):
    self.WINDOW = GraphWin("My Window", self.WIDTH, self.HEIGHT)
    self.WINDOW.setBackground(self.BG_COLOR)
  
  def draw_squares(self):
    for obj in self.SQUARES:
      obj[0].draw(self.WINDOW)

  # takes (Rectangle, string)
  # notices where you clicked and draws the corresponding secret (tuple[1]) in a Text at the center of the containing square (tuple[0])
  # returns the Text
  def reveal_and_return(self, rect_secret_tuple):
    # get the text we're printing
    center = rect_secret_tuple[0].getCenter()
    text = Text(center, rect_secret_tuple[1])
    text.setSize(self.FONT_SIZE)
    text.setFace(self.FONT_FACE)
    text.setTextColor(self.BG_COLOR)
    text.draw(self.WINDOW)
    return text

  # takes a Point
  # figures out whether the Point is within one of the squares in self.SQUARES
  # returns a boolean
  def am_in_square(self, data):
    # can I get out of having to write all this out?
    click_x = data.getX()
    click_y = data.getY()

    for square in self.SQUARES:
      p1 = square[0].getP1()
      p1x = p1.getX()
      p1y = p1.getY()

      p2 = square[0].getP2()
      p2x = p2.getX()
      p2y = p2.getY()

      if click_x >= p1x and click_x <= p2x and click_y >= p1y and click_y <= p2y:
        return True # if you're here, you found a square
    return False # if you made it here this isn't a square

  # takes a Point object
  # assumes Point is within one of the square tuples in self.SQUARES
  # returns that tuple
  # I tried reworking this and am_in_square to use a decorator since they're like 99% the same function but I didn't figure it out and moved on. revisit!
  def contents_of_square(self, data):
      # can I get out of having to write all this out AGAIN
      click_x = data.getX()
      click_y = data.getY()

      for square in self.SQUARES:
        p1 = square[0].getP1()
        p1x = p1.getX()
        p1y = p1.getY()

        p2 = square[0].getP2()
        p2x = p2.getX()
        p2y = p2.getY()

        if click_x >= p1x and click_x <= p2x and click_y >= p1y and click_y <= p2y:
          return square

  # listens for a click, looks at the list of [remaining] (Rectangle, string) for a cmpatible Rectangle, repeats this until match, returns tuple
  def get_first_square(self):
    while(True):
      point_clicked = self.WINDOW.getMouse() # Point
      is_in_square = self.am_in_square(point_clicked) # Bool
      if is_in_square == False:
        continue # must be in a square
      first_square = self.contents_of_square(point_clicked)
      return first_square
      
  def get_second_square(self, first_square):
    while(True):
      point_clicked = self.WINDOW.getMouse() # Point
      is_in_square = self.am_in_square(point_clicked) # Bool
      if is_in_square == False:
        continue # must be in a square
      second_square = self.contents_of_square(point_clicked) # SqTup
      if first_square[0] is second_square[0]:
        continue # must not be the same square
      return second_square

  def meditate(self):
    time.sleep(self.FAIL_COOLDOWN)

  # reasonable values to use to decenter buttons: 0.5, 1.5
  def generate_gutter_text(self, text, gutter_factor, horizontal_factor = 1):
    text = Text(\
      Point(\
        int(math.ceil((self.WIDTH / 2) * horizontal_factor)), \
        int(math.ceil(self.HEIGHT * (0.25 * gutter_factor)))), \
        text)
    text.setTextColor(self.SQ_COLOR)
    text.setSize(self.FONT_SIZE)
    return text

  def game_loop(self):
    title_text = self.generate_gutter_text(f'{self.SQUARES_COUNT} tiles! Match them!', 1)
    title_text.draw(self.WINDOW)
    # while user has guesses and guessables
    while(self.remaining_guesses > 0 and len(self.SQUARES) != 0):
      # display currently remaining guesses
      guesses_text = self.generate_gutter_text(f'Guesses remaining: {self.remaining_guesses}', 3)
      guesses_text.draw(self.WINDOW)

      # prompt for a valid guess; reveal
      square_one = self.get_first_square()
      text_one = self.reveal_and_return(square_one)
      square_one[0].setOutline(self.MAYBE_STROKE)
      
      # prompt for a valid other guess; reveal
      square_two = self.get_second_square(square_one)
      text_two = self.reveal_and_return(square_two)

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
      if square_one[1] == square_two[1]: # match
        square_one[0].setOutline(self.YES_STROKE)
        square_two[0].setOutline(self.YES_STROKE)
        self.SQUARES.remove(square_one)
        self.SQUARES.remove(square_two)
      else: # nomatch
        square_one[0].setOutline(self.NO_STROKE)
        square_two[0].setOutline(self.NO_STROKE) 
        self.meditate() # reflect on your choices for three seconds
        square_one[0].setOutline(self.SQ_STROKE)
        square_two[0].setOutline(self.SQ_STROKE) # writing these calls twice is a sign I should somehow be avoiding this
        text_one.undraw()
        text_two.undraw()
      self.remaining_guesses -= 1
      guesses_text.undraw()
    # can identify a win or loss based on whether there are detectable squares
    if len(self.SQUARES) == 0:
      self.generate_gutter_text('You Win!', 2).draw(self.WINDOW)
    else:
      outcome = self.generate_gutter_text('You Lose!', 2)
      outcome.draw(self.WINDOW)
    self.WINDOW.getMouse()

  # TODO
  def play_again_buttons (self):
    buttons = [\
      self.generate_gutter_text('Yes', 2, 0.5), \
      self.generate_gutter_text('No', 2, 1.5)]
    for button in buttons:
      button.draw(self.WINDOW)

def main():
  while(True):
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
