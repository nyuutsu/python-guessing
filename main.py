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
    self.SQ_STROKE_WIDTH = 5

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
    
    # end of constructor

  # based on the initialization of the game object we should be able to draw all the squares. do so.
  def draw_squares(self):
    for obj in self.SQUARES:
      obj[0].draw(self.WINDOW)
 
  # accepts a (assumed to be square) Rectangle object
  # returns a Point representing the Rectangle's centerpoint
  def get_center_of_this_square(self, square):
    center = Point(\
      square.getP1().getX() + self.HALF_SQUARE_WIDTH - self.HALF_GAP, \
      square.getP1().getY() + self.HALF_SQUARE_WIDTH - self.HALF_FONT_SIZE)
    return center

  # takes a "square tuple"
  # notices where you clicked and draws the corresponding secret (tuple[1]) in the center of the containing square (tuple[0])
  def unconditionally_permanently_reveal(self, data):
    # get the text we're printing
    center = self.get_center_of_this_square(data[0])
    text = Text(center, data[1])
    text.setSize(self.FONT_SIZE)
    text.setFace(self.FONT_FACE)
    text.draw(self.WINDOW)

  # takes a Point object
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
  def contents_of_square(self, data):
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
          return square # if you're here, you found a square

def main():
  game_instance = GameManager()
  game_instance.draw_squares()
  while(True):
    point_clicked = game_instance.WINDOW.getMouse() # Point
    is_in_square = game_instance.am_in_square(point_clicked) # Bool
    if is_in_square:
      specific_square = game_instance.contents_of_square(point_clicked) # SqTup
      game_instance.unconditionally_permanently_reveal(specific_square) # Void
    
if __name__ == '__main__':
  main()