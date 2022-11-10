from random import randrange as rd
import matplotlib.pyplot as plt


class Game:

    MAP_LENGTH = 16
    OBSTACLE_QUANTITY = 3
    MARGIN = 0.25

    def __init__(self):
        self.agent_coordinate = 0
        self.obstacle_coordinate = 0
        self.target_coordinate = 0
        self.list_of_points = []
        self.obstacle_number_list = []
        self.set_of_points = set()
        self.x = 0
        self.y = 0

        self.draw_table()  # отрисовка поля

    def draw_table(self):
        """Отрисовка главного поля."""
        quality = 0
        while len(self.list_of_points) < Game.MAP_LENGTH:
            self.list_of_points.append([self.x, self.y, quality])
            self.x += 1
            if self.x == 4:
                self.x = 0
                self.y += 1
        # Координата агента
        self.agent_coordinate = rd(0, Game.MAP_LENGTH - 1)
        while self.agent_coordinate in self.set_of_points:
            self.agent_coordinate = rd(0, Game.MAP_LENGTH - 1)
        self.set_of_points.add(self.agent_coordinate)
        self.list_of_points[self.agent_coordinate][2] = 1
        # Препятствия
        self.obstacle_coordinate = rd(0, Game.MAP_LENGTH - 1)
        obstacle_number = 0
        while obstacle_number < Game.OBSTACLE_QUANTITY:
            while self.obstacle_coordinate in self.set_of_points:
                self.obstacle_coordinate = rd(0, Game.MAP_LENGTH - 1)
            self.set_of_points.add(self.obstacle_coordinate)
            self.list_of_points[self.obstacle_coordinate][2] = 2
            obstacle_number += 1
            self.obstacle_number_list.append(self.obstacle_coordinate)
        # Координата цели
        self.target_coordinate = rd(0, Game.MAP_LENGTH - 1)
        while self.target_coordinate in self.set_of_points:
            self.target_coordinate = rd(0, Game.MAP_LENGTH - 1)
        self.set_of_points.add(self.target_coordinate)
        self.list_of_points[self.target_coordinate][2] = 3

        self.draw_markup()  # разметка
        self.draw_figurines()  # фигурки
        plt.grid()

    @staticmethod
    def draw_markup():
        """Вспомогательная - отрисовка координат."""
        plt.xlim([-0.5, 3.5])
        plt.ylim([-0.5, 3.5])

        coordinate = -0.5
        while coordinate != 4.5:
            plt.vlines(coordinate, -0.5, 3.5, color='k')
            plt.hlines(coordinate, -0.5, 3.5, color='k')
            coordinate += 1
        plt.grid()

    def draw_figurines(self):
        """Отрисовка фигурок - агента, препятствий и цели."""
        for i in range(Game.MAP_LENGTH):
            if self.list_of_points[i][2] == 1:
                plt.text(self.list_of_points[i][0] + Game.MARGIN,  # агент
                         self.list_of_points[i][1] + Game.MARGIN,
                         "A", size='large')
            if self.list_of_points[i][2] == 2:
                plt.text(self.list_of_points[i][0], self.list_of_points[i][1], "#")  # препятствие
            if self.list_of_points[i][2] == 3:
                plt.text(self.list_of_points[i][0] + Game.MARGIN,  # цель
                         self.list_of_points[i][1] + Game.MARGIN,
                         "T", size='large')

    def main_logic(self):
        """Выполнение основной логики."""
        f1 = f2 = f3 = f4 = 10
        g = 0

        agent = {'x': self.list_of_points[self.agent_coordinate][0],
                 'y': self.list_of_points[self.agent_coordinate][1]}
        target = {'x': self.list_of_points[self.target_coordinate][0],
                  'y': self.list_of_points[self.target_coordinate][1]}
        obstacles = [
            {'x': self.list_of_points[self.obstacle_number_list[0]][0],
             'y': self.list_of_points[self.obstacle_number_list[0]][1]},
            {'x': self.list_of_points[self.obstacle_number_list[1]][0],
             'y': self.list_of_points[self.obstacle_number_list[1]][1]},
            {'x': self.list_of_points[self.obstacle_number_list[2]][0],
             'y': self.list_of_points[self.obstacle_number_list[2]][1]}
        ]

        print("Координаты точек:")
        while agent['x'] != target['x'] or agent['y'] != target['y']:
            if ((agent['x'] - 1 != obstacles[0]['x']) or (agent['y'] != obstacles[0]['y'])) and (
                    (agent['x'] - 1 != obstacles[1]['x']) or (agent['y'] != obstacles[1]['y'])) and (
                    (agent['x'] - 1 != obstacles[2]['x']) or (agent['y'] != obstacles[2]['y'])) and \
                    Game.OBSTACLE_QUANTITY >= agent['x'] - 1 >= 0:
                f1 = g + abs(agent['x'] - target['x'] - 1) + abs(agent['y'] - target['y'])
            if ((agent['x'] != obstacles[0]['x']) or (agent['y'] - 1 != obstacles[0]['y'])) and (
                    (agent['x'] != obstacles[1]['x']) or (agent['y'] - 1 != obstacles[1]['y'])) and (
                    (agent['x'] != obstacles[2]['x']) or (agent['y'] - 1 != obstacles[2]['y'])) and \
                    Game.OBSTACLE_QUANTITY >= agent['y'] - 1 >= 0:
                f2 = g + abs(agent['x'] - target['x']) + abs(agent['y'] - target['y'] - 1)
            if ((agent['x'] + 1 != obstacles[0]['x']) or (agent['y'] != obstacles[0]['y'])) and (
                    (agent['x'] + 1 != obstacles[1]['x']) or (agent['y'] != obstacles[1]['y'])) and (
                    (agent['x'] + 1 != obstacles[2]['x']) or (agent['y'] != obstacles[2]['y'])) and \
                    Game.OBSTACLE_QUANTITY >= agent['x'] + 1 >= 0:
                f3 = g + abs(agent['x'] - target['x'] + 1) + abs(agent['y'] - target['y'])
            if ((agent['x'] != obstacles[0]['x']) or (agent['y'] + 1 != obstacles[0]['y'])) and (
                    (agent['x'] != obstacles[1]['x']) or (agent['y'] + 1 != obstacles[1]['y'])) and (
                    (agent['x'] != obstacles[2]['x']) or (agent['y'] + 1 != obstacles[2]['y'])) and \
                    Game.OBSTACLE_QUANTITY >= agent['y'] + 1 >= 0:
                f4 = g + abs(agent['x'] - target['x']) + abs(agent['y'] - target['y'] + 1)
            f = min(f1, f2, f3, f4)
            if f1 == f2 == f3 == f4:
                print("Невозможно")
                break
            if f1 > 50 or f2 > 50 or f3 > 50 or f4 > 50:
                print("Невозможно")
                break
            if f == f1:
                x_a_l = agent['x']
                y_a_l = agent['y']
                agent['x'] = agent['x'] - 1
                agent['y'] = agent['y']
            elif f == f2:
                x_a_l = agent['x']
                y_a_l = agent['y']
                agent['x'] = agent['x']
                agent['y'] = agent['y'] - 1
            elif f == f3:
                x_a_l = agent['x']
                y_a_l = agent['y']
                agent['x'] = agent['x'] + 1
                agent['y'] = agent['y']
            elif f == f4:
                x_a_l = agent['x']
                y_a_l = agent['y']
                agent['x'] = agent['x']
                agent['y'] = agent['y'] + 1
            print("x =", agent['x'], "y =", agent['y'])
            plt.text(agent['x'], agent['y'], 'x', color='r', size='large')
            g += 1
            f1 = f2 = f3 = f4 = 50

        plt.show()


if __name__ == '__main__':
    run = Game()
    run.main_logic()
