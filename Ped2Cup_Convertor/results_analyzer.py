from collections import OrderedDict

_Author_ = "Karthik Vaidhyanathan"

# Analyze the results generated from the simulation
import  pandas as pd
import os
from Initalizer import Initialize
import json
import plotly.graph_objects as go
import statistics
import math
import numpy as np
from plotly.subplots import make_subplots

init_object = Initialize()

def calculate_energy_consumption(aggregated_csv_filename):
    # Get the aggregated csv file containing the energy consumed by the senosrs and cacluate the energy consumed
    energy_list = []
    df_energy_consumption = pd.read_csv(aggregated_csv_filename, sep=",",
                         index_col="timestamp")  # Read the proccessed data frame
    df_energy_consumption_series = df_energy_consumption.values
    for i in range(0, 77):
        energy_value = 0
        for j in range(0, 16):
                energy_value = energy_value + df_energy_consumption_series[i, j]
        energy_list.append(energy_value)

    print(aggregated_csv_filename + " " + "Total Energy consumed: " ,sum(energy_list))


def plot_generator_energy(scenario_name,minutes,cumulative_intervals,plot_type="cumul"):
    # Get path to plots folder
    # Generate plots in the plots folder where folder name is the name of the scenario and the QoS name
    energy_score_json = {}
    energy_score_json[scenario_name] = {}
    plots_path = init_object.plots_dir
    aggregate_energy = init_object.aggregate_output_path_energy
    fig = go.Figure()
    x_axis_time_list = [index for index in range(1,minutes,1) if index%cumulative_intervals==0 ]
    print ("x axis ",x_axis_time_list)
    median_energy = 0

    for folder_name in os.listdir(aggregate_energy):
        print (folder_name)
        try:
            if scenario_name in folder_name:
                energy_score_json[scenario_name][folder_name] = {"data" : [], "median" : 0.0}
                file_path = aggregate_energy + folder_name + "/" + "aggregate_energy_"+ folder_name +".csv"
                #print (file_path)
                energy_list = []
                df_energy_consumption = pd.read_csv(file_path, sep=",",
                                                    index_col="timestamp")  # Read the proccessed data frame
                df_energy_consumption_series = df_energy_consumption.values
                energy_value = 0
                for i in range(0, minutes):
                    for j in range(0, 16):
                        energy_value = energy_value + df_energy_consumption_series[i, j]
                    if (i!=0 and i%cumulative_intervals==0):
                        energy_list.append(energy_value)
                        energy_score_json[scenario_name][folder_name]["data"].append(energy_value)
                        if plot_type == "box":
                            energy_value = 0
                print(folder_name + " " + "Total Energy consumed: ", sum(energy_list))
                print (len(energy_list))

                if plot_type == "cumul":
                    fig.add_trace(go.Scatter(x=x_axis_time_list, y=energy_list, name=folder_name))
                                        #line=dict(color='firebrick', width=4)))
                elif plot_type == "box":
                    fig.add_trace(go.Box(y=energy_list, quartilemethod="linear", name=folder_name))

                # First normalize the list to calculate the normalized median score
                normalized_energy_list = []
                energy_score_json[scenario_name][folder_name]["median"] = statistics.median(energy_score_json[scenario_name][folder_name]["data"])
                energy_score_json[scenario_name][folder_name]["max"] = max(energy_score_json[scenario_name][folder_name]["data"])
                energy_score_json[scenario_name][folder_name]["min"] = min(energy_score_json[scenario_name][folder_name]["data"])
                energy_score_json[scenario_name][folder_name]["mean"] = statistics.mean(energy_score_json[scenario_name][folder_name]["data"])

        except Exception as e:
            print (folder_name)
            print (e)


    # 2 hour simulation implies 120 minutes data which can be aggregated to 10 minute intervals or 15 minute slots


    #fig = go.Figure()
    # Create and style traces
    #fig.add_trace(go.Scatter(x=x_axis_time_list, y=high_2014, name='High 2014',
     #                        line=dict(color='firebrick', width=4)))
    '''
    fig.add_trace(go.Scatter(x=month, y=low_2014, name='Low 2014',
                             line=dict(color='royalblue', width=4)))
    fig.add_trace(go.Scatter(x=month, y=high_2007, name='High 2007',
                             line=dict(color='firebrick', width=4,
                                       dash='dash')  # dash options include 'dash', 'dot', and 'dashdot'
                             ))
    fig.add_trace(go.Scatter(x=month, y=low_2007, name='Low 2007',
                             line=dict(color='royalblue', width=4, dash='dash')))
    fig.add_trace(go.Scatter(x=month, y=high_2000, name='High 2000',
                             line=dict(color='firebrick', width=4, dash='dot')))
    fig.add_trace(go.Scatter(x=month, y=low_2000, name='Low 2000',
                             line=dict(color='royalblue', width=4, dash='dot')))
    '''
    # Edit the layout
    fig.update_layout(
        #title='Energy Consumption for Scenario ' + scenario_name,
                      xaxis_title='Time intervals (Aggregated over 15 minutes)',
                      yaxis_title='Energy Consumption (In Joules)',font=dict(
        family="sans serif",
        size=14,
        color="black",
    ),margin={"r":0,"t":0,"l":0,"b":0}, legend=
            dict(
            #orientation="v",
            #anchor="bottom",
            #y=1.02,
            #xanchor="right",
            #x=1.0,
            font=dict(size=12)
    ))

    #fig.layout.plot_bgcolor = 'rgba(0,0,0,0)'
    #fig.layout.grid = 'True'
    fig.show()
    if plot_type == "cumul":
        fig.write_image(init_object.plots_dir + "energy_consumption_" + scenario_name + "_cumul.png", format="png", engine="kaleido",
                        width=640, height=480,
                        scale=10.0)
    elif plot_type == "box":
        fig.write_image(init_object.plots_dir + "energy_consumption_" + scenario_name + "_box.png", format="png",
                        engine="kaleido",
                        width=640, height=480,
                        scale=10.0)
    return energy_score_json

def plot_generator_sensor_data(scenario_name,minutes,cumulative_intervals,plot_type='box'):
    # Get path to plots folder
    # Generate plots in the plots folder where folder name is the name of the scenario and the QoS name
    sensor_data_score_json = {}
    sensor_data_score_json[scenario_name] = {}
    plots_path = init_object.plots_dir
    aggregate_data = init_object.aggregate_sensor_data
    fig = go.Figure()
    x_axis_time_list = [index for index in range(1, minutes, 1) if index % cumulative_intervals == 0]
    print(x_axis_time_list)
    for folder_name in os.listdir(aggregate_data):
        try:
            if scenario_name in folder_name:
                  # for storing the utility scores
                sensor_data_score_json[scenario_name][folder_name] = {"data" : [], "median" : 0.0} # Intialize the json for a particular model config pair
                file_path = aggregate_data + folder_name + "/" + "aggregate_sensor_data"+ folder_name +".csv"

                sensor_data_list = []
                df_sensor_data = pd.read_csv(file_path, sep=",",
                                                    index_col="timestamp")  # Read the proccessed data frame
                df_sensor_data_series = df_sensor_data.values
                sensor_data = 0
                for i in range(0, minutes):
                    for j in range(0, 1):
                        sensor_data = sensor_data + df_sensor_data_series[i, j]
                    if (i!=0 and i%cumulative_intervals==0):
                        sensor_data_list.append(sensor_data)
                        if plot_type == "box":
                            # We need to compute the average for every N minutes to understand the mean
                            sensor_data_score_json[scenario_name][folder_name]["data"].append(sensor_data)
                            sensor_data = 0


                # Find the median for each configuration models in the scenario
                sensor_data_score_json[scenario_name][folder_name]["median"] = statistics.median(sensor_data_score_json[scenario_name][folder_name]["data"])
                sensor_data_score_json[scenario_name][folder_name]["max"] = max(sensor_data_score_json[scenario_name][folder_name]["data"])
                sensor_data_score_json[scenario_name][folder_name]["min"] = min(sensor_data_score_json[scenario_name][folder_name]["data"])
                sensor_data_score_json[scenario_name][folder_name]["mean"] = statistics.mean(sensor_data_score_json[scenario_name][folder_name]["data"])
                print(folder_name + " " + "Total number of people ", sum(sensor_data_list))
                print (len(sensor_data_list))

                #fig.add_trace(go.Scatter(x=x_axis_time_list, y=sensor_data_list, name=folder_name))
                if plot_type == "box":
                    fig.add_trace(go.Box(y= sensor_data_list, quartilemethod="linear", name=folder_name))
                elif plot_type == "cumul":
                    fig.add_trace(go.Scatter(x=x_axis_time_list, y=sensor_data_list, name=folder_name))


        except Exception as e:
            print (folder_name)
            print (e)

    fig.update_layout(
        #title='People Movement Data for ' + scenario_name,
                      xaxis_title='Time intervals (Aggregated over 15 minutes)',
                      yaxis_title='Number of People',font=dict(
        family="sans serif",
        size=14,
        color="black"
    ),margin={"r":0,"t":0,"l":0,"b":0},
        legend=
            dict(
            #orientation="v",
            #anchor="bottom",
            #y=1.02,
            #xanchor="right",
            #x=1.0,
            font=dict(size=12)
    ))

    fig.show()
    fig.write_image(init_object.plots_dir + "people_movement_"+scenario_name +".png", format="png", engine="kaleido", width=640, height=480,
                    scale=10.0)

    #fig.write_image(plots_path + scenario_name + "_data.jpg")
    return sensor_data_score_json


def tradeoff_score_calculator(energy_list,data_list,median_energy_min,median_data_max,energy_pen,data_pen,cumulative_intervals,scenario_name,max_energy,max_data,min_energy,min_data):
    # Calculate the utility score and
    fig = go.Figure()
    x_axis_time_list = [index for index in range(1, minutes, 1) if index % cumulative_intervals == 0]
    #fig = make_subplots(rows=2, cols=1)
    data_weight = 1
    energy_weight = 1

    # Assign goals based on scnearios in mix type and the time of the day as different parts of the day requires different QoE and QoS (Identified based on experience)
    mix_energy_data_goal_list = [(150,1000),(150,480),(100,200),(125,100),(180,1200),(120,1200),(100,200),(125,100)]
    mix_energy_data_pen_list = [(5,15),(10,10),(10,5),(3,15),(5,10),(10,10),(10,5),(3,15)]



    normalized_energy_min = (median_energy_min-min_energy)/(max_energy-min_energy)
    normalized_data_max = (median_data_max-min_data)/(max_data-min_data)

    print ("energy pen ", energy_pen)

    print ("normalized energy min ", normalized_energy_min)
    print ("normalized data max ", normalized_data_max)

    print ("max energy ", max_energy)
    print (" max data ", max_data)
    negative_cum_tradeoff_dict = {}
    for model_config in energy_list:
        energy_score_sum = 0
        data_score_sum = 0
        index = 0
        mix_scenario_list_iterator = 0
        # create energy and data score list to store the energy and data score sum per interval and then normalize
        print (model_config)
        energy_score_list = []
        data_score_list  = []

        for energy_val in energy_list[model_config]["data"]:
            if scenario_name == "Mix":
                # the goal and penalty changes every one hour
                print ("Index" , index)
                if (index%4==0):
                    print (" inside index ", index)
                    print (" max energy ", max_energy)
                    print (" max data  ", max_data)
                    normalized_energy_min = (mix_energy_data_goal_list[mix_scenario_list_iterator][0]-min_energy)/ (max_energy-min_energy)
                    normalized_data_max = (mix_energy_data_goal_list[mix_scenario_list_iterator][1]-min_data)/ (max_data-min_data)
                    energy_pen = mix_energy_data_pen_list[mix_scenario_list_iterator][0]
                    data_pen = mix_energy_data_pen_list[mix_scenario_list_iterator][1]

                    print("energy pen mixed ", energy_pen)
                    print (" data pen ", data_pen)
                    print("normalized energy min mixed ", normalized_energy_min)
                    print("normalized data max mixed ", normalized_data_max)

                    mix_scenario_list_iterator +=1
                    #if (mix_scenario_list_iterator==4):
                    #    mix_scenario_list_iterator = 0
                    print (" mix scenario iterator ", mix_scenario_list_iterator)


            normalized_energy_val = (energy_val - min_energy) / (max_energy - min_energy)
            normalized_data_val = (data_list[model_config]["data"][index] - min_data) / (max_data - min_data)

            if (normalized_energy_min - normalized_energy_val) < 0:
                energy_score_sum = energy_pen*(normalized_energy_min - normalized_energy_val)
            elif (normalized_energy_min - normalized_energy_val) >= 0:
                energy_score_sum = (normalized_energy_min - normalized_energy_val)
            energy_score_list.append(energy_score_sum)

            if (normalized_data_val - normalized_data_max) < 0:
                data_score_sum = data_pen*(normalized_data_val - normalized_data_max)
            elif (normalized_data_val - normalized_data_max) >= 0:
                data_score_sum = normalized_data_val - normalized_data_max
            data_score_list.append(data_score_sum)
            index += 1


        print (model_config)
        print (data_list[model_config]["data"])
        print (energy_list[model_config]["data"])
        print (" energy score list ", energy_score_list)
        print (" data score list ", data_score_list)

        # Most of the elements are negative hence add the minimum value to make the list positive

        positive_energy_score_list = []
        positive_data_score_list = []



        max_energy_score = max(energy_score_list)

        overall_score_sum = 0
        iterator = 0
        cum_tradeoff_score_list = []
        for data_score in data_score_list:
            overall_score_sum = overall_score_sum + (energy_score_list[iterator]) + (data_score)
            cum_tradeoff_score_list.append(overall_score_sum)
            iterator+=1


        print(cum_tradeoff_score_list)
        negative_cum_tradeoff_dict[model_config]=cum_tradeoff_score_list

        #fig.add_trace(go.Scatter(x=x_axis_time_list, y=cum_tradeoff_score_list, name=model_config))
        print (model_config,overall_score_sum)

    '''
    fig.add_trace(go.Scatter(x=x_axis_time_list, y=data_list["M6_C1_S1"]["data"],name="Average Count"),row=1,col=1)
    fig.update_yaxes(title_text="Cumulative Tradeoff Score", row=2, col=1,tickfont=dict(
        family="sans serif",
        size=12,
        color="black",
))
    fig.update_xaxes(title_text="Time intervals (Aggregated over 15 minutes)", row=2, col=1,tickfont=dict(
        family="sans serif",
        size=12,
        color="black",
))
    fig.update_yaxes(title_text="Average Number of People", row=1, col=1,tickfont=dict(
        family="sans serif",
        size=12,
        color="black",
))
'''
    positive_cum_tradeoff_dict = {}

    for key1 in negative_cum_tradeoff_dict.keys():
        print (" main ",key1)
        positive_cum_tradeoff_dict[key1] = []
        positive_list = []
        for index in range (0,len(negative_cum_tradeoff_dict[key1])):
            temp_list = []
            for key2 in negative_cum_tradeoff_dict:
                print (" third ", key2, index)
                temp_list.append(negative_cum_tradeoff_dict[key2][index])

            print (key1)
            min_val = -1*min(temp_list)
            print (min_val)
            print (negative_cum_tradeoff_dict[key1][index])
            # Add a constant to make it even for the minimum graph
            positive_list.append(negative_cum_tradeoff_dict[key1][index] + min_val + index)
            #print(negative_cum_tradeoff_dict[key1][index])

        positive_cum_tradeoff_dict[key1] = positive_list

    print ("positive cum tradeoff dict" , positive_cum_tradeoff_dict)
    for key in negative_cum_tradeoff_dict.keys():
        fig.add_trace(go.Scatter(x=x_axis_time_list, y=positive_cum_tradeoff_dict[key], name=key))
    fig.update_layout(
        title='Cumulative Tradeoff Plot for ' + scenario_name,
        xaxis_title='Time intervals (Aggregated over 15 minutes)',
        yaxis_title='Cumulative Tradeoff Score',
        font=dict(
        family="sans serif",
        size=12,
        color="black",
),margin={"r":0,"t":0,"l":0,"b":0},
        legend=
            dict(
            #orientation="v",
            #anchor="bottom",
            #y=1.02,
            #xanchor="right",
            #x=1.0,
            font=dict(size=12)
    ),)
        #legend=dict(
   # yanchor="top",
    #y=0.99,
    #xanchor="left",
    #x=0.01
    #)
    #)
    fig.write_image(init_object.plots_dir+"tradeoff_plot_" + scenario_name + ".png",format="png",engine="kaleido", width=1024, height=576,scale=10.0)
    fig.show()



def create_3d_plot(scenario,cumulative_intervals,minutes):

    mean_energy_list = []
    mean_movement_list = []
    fig = go.Figure()
    energy_json = plot_generator_energy(scenario, minutes, cumulative_intervals, plot_type="box")
    data_json = plot_generator_sensor_data(scenario, minutes, cumulative_intervals, plot_type="box")


    name_list = []
    for model_config in energy_json[scenario]:
        mean_energy_list.append(energy_json[scenario][model_config]["data"])
        mean_movement_list.append(data_json[scenario][model_config]["data"])
        name_list.append(model_config)

    fig.add_trace(go.Scatter(x=mean_energy_list, y=mean_movement_list,
                             mode='markers',
                             name='markers'))




    print (mean_energy_list)
    print (mean_movement_list)


    fig.show()




if __name__ == '__main__':

    #for folder_name in os.listdir(init_object.output_path):
    #    calculate_energy_consumption(init_object.output_path + folder_name + "/" + "aggregate_energy_" + folder_name + ".csv")
    #minutes = 481 # Number of minutes
    minutes = 121 # Number of minutes
    cumulative_intervals = 15 # Intervals in which the summation has to be done
    #scenario = "S2"
    scenario = "S4"

    energy_json = plot_generator_energy(scenario,minutes,cumulative_intervals,plot_type="box")
    data_json = plot_generator_sensor_data(scenario,minutes,cumulative_intervals,plot_type="box")

    print (" energy json ")
    #print (energy_json)
    sorted_energy = OrderedDict(sorted(energy_json[scenario].items()))
    print (json.dumps(sorted_energy))
    print (" data json ")
    sorted_data = OrderedDict(sorted(data_json[scenario].items()))
    print(json.dumps(sorted_data))

    median_min_energy = 10000
    min_energy = 20000
    max_energy = 0
    energy_median_sum = 0
    print (energy_json)

    e_mean_value = 0

    for model_config in energy_json[scenario]:
        print (model_config)
        energy_median_sum = energy_median_sum + energy_json[scenario][model_config]["median"]
        e_mean_value = e_mean_value + statistics.mean(energy_json[scenario][model_config]["data"])

        if energy_json[scenario][model_config]["median"]< median_min_energy:
            median_min_energy = energy_json[scenario][model_config]["median"]

        if energy_json[scenario][model_config]["min"]< min_energy:
            min_energy = energy_json[scenario][model_config]["min"]
        if energy_json[scenario][model_config]["max"] > max_energy:
            max_energy = energy_json[scenario][model_config]["max"]


    print (" mean energy ", e_mean_value/18.0)
    print (min_energy)
    print (max_energy)
    print ("median sum average ", energy_median_sum/18.0)





    median_max_data = 0
    min_data = 200000
    max_data = 0
    data_median_sum = 0
    data_mean_value = 0

    for model_config in data_json[scenario]:
        data_median_sum = data_median_sum + data_json[scenario][model_config]["median"]
        data_mean_value = data_mean_value + statistics.mean(data_json[scenario][model_config]["data"])
        if data_json[scenario][model_config]["median"] > median_max_data:
            median_max_data = data_json[scenario][model_config]["median"]
        if data_json[scenario][model_config]["min"] < min_data:
            min_data = data_json[scenario][model_config]["min"]
        if data_json[scenario][model_config]["max"] > max_data:
            max_data = data_json[scenario][model_config]["max"]


    # Find the max data and minimum energy from the scenarios

    print (" data mean value ", data_mean_value/18.0)

    print (" max data ", max_data)
    print (" min data ", min_data)
    print (" data goal ", data_mean_value/5.0)
    print (" energy goal ", e_mean_value/5.0)

    if scenario == "Mix":
        # 200.0 and 900.0 denote the range for ease of normalization
        tradeoff_score_calculator(energy_json[scenario], data_json[scenario], 125.0, 1000.0, init_object.qos_penalty,
                                  init_object.qoe_penalty, cumulative_intervals, scenario, 250.0, 1200.0, min_energy,
                                  min_data)
    else:
        tradeoff_score_calculator(energy_json[scenario],data_json[scenario],125.0,100.0,init_object.qos_penalty,init_object.qoe_penalty,cumulative_intervals,scenario,e_mean_value/18.0,data_mean_value/18.0,min_energy,min_data)


    #create_3d_plot("S1",15,121)