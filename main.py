from graphics import *
import math
import string

class GameManager:
  def __init__(self, width=500, height=500, squares_count=16, gap=10):
    # initialize arg constants
    self.WIDTH = width # window width
    self.HEIGHT = width # window height
    self.SQUARES_COUNT = squares_count
    self.GAP = gap
    
    # initialize computed constants  
    self.HALF_GAP = self.GAP // 2
    self.SQUARES_PER_ROW = int(math.floor(math.sqrt(self.SQUARES_COUNT)))
    self.MAX_SQUARE_WIDTH = self.WIDTH / self.SQUARES_PER_ROW

    # input validation
    assert width == height
    assert width % 2 == 0
    assert gap % 2 == 0
    assert math.sqrt(self.SQUARES_COUNT) == int(self.SQUARES_PER_ROW) # test ↑
    
    self.SQUARES = [] # store the drawn square objects
    # generate the data for secrets as pairs of letters
    def gen_secrets(squares_count):
      secrets = []
      for char in string.ascii_letters:
        secrets.append(char)
        secrets.append(char) # we want these to come in pairs
      return iter(secrets[0:squares_count]) # return an iterator of list
    self.secrets = gen_secrets(self.SQUARES_COUNT)

    # create window  
    self.WINDOW = GraphWin("My Window", self.WIDTH, self.HEIGHT)

  def draw_board():
    pass

  """
  draw_one_square() also generates and stores the square, which is bad
  why self is bad: https://github.com/Droogans/unmaintainable-code
    Make sure that every method does a little bit more (or less) than its name suggests. As a simple example, a method named isValid(x) should as a side effect convert x to binary and store the result in a database.
  """

  # template for drawing one square
  def draw_one_square(self, p1, p2):
      square = Rectangle(p1, p2)
      square.draw(self.WINDOW)
      secret = next(self.secrets)
      print(secret) #can remove
      self.SQUARES.append((square, secret))

  # template for one row of squares; relies on draw_one_square
  def draw_one_row(self, quantity, width, displacement = 0):
    x1 = 0
    y1 = displacement
    x2 = width
    y2 = displacement + width

    for item in range(quantity):
      self.draw_one_square(Point(x1, y1), Point(x2, y2))
      x1 += width
      x2 += width

def main():
  game_instance = GameManager()
    
  # test
  def test(game_instance):
    displacement = 0
    for row in range(game_instance.SQUARES_PER_ROW):
      game_instance.draw_one_row(game_instance.SQUARES_PER_ROW, game_instance.MAX_SQUARE_WIDTH, displacement)
      displacement += game_instance.MAX_SQUARE_WIDTH

  test(game_instance)

  
  
  
  game_instance.WINDOW.getMouse() # on click return a point(click_x, click_y) (and so exit)
  
main()