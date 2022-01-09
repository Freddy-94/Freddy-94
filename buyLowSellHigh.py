# -*- coding: utf-8 -*-
"""
Created on Sat Jan  8 21:24:06 2022

@author: alfre
"""

from pandas_datareader import data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# First day
start_date = '2021-01-01'
# Last day
end_date = '2021-10-21'
# Call the function DataReader from the class data
goog_data = data.DataReader('GOOG', 'yahoo', start_date, end_date)

# Panda dataframe having the same dimension as the dataframe containing data
goog_data_signal = pd.DataFrame(index=goog_data.index)

goog_data_signal['price'] = goog_data['Adj Close']
goog_data_signal['daily_difference'] = goog_data_signal['price'].diff()

# signal based on the values of column daily_difference
# if the value is positive, we give the value 1, otherwise, remain 0:
goog_data_signal['signal'] = 0.0
goog_data_signal['signal'][:] = np.where(goog_data_signal['daily_difference'][:] > 0, 1.0, 0.0)

# Since we don't want to constantly buy if the market keeps moving down, or
# constantly sell when the market is moving up, we will limit the number of orders
# by restricting ourselves to the number of positions on the market. The position is
# your inventory of stocks or assets that you have on the market. For instance, if
# you buy one Google share, this means you have a position of one share on the
# market. If you sell this share, you will not have any positions on the market
# To simplify our example and limit the position on the market, it will be impossible
# to buy or sell more than one time consecutively. Therefore, we will apply diff() to
# the column signal:
# goog_data_signal['positions'] = goog_data_signal['signal'].diff()
# price daily_difference signal positions
# Date
# 2014-01-02 552.963501 NaN 0.0 NaN
# 2014-01-03 548.929749 -4.033752 0.0 0.0
# 2014-01-06 555.049927 6.120178 1.0 1.0
# 2014-01-07 565.750366 10.700439 1.0 0.0
# 2014-01-08 566.927673 1.177307 1.0 0.0
# 2014-01-09 561.468201 -5.459473 0.0 -1.0
# 2014-01-10 561.438354 -0.029846 0.0 0.0
# 2014-01-13 557.861633 -3.576721 0.0 0.0
# We will buy a share of Google on January 6 for a price of 555.049927, and then sell
# this share for a price of 561.468201. The profit of this trade is 561.468201-
# 555.049927=6.418274.

goog_data_signal['positions'] = goog_data_signal['signal'].diff()

print(goog_data_signal.head())

#definition of a figure that will contain our chart
fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Google price in $')

# plot the price within the range of days we initially chose
goog_data_signal['price'].plot(ax=ax1, color='r', lw=2.)

# Next, we draw an up arrow when we buy one Google share
ax1.plot(goog_data_signal.loc[goog_data_signal.positions == 1.0].index,
         goog_data_signal.price[goog_data_signal.positions == 1.0],
         '^', markersize=5, color='m')

# And draw a down arrow when we sell one Google share
ax1.plot(goog_data_signal.loc[goog_data_signal.positions == -1.0].index,
         goog_data_signal.price[goog_data_signal.positions == -1.0],
         'v', markersize=5, color='k')

plt.show()

# Backtesting

# Set the initial capital
initial_capital= float(1000.0)

# creation of a data frame for the positions and the portfolio
positions = pd.DataFrame(index=goog_data_signal.index).fillna(0.0)
portfolio = pd.DataFrame(index=goog_data_signal.index).fillna(0.0)

# store GOOG positions in the following data frame:
positions['GOOG'] = goog_data_signal['signal']

# store the amount of the GOOG positions for the portfolio
portfolio['positions'] = (positions.multiply(goog_data_signal['price'], axis=0))

# calculate the non-invested money (cash):
portfolio['cash'] = initial_capital - (positions.diff().multiply(goog_data_signal['price'], axis=0)).cumsum()

# The total investment will be calculated by summing the positions and the cash:
portfolio['total'] = portfolio['positions'] + portfolio['cash']
portfolio.plot()
plt.show()


fig = plt.figure()
ax1 = fig.add_subplot(111, ylabel='Portfolio value in $')
portfolio['total'].plot(ax=ax1, lw=2.)
ax1.plot(portfolio.loc[goog_data_signal.positions == 1.0].index,portfolio.total[goog_data_signal.positions == 1.0],'^', markersize=10, color='m')
ax1.plot(portfolio.loc[goog_data_signal.positions == -1.0].index,portfolio.total[goog_data_signal.positions == -1.0],'v', markersize=10, color='k')
plt.show()
