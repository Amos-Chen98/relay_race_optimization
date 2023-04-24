# relay_race_optimization

5个人接力跑1小时，如何分配每人跑的距离，使总距离最长？这个仓库给出了一种解决方案。

## 背景

规则：每队5人进行接力，比赛时间固定为60分钟，在规定时间内跑过总距离最长的队伍获胜。每人只能接力一棒，不限制每人接力距离。

## 方法

首先，对于每名运动员，基于其历史训练数据（即一系列（距离-时间）数据点），采用分段三次多项式曲线，插值得到一条“距离-时间”曲线，其作用是估计这名运动员在时间t内能跑动的距离f(t)。

随后，构建一个约束优化问题：自变量为每名运动员跑动的时间，目标为最小化所有运动员跑动距离之和的相反数，约束是每名运动员跑动时间之和为60分钟。使用[scipy.optimize.minimize()](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.minimize.html#scipy.optimize.minimize)中的SLSQP求解器求解即可得到最优的时间（距离）分配。

## 如何使用代码

在`main.py`中，参考代码注释，按预设格式输入每名运动员的历史训练数据（每名运动员的数据点数量不必相同），直接运行即可查看结果。比赛总时间可以通过`total_time`这一参数修改。

例如，参考丹尼尔斯跑力表选取跑力不同的5名运动员，其成绩如下：

```Python
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
```

计算结果为：

```
Player 1 runs for 403 m at pace 04:05, expected time 01:39
Player 2 runs for 908 m at pace 03:59, expected time 03:37
Player 3 runs for 1506 m at pace 03:52, expected time 05:50
Player 4 runs for 2281 m at pace 03:48, expected time 08:40
Player 5 runs for 10052 m at pace 03:59, expected time 40:12
Expected total distance: 15151 m
```

## 局限性

该解决方案最大的局限性在于每名运动员的“距离-时间”曲线仅由统计方法得出，属于非常粗略的估计，存在较大误差，特别是短距离的估计不准确。更多输入数据可能带来更好的结果。

