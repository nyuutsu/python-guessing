from graphics import *
import math
import string

"""
verify that things work as expected
can draw the squares per computed dimensions
can store secret in square
"""

def main():
  # constants & initialization
  vwidth = 500 # window width
  vheight = vwidth # window height
  squares_count = 16 # amount of squares
  squares_per_row = int(math.floor(math.sqrt(squares_count))) # "" per row
  assert math.sqrt(squares_count) == int(squares_per_row) # test ↑
  max_square_width = vwidth / squares_per_row # sq dimension  == max fit
  assert max_square_width == 125 # test ↑
  squares = [] # store the square objects
  # function to generate the data for secrets
  def gen_secrets():
    secrets = []
    for char in string.ascii_letters:
      secrets.append(char)
      secrets.append(char) # we want these to come in pairs
    return iter(secrets[0:squares_count]) # return an iterator of list
  secrets = gen_secrets() # iterable data for secrets
  
  # create window  
  win = GraphWin("My Window", vwidth, vheight)

  # draw functions trust num_rows == num_columns
  
  """
  draw_one_square() also generates and stores the square, which is bad
  why this is bad: https://github.com/Droogans/unmaintainable-code
    Make sure that every method does a little bit more (or less) than its name suggests. As a simple example, a method named isValid(x) should as a side effect convert x to binary and store the result in a database.
  """
  # template for drawing one square
  def draw_one_square(p1, p2, window = win):
      square = Rectangle(p1, p2)
      square.draw(win)
      secret = next(secrets)
      print(secret) #can remove
      squares.append((square, secret))

  # template for one row of squares; relies on draw_one_square
  def draw_one_row(quantity, width, displacement = 0):
    x1 = 0
    y1 = displacement
    x2 = width
    y2 = displacement + width

    for item in range(quantity):
      draw_one_square(Point(x1, y1), Point(x2, y2))
      x1 += width
      x2 += width
  
  # test
  def test():
    displacement = 0
    for row in range(squares_per_row):
      draw_one_row(squares_per_row, max_square_width, displacement)
      displacement += max_square_width
    print(squares)

  test() # run the test
  
  win.getMouse() # on click return a point(click_x, click_y) (and so exit)
  
main()