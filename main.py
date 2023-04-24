'''
Author: Yicheng Chen (yicheng-chen@outlook.com)
LastEditTime: 2023-04-24 17:45:40
'''
import numpy as np
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
from scipy.optimize import minimize


# 5 players' historical running data, time in mins.secs(e.g. 12:45 -> 12.45), distance in meters
player_time = [None]*5
player_dis = [None]*5

player_time[0] = [6.35, 14.03, 24.08, 50.03, 110.59]
player_dis[0] = [1500, 3000, 5000, 10000, 21097.5]

player_time[1] = [6.11, 13.11, 22.41, 47.07, 104.20]
player_dis[1] = [1500, 3000, 5000, 10000, 21097.5]


player_time[2] = [5.49, 12.26, 21.25, 44.25, 98.27]
player_dis[2] = [1500, 3000, 5000, 10000, 21097.5]


player_time[3] = [5.30, 11.45, 20.18, 42.04, 93.12]
player_dis[3] = [1500, 3000, 5000, 10000, 21097.5]

player_time[4] = [5.13, 11.09, 19.17, 39.59, 88.31]
player_dis[4] = [1500, 3000, 5000, 10000, 21097.5]


for i in range(len(player_time)):
    for j in range(len(player_time[i])):
        min = int(player_time[i][j])
        sec = int((player_time[i][j] - min) * 100)
        player_time[i][j] = min * 60 + sec


class RelayOptimizer:
    def __init__(self, player_time, player_dis):
        self.player_num = len(player_time)
        self.total_time = 3600  # 1 hour
        self.bounds = [(0, self.total_time) for _ in range(self.player_num)]
        self.cs = [None]*self.player_num  # CubicSpline
        for i in range(self.player_num):
            player_time[i].insert(0, 0)
            player_dis[i].insert(0, 0)
            self.cs[i] = CubicSpline(player_time[i], player_dis[i])

    def objective(self, x):
        return -sum(self.cs[i](x[i]) for i in range(self.player_num))

    def constraint(self, x):
        return sum(x) - self.total_time

    def optimize(self):
        x = self.total_time/self.player_num*np.ones(self.player_num)
        res = minimize(self.objective, x, method='SLSQP', bounds=self.bounds, constraints={'type': 'eq', 'fun': self.constraint})
        for i in range(self.player_num):
            dis = self.cs[i](res.x[i])
            time_min = int(res.x[i] / 60)
            time_sec = int(res.x[i] % 60)
            if dis < 1e-3:
                pace_min = 0
                pace_sec = 0
            else:
                pace = res.x[i]/dis*1000  # sec/km
                pace_min = int(pace / 60)
                pace_sec = int(pace % 60)
            print("Player %d runs for %d m at pace %02d:%02d, expected time %02d:%02d" % (i+1, dis, pace_min, pace_sec, time_min, time_sec))
        print("Expected total distance: %d m" % (-self.objective(res.x)))
        self.res = res

    def plot_pace_curve(self):
        duration = np.linspace(1, self.total_time, 1000)
        for i in range(self.player_num):
            dis = self.cs[i](duration)  # m
            pace = duration/dis*1000  # sec/km
            expected_dis = self.cs[i](self.res.x[i])
            expected_pace = self.res.x[i]/expected_dis*1000
            plt.plot(dis, pace, label="Player %d" % (i+1))
            plt.scatter(expected_dis, expected_pace, marker='o', color='red', s=30)
        plt.legend()
        plt.xlabel("Distance (m)")
        plt.ylabel("Pace (sec/km)")
        plt.title("Pace Curve")
        plt.grid()
        plt.show()


if __name__ == '__main__':
    ro = RelayOptimizer(player_time, player_dis)
    ro.optimize()
    ro.plot_pace_curve()
