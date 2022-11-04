# -*- coding: utf-8 -*-
# this is to pre process the bike csv data

import json
import urllib
import math
import pandas as pd 
import matplotlib.pyplot as plt
import os
import folium
import folium.plugins
import matplotlib.pyplot as plt
from selenium import webdriver
import time
from haversine import haversine_vector, Unit
import haversine as hs

from coordtransform import gcj02_to_wgs84

"""
TODO:

1. 文件缺失: `subway_all_lines`, `bus_station` 
2. 函数缺失: `filter_by_origin` 
3. 坐标系: bd09

"""

# keep
def plot_folms(df_ptl_flum, file_name_plt):
    #file_name_plt  without afflix
    # df  Long Lat, radius
    # change_d_p_dis :should be a "raidus" , "demand", "profit", etc.
    colors = {1 : 'red', 0 : 'blue'}
    # WGS84 and EPSG 4326 ()
    # default is 3857
    map_osm = folium.Map(location=[22.605, 114.005], zoom_start=12) #,crs = 'EPSG4326'  # 
     #The latitude of Shenzhen, Guangdong, China is 22.542883, and the longitude is 114.062996

    ### examples of heatmaps
    # df.Enlem=df.Enlem.astype(float)
    # df.Boylam=df.Boylam.astype(float)
    # heat_df=df[["Enlem","Boylam"]]
    # heat_data=list(zip(df.Enlem, df.Boylam))
    # folium.plugins.HeatMap(heat_data).add_to(m)

    # df_ptl_flum.apply(lambda row:folium.Circle(location=[row["Long"],row["Lat"]],
    #                                         radius=row["raidus"],
    #                                         #fill_color=colors[row['Occu']],
    #                                         fill_color='red',
    #                                         fill = True,
    #                                         color = False
    #                                         ).add_to(map_osm), axis=1)
    df_ptl_flum.apply(lambda row:folium.Circle(location = [row["Lat"],row["Long"]],
                                            radius=5,
                                            #radius = row['change_d_p_dis']*1000,
                                            #radius=row[change_d_p_dis]*1000,
                                            fill_color='blue',
                                            fill = True,
                                            color = 'darkblue'
                                            ).add_to(map_osm), axis=1)

    # #map_osm
    # ## add a minimap

    # minimap = folium.plugins.MiniMap()
    # map_osm.add_child(minimap)


    sw = [22.4, 113.3]
    ne = [23.1, 114.7]

    map_osm.fit_bounds([sw, ne]) 
    mapFname = file_name_plt+'.html'
    map_osm.save(mapFname)    

    # ############## here is the save screenshot function  ########################
    # #  here is to save the plot screenshot
    # mapUrl = 'file://{0}/{1}'.format(os.getcwd(), mapFname)

    # #download gecko driver for firefox from here - https://github.com/mozilla/geckodriver/releases
    # #use selenium to save the html as png image
    # driver = webdriver.Firefox(executable_path = 'C:\\Program Files\\Mozilla Firefox\\geckodriver.exe')
    # driver.get(mapUrl)
    # # wait for 5 seconds for the maps and other assets to be loaded in the browser
    # time.sleep(30)
    # driver.save_screenshot(file_name_plt+'.png')
    # driver.quit()

    # ############## screenshot function section ends ########################


def plot_folms_add(df_ptl_flum, change_d_p_dis,file_name_plt):
    #file_name_plt  without afflix
    # df  Long Lat, radius
    # change_d_p_dis :should be a "raidus" , "demand", "profit", etc.
    colors = {1 : 'red', 0 : 'blue'}
    # WGS84 and EPSG 4326 ()
    # default is 3857
    map_osm = folium.Map(location=[22.605, 114.005], zoom_start=12) #,crs = 'EPSG4326'  # 
     #The latitude of Shenzhen, Guangdong, China is 22.542883, and the longitude is 114.062996

    ### examples of heatmaps
    # df.Enlem=df.Enlem.astype(float)
    # df.Boylam=df.Boylam.astype(float)
    # heat_df=df[["Enlem","Boylam"]]
    # heat_data=list(zip(df.Enlem, df.Boylam))
    # folium.plugins.HeatMap(heat_data).add_to(m)

    # df_ptl_flum.apply(lambda row:folium.Circle(location=[row["Long"],row["Lat"]],
    #                                         radius=row["raidus"],
    #                                         #fill_color=colors[row['Occu']],
    #                                         fill_color='red',
    #                                         fill = True,
    #                                         color = False
    #                                         ).add_to(map_osm), axis=1)
    df_ptl_flum.apply(lambda row:folium.Circle(location = [row["Lat"],row["Long"]],
                                            #radius=5,
                                            radius = row[change_d_p_dis],
                                            #radius=row[change_d_p_dis]*1000,
                                            fill_color='blue',
                                            fill = True,
                                            color = 'darkblue'
                                            ).add_to(map_osm), axis=1)

    # #map_osm
    # ## add a minimap

    # minimap = folium.plugins.MiniMap()
    # map_osm.add_child(minimap)


    sw = [22.4, 113.3]
    ne = [23.1, 114.7]

    map_osm.fit_bounds([sw, ne]) 
    mapFname = file_name_plt+'.html'
    map_osm.save(mapFname)    

    # ############## here is the save screenshot function  ########################
    # #  here is to save the plot screenshot
    # mapUrl = 'file://{0}/{1}'.format(os.getcwd(), mapFname)

    # #download gecko driver for firefox from here - https://github.com/mozilla/geckodriver/releases
    # #use selenium to save the html as png image
    # driver = webdriver.Firefox(executable_path = 'C:\\Program Files\\Mozilla Firefox\\geckodriver.exe')
    # driver.get(mapUrl)
    # # wait for 5 seconds for the maps and other assets to be loaded in the browser
    # time.sleep(30)
    # driver.save_screenshot(file_name_plt+'.png')
    # driver.quit()

    # ############## screenshot function section ends ########################


if __name__ == '__main__':

    script_dir = os.path.dirname(__file__)
    csv_dir = os.path.join(script_dir, 'csv_04\\')# single vehicle trajectory
    des_dir = os.path.join(script_dir, 'temp1\\')# single vehicle trajectory

    # subways
    df = pd.read_csv("subway_all_lines.csv",usecols=['lat','long','station'],encoding='utf-8',sep='\t')
    # FIXME
    df['lon_1']= df[['long','lat']].apply(lambda x: gcj02_to_wgs84(*x)[0], axis=1)
    df['lat_1']= df[['long','lat']].apply(lambda x: gcj02_to_wgs84(*x)[1], axis=1)
    # rename lat long to Lat Long
    df = df.rename(columns={'lat_1': 'Lat', 'lon_1': 'Long'})
    # drop duplicate stations
    df_sub = df.drop_duplicates()#(keep = False, inplace = True)
    df_sub = df_sub.reset_index()
    df_sub.to_csv("subway_lines_drop_duplicates.csv",encoding='utf-8')
    plot_folms(df,'subway_folm_plt')


    # # plot the bus stations in maps 
    # df = pd.read_csv("bus_station.csv",usecols=['lat','lon'],encoding='unicode_escape')
    # df['lon_1']= df[['lon','lat']].apply(lambda x: gcj02_to_wgs84(*x)[0], axis=1)
    # df['lat_1']= df[['lon','lat']].apply(lambda x: gcj02_to_wgs84(*x)[1], axis=1)
    # #print (df.describe())
    # # rename lat long to Lat Long
    # df = df.rename(columns={'lat_1': 'Lat', 'lon_1': 'Long'})
    # plot_folms(df,'bus_folm_plt')

    # plt the data around subway station 
    # calcaulting the time differences 
    a_bus_percentge_list=[]
    bus_top_10_list_start=[]
    bus_top_30_list_start=[]


    bus_top_10_list_end=[]
    bus_top_30_list_end=[]

    # for a month in a folder
    for i in range(1,31):
        if i<10:
            date_i= str(0)+str(i)
        else:
            date_i=str(i)
        print ("Now we are processing 04-"+ date_i+"data!")

        df1 = pd.read_csv(csv_dir+"2021-04-"+date_i+".csv")  #,nrows = 1000
        df1['lon_s']= df1[['START_LNG','START_LAT']].apply(lambda x: gcj02_to_wgs84(*x)[0], axis=1)
        df1['lat_s']= df1[['START_LNG','START_LAT']].apply(lambda x: gcj02_to_wgs84(*x)[1], axis=1)
        df1['lon_e']= df1[['END_LNG','END_LAT']].apply(lambda x: gcj02_to_wgs84(*x)[0], axis=1)
        df1['lat_e']= df1[['END_LNG','END_LAT']].apply(lambda x: gcj02_to_wgs84(*x)[1], axis=1)
        # rename lat long of start and end 
        df = df.rename(columns={'lon_s': 'START_LNG', 'lat_s': 'START_LAT','lon_e': 'END_LNG', 'lat_e': 'END_LAT'})
        df1.START_TIME = pd.to_datetime(df1.START_TIME)
        df1.END_TIME= pd.to_datetime(df1.END_TIME)
        df1['tot_mins_diff'] = (df1.END_TIME-df1.START_TIME) / pd.Timedelta(minutes=1)

        
        total = df1['USER_ID'].count()
        print ("Total number of day"+date_i+" total trip number is",total)
        #print (df1['USER_ID'].count())

        # dropping the  time values < 0, or > 60 mins 
        df1.drop(df1[(df1['tot_mins_diff'] <0) | (df1['tot_mins_diff'] > 60)].index, inplace=True)
        # only trips inside boundaries
        df1.drop(df1[(df1['START_LNG'] <113) | (df1['START_LNG'] > 114.617)].index, inplace=True)
        df1.drop(df1[(df1['START_LAT'] <22.45) | (df1['START_LAT'] > 23.1)].index, inplace=True)
        df1.drop(df1[(df1['END_LNG'] <113) | (df1['END_LNG'] > 114.617)].index, inplace=True)
        df1.drop(df1[(df1['END_LAT'] <22.45) | (df1['END_LAT'] > 23.1)].index, inplace=True)


        # distance--using haversine, although the 100-300 m won't make too much differneces  
        df1['distance'] = df1.apply(lambda x: hs.haversine((x.START_LAT, x.START_LNG),(x.END_LAT,x.END_LNG)), axis=1) # unit: km
        # if dis>5, not likely to cmmute to stations,just delete those trips
        df1.drop(df1[(df1['distance'] >5)].index, inplace=True)
        print ("Here we finished the filtering process!")
        a_bus_percentge_list.append(df1['distance'].count()/total)
        print (df1['distance'].count()/total)

        df_sub['region_sub'] = df_sub.index # total 283 stations  # should from 0 to 283, thus, 0, 1, 2, ------  282
        #print ("check here the maxim!!")  # 0-235, total 
        #print (df_sub.describe())
        df_sub['raidus'] =0.15 #  300 m is now testing 


        ### IMPORTANT  for start, it id for the last mile, thus the start time is used
        df_start = df1[['START_LNG','START_LAT','START_TIME']]  
        df_start = df_start.rename(columns={'START_LNG':'Long',"START_LAT":'Lat'})
        pick_up_reg = filter_by_origin(df_start,df_sub)
        pick_up_reg.to_csv(des_dir+"Region_start_"+date_i+".csv",encoding='utf_8_sig')
        
        times = pd.to_datetime(pick_up_reg.START_TIME)
        dfff_sum = pick_up_reg.groupby(['Region',times.dt.hour]).Long.count()
        dfff_sum.to_csv(des_dir+"Region_start_hour_"+date_i+".csv",encoding='utf_8_sig')
        dfff_sum = pd.read_csv("Region_start_hour_"+date_i+".csv",encoding='utf_8_sig')
        print (dfff_sum.head())
        dfff_sum = dfff_sum.rename(columns={'Long':'demand_p'})  #  this is very uneasy....
        
        print ("The start from subway percentage is") 
        print (dfff_sum['demand_p'].sum()/(df1['USER_ID'].count()))
        dfff_sum.to_csv(des_dir+"start_from_subway_0_1"+date_i+".csv",encoding='utf_8_sig')  # 先单车后换成subway
        dfff_sum = dfff_sum.reset_index()
        df_sub_start_count = dfff_sum.merge(df_sub,how ="left", left_on='Region', right_on='region_sub')
        
        print ("The start from subway top 10 percentage is")
        bus_top_10_list_start.append(dfff_sum.nlargest(10, 'demand_p')['demand_p'].sum()/(dfff_sum['demand_p'].sum()))
        
        print (dfff_sum.nlargest(10, 'demand_p')['demand_p'].sum()/(dfff_sum['demand_p'].sum()))
        bus_top_30_list_start.append(dfff_sum.nlargest(30, 'demand_p')['demand_p'].sum()/(dfff_sum['demand_p'].sum()))
        
        print ("The start from subway top 30 percentage is")
        print (dfff_sum.nlargest(30, 'demand_p')['demand_p'].sum()/(dfff_sum['demand_p'].sum()))
        df_sub_start_count.to_csv(des_dir+"df_sub_start_count_04"+date_i+".csv",encoding='utf_8_sig')
        df_sub_start_count.nlargest(30, 'demand_p').to_csv(des_dir+"df_sub_start_count_04"+date_i+"_30.csv",encoding='utf_8_sig')
        plot_folms_add(df_sub_start_count,'demand_p','subway_folm_plt_count'+date_i)

        ### IMPORTANT  for end, it id for the first mile, thus the end time is used
        df_end = df1[['END_LNG','END_LAT','END_TIME']]
        df_end = df_end.rename(columns={'END_LNG':'Long',"END_LAT":'Lat'})
        drop_off_reg = filter_by_origin(df_end,df_sub)
        drop_off_reg.to_csv(des_dir+"Region_end_"+date_i+".csv",encoding='utf_8_sig')
        times = pd.to_datetime(drop_off_reg.END_TIME)
        dfff_sum_2 = drop_off_reg.groupby(['Region',times.dt.hour]).Long.count()
        dfff_sum_2.to_csv(des_dir+"Region_end_hour_"+date_i+".csv",encoding='utf_8_sig')
        dfff_sum_2 = pd.read_csv("Region_end_hour_"+date_i+".csv",encoding='utf_8_sig')
        #print (dfff_sum_2.head())
        dfff_sum_2 = dfff_sum_2.rename(columns={'Long':'demand_d'})
        print ("The end to subway percentage is") 
        print (dfff_sum_2['demand_d'].sum()/(df1['USER_ID'].count()))
        dfff_sum_2.to_csv(des_dir+"drop_to_subway_0_1"+date_i+".csv") # 先subway后换成单车
        dfff_sum_2 = dfff_sum_2.reset_index()
        df_sub_end_count = dfff_sum_2.merge(df_sub,how ="left", left_on='Region', right_on='region_sub')#,suffixes=('_subway', '_count')
        print ("The end to subway top 10 percentage is")
        bus_top_10_list_end.append(dfff_sum_2.nlargest(10, 'demand_d')['demand_d'].sum()/(dfff_sum_2['demand_d'].sum()))
        print (dfff_sum_2.nlargest(10, 'demand_d')['demand_d'].sum()/(dfff_sum_2['demand_d'].sum()))
        print ("The end to subway top 30 percentage is")
        bus_top_30_list_end.append(dfff_sum_2.nlargest(30, 'demand_d')['demand_d'].sum()/(dfff_sum_2['demand_d'].sum()))
        print (dfff_sum_2.nlargest(30, 'demand_d')['demand_d'].sum()/(dfff_sum_2['demand_d'].sum()))
        df_sub_end_count.to_csv(des_dir+"df_sub_end_count_04"+date_i+".csv",encoding='utf_8_sig')
        df_sub_end_count.nlargest(30, 'demand_d').to_csv(des_dir+"df_sub_end_count_04"+date_i+"_30.csv",encoding='utf_8_sig')
        plot_folms_add(df_sub_end_count,'demand_d','subway_folm_plt_count_end'+date_i)



    print (a_bus_percentge_list)
    print (bus_top_10_list_start)
    print (bus_top_30_list_start)


    print (bus_top_10_list_end)
    print (bus_top_30_list_end)