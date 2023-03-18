#!/bin/bash
import sys

from center_system import CenterSystem

controlData = {
    'initSpeed': 6.0784,
    'toleranceToward': 0.1,
    'towardSpeedAlpha': 3.5513,
    'towardSpeedBeta': -1.2969,
    'boomTowardSpeedAlpha': 2.8,
    'boomTowardSpeedBeta': -0.3,
    'sumDistanceA': 1,
    'sumDistanceB': 1,

    'weightDistance': 0,
    'boomDistance': 2.954,
    'slowSpeed': 4.3967,
    'sellDistanceA': 6.0784,
    'sellDistanceB': 1.255,

    'nearDecri': 1,
    'theTimeStopBuy': 8850, # <9000
}

if __name__ == '__main__':
    CS = CenterSystem()
    CS.initControlData(controlData)
    CS.getMapData()
    for _ in range(9000):
        if CS.getGameData():
            CS.beforeCenterComputerFunction()
            CS.CenterComputerFunction()
            CS.afterCenterComputerFunction()

            CS.setCarsAction()
            CS.putCommandToSys()
        else:
            break
