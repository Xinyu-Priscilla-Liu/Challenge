# -*- coding: utf-8 -*-
"""
Created on Sun Oct 29 14:23:03 2017

@author: Owner
"""

# -*- coding: utf-8 -*-
"""
Created on Sun Mar 26 14:36:23 2017

@author: Xinyu
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os as os
import matplotlib.gridspec as gridspec

from mpl_toolkits.basemap import Basemap as Basemap
from matplotlib.colors import rgb2hex
from matplotlib.patches import Polygon


ghg2011 = pd.read_excel('ghgp_data_2011-final-8-18-14.xlsx', skiprows = 3, sheetname=0, 
                        parse_cols= 'E,F,H,I,J,K,M,O',
                        names = ['State','Zip Code','County', 'Latitude','Longitude',
                   'Primary NAICS Code','Industry Type (sectors)','CO2 emissions (metric tons CO2)'])

ghg2012 = pd.read_excel('ghgp_data_2012-final-8-18-14.xlsx', skiprows = 3, sheetname=0, 
                        parse_cols= 'E,F,H,I,J,K,M,O',
                        names = ['State','Zip Code','County', 'Latitude','Longitude',
                   'Primary NAICS Code','Industry Type (sectors)','CO2 emissions (metric tons CO2)'])

ghg2013 = pd.read_excel('ghgp_data_2013-final-8-18-14.xlsx', skiprows = 3, sheetname=0, 
                        parse_cols= 'E,F,H,I,J,K,M,O',
                        names = ['State','Zip Code','County', 'Latitude','Longitude',
                   'Primary NAICS Code','Industry Type (sectors)','CO2 emissions (metric tons CO2)'])

ghg2014 = pd.read_excel('ghgp_data_2014_0.xlsx', skiprows = 3, sheetname=0, 
                        parse_cols= 'E,F,H,I,J,K,M,O',
                        names = ['State','Zip Code','County', 'Latitude','Longitude',
                   'Primary NAICS Code','Industry Type (sectors)','CO2 emissions (metric tons CO2)'])

# For Ohio
# Unit million metric tons of CO2
Transportation = pd.read_excel('state\\ohio.xlsx', skiprows = 25,skip_footer = 14, sheetname = 0,
                               parse_cols = 'AH,AI,AJ,AK',
                               names = ['2011','2012','2013','2014'])
# Unit metric tons of CO2
Transportation = Transportation.apply(lambda x: x*1000000, axis = 1)

# Filter ghg data for the state of ohio
ghg2011 = ghg2011[ghg2011['State'] == 'OH']
ghg2011 = ghg2011[(ghg2011['Industry Type (sectors)'] == 'Power Plants') | (ghg2011['Industry Type (sectors)'] == 'Petroleum and Natural Gas Systems') | (ghg2011['Industry Type (sectors)'] == 'Chemicals') | (ghg2011['Industry Type (sectors)'] == 'Metals')| (ghg2011['Industry Type (sectors)'] == 'Minerals')]
ghg2011 = ghg2011.dropna()
ghg2011.reset_index()

ghg2012 = ghg2012[ghg2012['State'] == 'OH']
ghg2012 = ghg2012[(ghg2012['Industry Type (sectors)'] == 'Power Plants') | (ghg2012['Industry Type (sectors)'] == 'Petroleum and Natural Gas Systems') |  (ghg2012['Industry Type (sectors)'] == 'Chemicals') | (ghg2012['Industry Type (sectors)'] == 'Metals')| (ghg2012['Industry Type (sectors)'] == 'Minerals')]
ghg2012 = ghg2012.dropna()
ghg2012.reset_index()

ghg2013 = ghg2013[ghg2013['State'] == 'OH']
ghg2013 = ghg2013[(ghg2013['Industry Type (sectors)'] == 'Power Plants') | (ghg2013['Industry Type (sectors)'] == 'Petroleum and Natural Gas Systems') | (ghg2013['Industry Type (sectors)'] == 'Chemicals') | (ghg2013['Industry Type (sectors)'] == 'Metals')| (ghg2013['Industry Type (sectors)'] == 'Minerals')]
ghg2013 = ghg2013.dropna()
ghg2013.reset_index()

ghg2014 = ghg2014[ghg2014['State'] == 'OH']
ghg2014 = ghg2014[(ghg2014['Industry Type (sectors)'] == 'Power Plants') | (ghg2014['Industry Type (sectors)'] == 'Petroleum and Natural Gas Systems') | (ghg2014['Industry Type (sectors)'] == 'Chemicals') | (ghg2014['Industry Type (sectors)'] == 'Metals')| (ghg2014['Industry Type (sectors)'] == 'Minerals')]
ghg2014 = ghg2014.dropna()
ghg2014.reset_index()


# find the emissions from different sectors in the state of ohio

dic_2011 = {}
for group, frame in ghg2011.groupby('Industry Type (sectors)'):
    Total_CO2_Emission_2011 = np.sum(frame['CO2 emissions (metric tons CO2)'])
    dic_2011[group] = Total_CO2_Emission_2011
    
dic_2012 = {}
for group, frame in ghg2012.groupby('Industry Type (sectors)'):
    Total_CO2_Emission_2012 = np.sum(frame['CO2 emissions (metric tons CO2)'])
    dic_2012[group] = Total_CO2_Emission_2012
    
dic_2013 = {}
for group, frame in ghg2013.groupby('Industry Type (sectors)'):
    Total_CO2_Emission_2013 = np.sum(frame['CO2 emissions (metric tons CO2)'])
    dic_2013[group] = Total_CO2_Emission_2013
    
dic_2014 = {}
for group, frame in ghg2014.groupby('Industry Type (sectors)'):
    Total_CO2_Emission_2014 = np.sum(frame['CO2 emissions (metric tons CO2)'])
    dic_2014[group] = Total_CO2_Emission_2014
    
# put the information together
df = pd.DataFrame([dic_2011, dic_2012, dic_2013, dic_2014], index = ['2011','2012','2013','2014'])

# add transportation to df
Transportation = Transportation.T
df['Transportation'] = Transportation[0]

df['Petroleum and Chemicals'] = df['Chemicals'] + df['Metals'] + df['Minerals'] + df['Petroleum and Natural Gas Systems']

columns_to_keep = ['Power Plants', 'Transportation', 'Petroleum and Chemicals']
df = df[columns_to_keep]


# use gridspec to partition the figure into subplots
plt.figure()
gspec = gridspec.GridSpec(5, 4)

# creating subplots, all indicing starts from 0, save them to axis
total = plt.subplot(gspec[0, :])
Carbon2011 = plt.subplot(gspec[1:3,0:2])
Carbon2012 = plt.subplot(gspec[1:3,2:4])
Carbon2013 = plt.subplot(gspec[3:5,0:2])
Carbon2014 = plt.subplot(gspec[3:5,2:4])

# total plot
a = np.array([1,2,3,4])
total.plot(a, df['Power Plants'] + df['Transportation']+df['Petroleum and Chemicals'], '-o', color = 'black')

total.set_xlim([0.5,4.5])
total.set_ylim([160000000,190000000])
total.locator_params(nbins=5, axis='x')
total.set_xticklabels(('', '2011', '2012', '2013', '2014', ''))
total.set_title('Total CO$_2$ Emission in Ohio (Metric Tons)')

# reduce the number of tickers in the figure
total.locator_params(nbins=5, axis='x')
total.locator_params(nbins=3, axis='y')
# remove all the ticks (both axes), and tick labels on the Y axis
total.tick_params(top='off', bottom='off', left='off', right='off')
total.grid()

# remove the frame of the chart
for spine in total.spines.values():
    spine.set_visible(False)

# pie chart 
labels = 'Power Plants','Transportation','Petroleum and Chemicals'
explode = (0, 0, 0)  # only "explode" the 2nd slice (i.e. 'Hogs')
colors = ['yellowgreen', 'lightcoral', 'lightskyblue']

size2011 = df.loc['2011']
Carbon2011.pie(size2011, explode=explode, autopct='%1.1f%%', shadow=True, colors = colors)
Carbon2011.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
Carbon2011.yaxis.set_label_position("left")
Carbon2011.set_ylabel('Year: 2011')

size2012 = df.loc['2012']
Carbon2012.pie(size2012, explode=explode, autopct='%1.1f%%', shadow=True, colors = colors)
Carbon2012.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
Carbon2012.yaxis.set_label_position("right")
Carbon2012.set_ylabel('Year: 2012')

size2013 = df.loc['2013']
Carbon2013.pie(size2013, explode=explode, autopct='%1.1f%%', shadow=True, colors = colors)
Carbon2013.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
Carbon2013.yaxis.set_label_position("left")
Carbon2013.set_ylabel('Year: 2013')

size2014 = df.loc['2014']
Carbon2014.pie(size2014, explode=explode, autopct='%1.1f%%', shadow=True, colors = colors)
Carbon2014.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
Carbon2014.yaxis.set_label_position("right")
Carbon2014.set_ylabel('Year: 2014')

# Add label
labels = ('Power Plant', 'Transportation', 'Chemicals')
plt.legend(labels, loc=(-0.32, 0.9),labelspacing=0.1, fontsize='small', frameon=False)
plt.show()

directory = 'state'

state_total = {}

frame = pd.DataFrame()
list_ = []
    
for root,dirs,files in os.walk(directory):
    for file in files:
       if file.endswith(".xlsx"):
           state = file.split('.')[0].title()
           emission = pd.read_excel(''.join([directory, '\\',file]), skiprows = 39, sheetname = 0,
                               parse_cols = 'AH,AI,AJ,AK',
                               names = ['2011','2012','2013','2014'])
           emission['state'] = state
           list_.append(emission)
           frame = pd.concat(list_)
           
frame['2014_to_2011'] = frame['2014']/frame['2011']

emission_ratio_2014_2011 = pd.Series(frame['2014_to_2011'].values,index=frame['state']).to_dict()     

# Lambert Conformal map of lower 48 states.
m = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
            projection='lcc',lat_1=33,lat_2=45,lon_0=-95)

shp_info = m.readshapefile('st99_d00','states',drawbounds=True)

# choose a color for each state based on population density.
colors={}
statenames=[]
cmap = plt.cm.bwr_r

vmin = min(frame['2014_to_2011'].values)
vmax = max(frame['2014_to_2011'].values) # set range.

for shapedict in m.states_info:
    statename = shapedict['NAME']
    # skip DC and Puerto Rico.
    if statename not in ['District of Columbia','Puerto Rico']:
        state_emission_ratio = emission_ratio_2014_2011[statename]
        # calling colormap with value between 0 and 1 returns
        # rgba value.  Invert color range (hot colors are high
        # population), take sqrt root to spread out colors more.
        colors[statename] = cmap(1.-np.sqrt((state_emission_ratio-vmin)/(vmax-vmin)))[:3]
    statenames.append(statename)


import matplotlib as mpl
fig, ax = plt.subplots(figsize=(12,6))
for nshape,seg in enumerate(m.states):
    if statenames[nshape] not in ['District of Columbia','Puerto Rico']:
        color = rgb2hex(colors[statenames[nshape]]) 
        poly = Polygon(seg,facecolor=color,edgecolor=color)
        ax.add_patch(poly)
# draw meridians and parallels.
m.drawparallels(np.arange(25,65,20),labels=[1,0,0,0])
m.drawmeridians(np.arange(-120,-40,20),labels=[0,0,0,1])
plt.title('Ratio of CO2 Emission (Year 2014/Year 2011)')


cax = fig.add_axes([0.82, 0.2, 0.02, 0.6])
cb = mpl.colorbar.ColorbarBase(cax, cmap=cmap, spacing='proportional')
plt.show()
