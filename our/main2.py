#!/bin/bash
import argparse
import sys

from center_system import CenterSystem

parser = argparse.ArgumentParser(description="PyTorch Data_Pre")
parser.add_argument("--towardSpeedAlpha", default=2.8, type=float, help="train root path")
parser.add_argument("--towardSpeedBeta", default=-0.3, type=float, help="test root path")
parser.add_argument("--boomDistance", default=2.6,  type=float, help="use cuda?")
parser.add_argument("--slowSpeed", default=3.5, type=float, help="use cuda?")
parser.add_argument("--initSpeed", default=6.8, type=float, help="use cuda?")
parser.add_argument("--sellDistanceB", default=8, type=float, help="use cuda?")
opt = parser.parse_args()

controlData = {
    'initSpeed': opt.initSpeed, #6.8
    'toleranceToward': 0.1,
    'towardSpeedAlpha': opt.towardSpeedAlpha, #2.8,
    'towardSpeedBeta': opt.towardSpeedBeta, #-0.3,
    'boomTowardSpeedAlpha': opt.towardSpeedAlpha, #2.8,
    'boomTowardSpeedBeta': opt.towardSpeedBeta, #-0.3,
    'sumDistanceA': 1,
    'sumDistanceB': 1,

    'weightDistance': 0,
    'boomDistance': opt.boomDistance, #2.6,
    'slowSpeed': opt.slowSpeed, #3.5,
    'sellDistanceA': opt.initSpeed, #6.8,
    'sellDistanceB': opt.sellDistanceB, #8,

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
