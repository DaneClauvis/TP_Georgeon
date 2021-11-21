#!/usr/bin/env python
import turtle

# Olivier Georgeon, 2021.
# This code is used to teach Developmental AI.
#
# Inspired by Turtle Python tutorial:
#   * https://www.javatpoint.com/python-turtle-programming


class TurtlePyEnacter:

    def __init__(self):
        """ Creating the Turtle window """
        self.screen = turtle.getscreen()
        self.screen.setup(400, 400)
        self.turtle = turtle.Turtle("turtle")
        self.turtle.color("green")
        self.turtle.speed(1)

    def outcome(self, action):
        """ Enacting an action and returning the outcome """
        self.turtle.color("green")
        _outcome = 0
        for i in range(10):
            if action == 0:
                # move forward
                self.turtle.speed(1)
                self.turtle.forward(5)
            elif action == 1:
                # rotate left
                self.turtle.speed(10)
                self.turtle.left(4)
                self.turtle.forward(2)
            elif action == 2:
                # rotate right
                self.turtle.speed(10)
                self.turtle.right(4)
                self.turtle.forward(2)

            # Bump on screen edge and return outcome 1
            (screen_x, screen_y) = self.screen.screensize()
            if self.turtle.xcor() < -screen_x/2:
                self.turtle.goto(-screen_x/2, self.turtle.ycor())
                _outcome = 1
                self.turtle.color("red")
            if self.turtle.xcor() > screen_x/2:
                self.turtle.goto(screen_x/2, self.turtle.ycor())
                _outcome = 1
                self.turtle.color("red")
            if self.turtle.ycor() < -screen_y/2:
                self.turtle.goto(self.turtle.xcor(), -screen_y/2)
                _outcome = 1
                self.turtle.color("red")
            if self.turtle.ycor() > screen_y/2:
                self.turtle.goto(self.turtle.xcor(), screen_y/2)
                _outcome = 1
                self.turtle.color("red")

        return _outcome


if __name__ == '__main__':
    """ Main """
    x = TurtlePyEnacter()
    interaction_step = 0 # Prevents triggering a new interaction before the previous is finished

    def k1():
        global interaction_step
        if interaction_step == 0:
            interaction_step = 1
            print(x.outcome(0))
            interaction_step = 0

    def k2():
        global interaction_step
        if interaction_step == 0:
            interaction_step = 1
            print(x.outcome(1))
            interaction_step = 0

    def k3():
        global interaction_step
        if interaction_step == 0:
            interaction_step = 1
            print(x.outcome(2))
            interaction_step = 0

    x.screen.onkey(k1, "Up")  # the up arrow key
    x.screen.onkey(k2, "Left")  # the left arrow key
    x.screen.onkey(k3, "Right")  # you get it!

    x.screen.listen()
    x.screen.mainloop()