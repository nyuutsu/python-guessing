__author__ = 'dmc'

## This is a set of utilities for manipulating fonts and strings.
from tkinter import font as tkFont
from graphics import Text
from graphics import GraphicsError

## Define the FontUtils class
class FontUtils:

    ## This method calculates the width and height of a Text object.
    ## It uses the font information stored in the object to invoke the correct font metrics.
    ## Input: an instance of a graphics.Text object
    ## Output: a dict containing the width and height of the text, in pixels.
    @staticmethod
    def getStringDimensions( textObject ):
        fontOption = textObject.config[ 'font' ]
        font = tkFont.Font( family=fontOption[0], size=fontOption[1] )
        ( w,h ) = (font.measure( textObject.getText() ), font.metrics("linespace") )
        return {'width' : w, 'height': h }

    ## This method calculates the width of a Text object.
    ## It uses the font information stored in the object to invoke the correct font metrics.
    ## Input: an instance of a graphics.Text object
    ## Output: the width of the object, in pixels.
    ## Raises: GraphicError if textObject is not an instance of graphics.Text
    @staticmethod
    def getStringWidth( textObject ):
        # if isinstance( textObject, Text ):
        #     pass
        # else:
        #     raise GraphicsError( "Object is not a text object" )

        try:
            fontOption = textObject.config[ 'font' ]
            font = tkFont.Font( family=fontOption[0], size=fontOption[1] )
            w = font.measure( textObject.getText() )
            return w
        except KeyError:
            pass
        ## We can only get here if an error occurred.
        raise GraphicsError("Object is not a text object")
