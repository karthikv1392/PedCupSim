_Author_ = "Karthik Vaidhyanathan"

# Get the sensor data for the different sensors to compute Quality of Experience
from Initalizer import Initialize
from datetime import datetime
from datetime import timedelta
import os

import pandas as pd
init_object = Initialize()


class Data_Loader_Sensor():
    # class to load the csv data to json

    data_traffic_path = ""
    data_traffic_file = ""
    def __init__(self):
        self.results_dir = init_object.results_dir
        self.result_folder = init_object.result_folder
        self.sensor_data_file = init_object.sensor_logs
        self.aggregate_output = init_object.aggregate_sensor_data


    def load_data_to_csv(self,folder_name):
        # loads the log file to csv file
        file =  open(self.results_dir + folder_name + "/" + self.sensor_data_file,"r")
        sensor_data_count = 1 # Keep a check on the number of data points collected
        traffic_count  = 0
        traffic_induvidual_count = 0 # For each time instance
        sensor_data = 0
        prev_time  = 0.0 # Keep a check on the time
        df_dict = {}
        df_dict_sensor = {}
        line_count = 0
        for line in file.readlines():
            if "Time" in line:
                if line_count>0:
                    #if prev_time in df_dict:
                    #    df_dict[prev_time]=df_dict[prev_time] + traffic_induvidual_count
                    #else:
                    if prev_time not in df_dict:
                        df_dict[prev_time] = traffic_induvidual_count
                        df_dict_sensor[prev_time] = float(sensor_data)
                        traffic_induvidual_count = 0
                        sensor_data = 0
                    current_time = float(line.split(":")[1].split(" ")[1])

                    #print (current_time)
                    prev_time = current_time
                line_count += 1
            if (init_object.server_sensor_id + " is reading from its buffer") in line:
                server_sensor_data = float(line.split(" ")[6].strip("\""))
                sensor_data = sensor_data + server_sensor_data
                sensor_data_count+=1
                print (server_sensor_data)

        #print (traffic_count)
        #print (sum(df_dict.values()))
        df_dict[prev_time]=sensor_data_count
        max_time =prev_time  # The last time value inserted becomes the maximum time
        start_time = datetime.now() - timedelta(seconds=max_time)
        #print (traffic_count)
        print (start_time)
        new_df_dict = {}
        check_Sum = 0

        # Another dataframe for sensor data
        dataframe_sensor_data = {}
        dataframe_sensor_data["timestamp"] = []
        dataframe_sensor_data["sensor_data"] = []


        for key in df_dict_sensor.keys():
            check_Sum =  check_Sum + df_dict_sensor[key]
            milliseconds = float(key *1000)
            time_value = start_time + timedelta(milliseconds=milliseconds)
            dataframe_sensor_data["timestamp"].append(time_value)

            if time_value in new_df_dict:
                new_df_dict[time_value] = new_df_dict[time_value] +  df_dict_sensor[key]
                #dataframe_dict["traffic"].append(new_df_dict[time_value] +  df_dict[key])
                print (df_dict[key])
                dataframe_sensor_data["sensor_data"].append(df_dict_sensor[key])
            else:
                new_df_dict[time_value] = df_dict[key]
                dataframe_sensor_data["sensor_data"].append(df_dict_sensor[key])


        #processed_dataframe = pd.DataFrame(dataframe_dict)
        processed_dataframe = pd.DataFrame(dataframe_sensor_data)
        processed_dataframe.index = processed_dataframe["timestamp"]
        aggregate_df = processed_dataframe.resample('1T').sum()
        os.mkdir(init_object.aggregate_sensor_data + folder_name)
        aggregate_df.to_csv(init_object.aggregate_sensor_data + folder_name + "/" + "aggregate_sensor_data" + folder_name + ".csv",
                            index=True)
        #aggregate_df.to_csv(init_object.data_path+ "aggregated_traffic_CO_5Dec" +".csv",index =True)


if __name__ == '__main__':
    sensor_data_loader = Data_Loader_Sensor()
    for folder_name in os.listdir(sensor_data_loader.results_dir):
        sensor_data_loader.load_data_to_csv(folder_name)