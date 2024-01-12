import turtle
from abc import *

class Canvas:
    def __init__(self, w, h):
        # Inicializē turtle un ekrānu zīmējumam
        self.__turtle = turtle.Turtle()
        self.__screen = turtle.Screen()

        # Izveido ekrāna izmērus
        self.__screen.setup(width=w, height=h)
        
        # Paslēpt noklusējuma turtle kursoru
        self.__turtle.hideturtle()

    def draw(self, gObject):
        # Sagatavo turtle, lai pārvietotu bez izsekojuma
        self.__turtle.up()
        
        # Izslēgt animāciju, lai zīmētu vienmērīgāk
        self.__screen.tracer(0)
        
        # Izsaukt ģeometriskā objekta abstrakto _draw metodi
        gObject._draw(self.__turtle)
        
        # Ieslēgt animāciju pēc zīmēšanas
        self.__screen.tracer(1)


class GeometricObject(ABC):         # Manto no Abstraktās pamata klases
    def __init__(self):
        # Noklusējuma atribūti zīmēšanai
        self.__lineColor = 'black'  # Noklusējuma zīmēšanas krāsa
        self.__lineWidth = 1        # Noklusējuma līnijas platums 

    def getColor(self):
        return self.__lineColor

    def getWidth(self):
        return self.__lineWidth

    def setColor(self, color):
        self.__lineColor = color

    def setWidth(self, width):
        self.__lineWidth = width

    @abstractmethod                 # Norādīt, ka metode ir abstrakta
    def _draw(self, someturtle):
        pass                       

class Point(GeometricObject):
    def __init__(self, coordinates):
        super().__init__()
        # Koordinātas tiek glabātas kā tuple
        self.__coordinates = coordinates

    def getCoord(self):
        return self.__coordinates

    def getX(self):
        return self.__coordinates[0]

    def getY(self):
        return self.__coordinates[1]

    def _draw(self, turtle):
        # Pārvietot turtle uz norādītajām koordinātēm un zīmēt punktu
        turtle.goto(self.getX(), self.getY())
        turtle.dot(self.getWidth(), self.getColor())


class Line(GeometricObject):
    def __init__(self, p1, p2):
        super().__init__()
        # Punkti, kas nosaka līniju
        self.__p1 = p1
        self.__p2 = p2

    def getP1(self):
        return self.__p1

    def getP2(self):
        return self.__p2

    def _draw(self, turtle):
        # Zīmēt līniju starp diviem punktiem ar noteiktajiem atribūtiem
        turtle.color(self.getColor())
        turtle.width(self.getWidth())
        turtle.up()
        turtle.goto(self.__p1.getCoord())
        turtle.down()
        turtle.goto(self.__p2.getCoord())


def test2():
    # Izveidot kanvasu ar izmēriem 500x500
    myCanvas = Canvas(500, 500)

    # Izveidot četrus punktus
    point1 = Point((-100, -100))
    point2 = Point((100, 100))
    point3 = Point((-100, 100))
    point4 = Point((100, -100))

    # Izveidot divas līnijas, izmantojot punktus
    line1 = Line(point1, point2)
    line2 = Line(point3, point4)

    # Iestatīt atribūtus līnijām
    line1.setWidth(4)    
    myCanvas.draw(line1)
    myCanvas.draw(line2)

    # Mainīt līniju atribūtus
    line1.setColor('red')
    line2.setWidth(4)

if __name__ == "__main__":
    # Palaist testu un parādīt turtle grafiku
    test2()
    turtle.done()
