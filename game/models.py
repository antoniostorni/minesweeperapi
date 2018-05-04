from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

PLAYING = 'playing'
GAME_OVER = 'game_over'

class Grid(models.Model):
    """
    Grid model
    """

    STATUS_CHOICES = (
        (PLAYING, 'Playing'),
        (GAME_OVER, 'Game Over'),
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(choices=STATUS_CHOICES, max_length=20, default=PLAYING)

    height = models.IntegerField(default=8)
    width = models.IntegerField(default=8)
    number_of_mines = models.IntegerField(default=1)

    belongs_to = models.ForeignKey(User, on_delete=models.CASCADE)

    def total_of_squares(self):
        """
        :return: Total of squares
        """
        return self.height * self.width

    def build_grid_squares_structure(self):
        """
        Creates the squares for the grid structure
        :return:
        """
        for x in range(0, self.width):
            for y in range(0, self.height):
                new_square = Square(x=x, y=y, grid=self)
                new_square.save()

        # Add mines to the game = Those mines are random squares positions
        mine_squares = self.square_set.order_by('?')[:self.number_of_mines]
        for square in mine_squares:
            square.act_as_mine()


class Square(models.Model):
    """
    Square model
    """
    x = models.IntegerField()
    y = models.IntegerField()
    grid = models.ForeignKey(Grid, on_delete=models.CASCADE)
    flagged = models.BooleanField(default=False)
    explored = models.BooleanField(default=False)
    mine = models.BooleanField(default=False)
    mines = models.IntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_adjacents(self):
        """
        :return: list of square adjacents
        """

        adjacents = self.grid.square_set.filter(
            Q(x=self.x - 1, y=self.y - 1) |
            Q(x=self.x, y=self.y - 1) |
            Q(x=self.x + 1, y=self.y - 1) |
            Q(x=self.x - 1, y=self.y) |
            Q(x=self.x + 1, y=self.y) |
            Q(x=self.x - 1, y=self.y + 1) |
            Q(x=self.x, y=self.y + 1) |
            Q(x=self.x + 1, y=self.y + 1)
        )

        return adjacents

    def act_as_mine(self):
        """
        Set square to act as mine
        :return:
        """

        self.mine = True
        self.mines = 0
        for adjacent in self.adjacents():
            if not adjacent.mine:
                adjacent.mines += 1
                adjacent.save()
        self.save()

    def toggle_flag(self):
        """
        Toggle flag on square
        :return:
        """
        self.flagged = not self.flagged

    def explore(self):
        """
        Explore square
        :return:
        """

        if self.mine:
            self.grid.status = GAME_OVER
            self.grid.save()
        else:
            self.explored = True
            if self.mines == 0:
                self.explore_adjacents()

        self.save()

    def explore_adjacents(self):
        """
        Explore adjacentes squares (runs when square had 0 mines and propagates)
        :param adjacents:
        :return:
        """
        for square in self.get_adjacents():
            explore(square)


