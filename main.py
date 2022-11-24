from graphics import *
import math
import random
import string

class GameManager:
  def __init__(self, width=500, height=500, squares_count=16, gap=50):
    # initialize arg constants
    self.WIDTH = width # window width
    self.HEIGHT = width # window height
    self.SQUARES_COUNT = squares_count
    self.GAP = gap
    
    # initialize computed constants  
    self.HALF_GAP = self.GAP // 2
    self.SQUARES_PER_ROW = int(math.floor(math.sqrt(self.SQUARES_COUNT)))
    self.MAX_SQUARE_WIDTH = self.WIDTH // self.SQUARES_PER_ROW
    self.HALF_SQUARE_WIDTH = self.MAX_SQUARE_WIDTH // 2
    self.SQUARES = []

    # initialize magic constants
    self.FONT_SIZE = 30
    self.HALF_FONT_SIZE = self.FONT_SIZE // 2
    self.FONT_FACE = 'courier'
    self.BG_COLOR = 'grey'
    self.SQ_COLOR = 'lightgrey'
    self.SQ_STROKE = 'purple'
    self.SQ_STROKE_WIDTH = 10

    # sanity check
    assert width == height
    assert width % 2 == 0
    assert gap % 2 == 0
    assert math.sqrt(self.SQUARES_COUNT) == int(self.SQUARES_PER_ROW)
    
    # helper for create_one_square()
    def gen_secrets(squares_count):
      secrets = []
      for char in string.ascii_letters:
        secrets.append(char)
        secrets.append(char) # we want these to come in pairs
      truncated_secrets = secrets[0:squares_count]
      random.shuffle(truncated_secrets)
      return iter(truncated_secrets)
    self.secrets = gen_secrets(self.SQUARES_COUNT) # iterator!
    
    # helper for create_one_row()
    def create_one_square(p1, p2):
      square = Rectangle(p1, p2)
      square.setOutline(self.SQ_STROKE)
      square.setFill(self.SQ_COLOR)
      square.setWidth(self.SQ_STROKE_WIDTH)
      secret = next(self.secrets)
      self.SQUARES.append((square, secret))

    # helper for gen_squares()
    def create_one_row(quantity, width, displacement = 0):
      x1 = 0
      y1 = displacement
      x2 = width
      y2 = displacement + width

      for item in range(quantity):
        create_one_square(Point(x1 + self.HALF_GAP, y1 + self.HALF_GAP), Point(x2 - self.HALF_GAP, y2 - self.HALF_GAP))
        x1 += width
        x2 += width

    def gen_squares():
      displacement = 0
      for row in range(self.SQUARES_PER_ROW):
        create_one_row(self.SQUARES_PER_ROW, self.MAX_SQUARE_WIDTH, displacement)
        displacement += self.MAX_SQUARE_WIDTH
    gen_squares()

    # create window  
    def create_window():
      self.WINDOW = GraphWin("My Window", self.WIDTH, self.HEIGHT)
      self.WINDOW.setBackground(self.BG_COLOR)
    create_window()

  def draw_board(self):
    for obj in self.SQUARES:
      obj[0].draw(self.WINDOW)
      # this APPROXIMATES centering the text in the square. revisit this
      # eventually, don't actually show these until needed
      text = Text(Point(\
        obj[0].getP1().getX() + self.HALF_SQUARE_WIDTH - self.HALF_GAP, \
        obj[0].getP1().getY() + self.HALF_SQUARE_WIDTH - self.HALF_FONT_SIZE), \
        obj[1])
      text.setSize(self.FONT_SIZE)
      text.setFace(self.FONT_FACE)
      text.draw(self.WINDOW)

def main():
  game_instance = GameManager()  
  game_instance.draw_board()
  game_instance.WINDOW.getMouse() # on click return a point(click_x, click_y) (and so exit)
  
main()