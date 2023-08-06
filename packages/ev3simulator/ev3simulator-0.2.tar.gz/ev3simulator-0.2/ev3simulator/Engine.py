#!/usr/bin/python3
import time
import math


class LargeMotor:
    U = 0
    I = 0
    w = 0
    position = 0
    dU = 0
    time_sleep = 0.0001
    L = 0.0047
    km = 0.318
    J = 0.00247
    ke = 0.318
    R = 8.21
    pre_time = time.time()
    start_time = time.time()

    def __init__(self, name):
        self.name = name

    def set_time_sleep(self, time_sleep):
        if (time_sleep < 0.0001):
            self.time_sleep = time_sleep

    def run_direct(self, duty_cycle_sp):
        self.U = duty_cycle_sp * 8 / 100 - self.dU
        self.rotate()
        time.sleep(self.time_sleep)  # min 0.0001

    def rotate(self):
        self.I += self.U * self.dt() / self.L
        self.w += self.I * self.km * self.dt() / self.J
        self.position += self.w * self.dt()
        self.dU = self.w * self.ke + self.I * self.R
        self.pre_time = time.time()

    def stop(self, stop_action):
        if stop_action == "stop":
            self.U = 0
            self.w = 0
            self.position = 0
            self.dU = 0

    def dt(self):
        dt = time.time() - self.pre_time
        return dt


class UltrasonicSensor:
    x = 0
    y = 0
    angle = 0
    x1 = 0
    y1 = 0
    x2 = 0
    y2 = 0
    y_wall_start = []
    x_wall_start = []
    y_wall_finish = []
    x_wall_finish = []

    def __init__(self, name, angle):
        self.name = name
        self.angle = angle

    def add_wall(self, x_start, y_start, x_finish, y_finish):
        self.x_wall_start.append(x_start)
        self.y_wall_start.append(y_start)
        self.x_wall_finish.append(x_finish)
        self.y_wall_finish.append(y_finish)

    def value(self, x3, y3, alpha):
        answer = []
        alpha += self.angle
        for i in range(0, self.x_wall_start.__len__(), 1):
            self.x1 = self.x_wall_start[i]
            self.y1 = self.y_wall_start[i]
            self.x2 = self.x_wall_finish[i]
            self.y2 = self.y_wall_finish[i]

            x = (-self.x1 * (self.y1 - self.y2) / (self.x1 - self.x2) * 1/math.tan(math.radians(alpha)) + self.y1 *
                 1/math.tan(math.radians(alpha)) -
                 y3 * 1/math.tan(math.radians(alpha)) + x3) / (1 - (self.y1 -
                self.y2)/(self.x1 - self.x2) * 1/math.tan(math.radians(alpha)))
            y = (x - self.x1)*(self.y1 - self.y2)/(self.x1 - self.x2) + self.y1
            r = math.hypot(x3 - x, y3 - y)

            y_max = max(self.y1, self.y2)
            x_max = max(self.x1, self.x2)
            y_min = min(self.y1, self.y2)
            x_min = min(self.x1, self.x2)

            if y <= y_max and y >= y_min and x <= x_max and x >= x_min and (alpha > 0 and alpha < 180 and y > y3 or alpha > 180 and alpha < 360 and y < y3):
                answer.append(r)
        if answer.__len__() > 0:
            return min(answer)
        else:
            return 200

