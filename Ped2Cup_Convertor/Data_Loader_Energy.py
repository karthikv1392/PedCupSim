_Author_ = "Karthik Vaidhyanathan"

# This will parse the log file of CupCarbon and generate the data

from configparser import ConfigParser

import json

import csv
import pandas as pd

from datetime import datetime
from datetime import timedelta
from Initalizer import Initialize
import os

CONFIG_FILE = "settings.conf"
CONFIG_SECTION = "settings"

init_object = Initialize()


class DataLoader():
    # class to load the csv data to json
    # This will also support loading real-time simulation data from kafka queue for prediction
    data_path = ""
    energy_val = 19160.0  # starting energy value as per CupCarbon
    component_count = 0  # The total number of sensors for which the monitoring needs to be done
    data_file = ""
    json_path = ""

    def __init__(self):
        # Initialize the configurations
        self.results_dir = init_object.results_dir
        self.result_folder = init_object.result_folder

        self.data_path = init_object.data_path
        self.data_file = init_object.data_file
        self.json_path = init_object.output_path
        self.energy_val = float(init_object.energy_val)
        # self.component_count = int(init_object.component_count)
        self.component_count = int(init_object.components)
        self.aggregate_file_name = init_object.result_folder

    def load_data_history(self,result_folder_name):
        # Loads the historical csv file to the json

        sensor_json = {}
        prev_vals = []  # A list to store the energy values of the previous state
        # For every sensor, create a key and then insert time and energy as pairs
        # df = pd.read_csv(self.data_path + self.data_file,sep=";")   # Load the csv into a dataframe
        df = pd.read_csv(init_object.results_dir + result_folder_name + "/" + init_object.energy_file, sep=";")  # Load the csv into a dataframe

        max_time = (max(df["Time (Sec)"]))  # Find the maximum seconds for which the simulation was done.
        start_time = datetime.now() - timedelta(
            seconds=max_time)  # The maximum time will allow us to create a mapping for timestamp

        # Convert this data frame to a new dataframe with proper timestamps
        # Read the csv and convert into a json which can be used by time series databases

        new_df_dict = {}
        new_df_dict["timestamp"] = []
        # print (df)
        # with open(self.data_path + self.data_file) as csvfile:
        sensor_key_dict = {}

        with open(init_object.results_dir + result_folder_name + "/" + init_object.energy_file) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';', )
            count = 0
            for row in csvreader:
                sen_count = 1
                if count == 0:
                    # time.sleep(10)
                    key_start = "S"
                    key_count = 1
                    print(row)
                    # time.sleep(10)
                    for key in row[1:]:
                        # Create a mapping to keep all the mappings uniform
                        if key != "":
                            sensor_key_dict[key] = key_start + str(key_count)
                            key_count += 1

                    print(sensor_key_dict)
                    # time.sleep(10)
                    for keys in row[1:]:
                        if keys != "":
                            sensor_json[sensor_key_dict[keys]] = []
                            new_df_dict[sensor_key_dict[keys]] = []
                            prev_vals.append(self.energy_val)  # all will have the same amount of energy

                # print (len(prev_vals))
                if count >= 1:
                    time_value = start_time + timedelta(milliseconds=float(row[0]) * 1000)
                    timestamp = int(time_value.timestamp() * 1000)
                    # if (timestamp) in new_df_dict["timestamp"]:
                    #    print ("exist " + str(count))
                    # else:
                    new_df_dict["timestamp"].append(timestamp)

                    # print (prev_vals)
                    # time.sleep(2)
                    while sen_count <= self.component_count:
                        time_energy_pair = []  # Create a time energy pair
                        # time_value = start_time + timedelta(seconds=float(row[0]))
                        # print (time_value)
                        # Convert the timestamp to epoch timestamp
                        # timestamp = time.mktime(time_value.timetuple())
                        # timestamp = int(time_value.timestamp() *1000)    # Get timestamp in milliseconds
                        # Normalize the data value for energy

                        # Energy value should be subtracted from the previous
                        # print (prev_vals[sen_count-1])x
                        # normalized_energy_val = round(
                        # float((self.energy_val - float(row[sen_count])) / self.energy_val), 5) * 1000
                        normalized_energy_val = prev_vals[sen_count - 1] - float(row[sen_count])
                        # print(normalized_energy_val)
                        # time.sleep(2)
                        # print (prev_vals[sen_count-1])
                        # normalized_energy_val =  (prev_vals[sen_count-1] - float(row[sen_count])) * 1000
                        prev_vals[sen_count - 1] = float(row[sen_count])  # Re assign the values
                        # normalized_energy_val =  round(prev_vals[sen_count-1] - float(row[sen_count]),2)
                        # normalized_energy_val =  round(prev_vals[sen_count-1] - float(row[sen_count]),2)

                        time_energy_pair.append(timestamp)
                        time_energy_pair.append(float(row[sen_count]))
                        sensor_json["S" + str(sen_count)].append(time_energy_pair)
                        new_df_dict["S" + str(sen_count)].append(normalized_energy_val)
                        sen_count += 1
                    # print (prev_vals)
                    # time.sleep(1)
                count += 1
                # print (count)

        # Now the sensor_json will have all the data stored store it in the data folder
        # print (sensor_json)

        data_json_file = open(self.json_path + "data.json", "w")
        json.dump(sensor_json, data_json_file)

        # print (new_df_dict)

        # Convert the new df dict to a pandas data frame

        data_frame = pd.DataFrame(new_df_dict)

        # Send back the data_frame to the calling function and save as a new csv file
        data_frame.to_csv(self.data_path + "processed_data.csv", index=False)

        # print (process_df)

        # print (process_df.timestamp[])
        # resample_index = pd.date_range(start=process_df.timestamp[0], end=max(process_df.timestamp), freq='1s')
        # dummy_frame = pd.DataFrame(process_df, index=resample_index, columns=process_df.columns)

        # Return the data frame to
        return data_frame

    def process_data(self, data_frame,folder_name):
        # Takes a dataframe as argument
        ds = pd.to_datetime(data_frame["timestamp"],
                            unit='ms')  # Convert the timestamps to new value to get the aggregated time stamp

        column_list = data_frame.columns.values
        process_df = data_frame[[column_list[1]]].copy()  # Ignore the timestamp column
        for index in column_list:
            # Loop through all the columns and keep adding them
            if index != "timestamp":
                process_df[index] = data_frame[[index]]

        process_df.index = ds  # The index will go as the timestamp values
        # process_df["S2"] = data_frame[["S2"]]
        # process_df["S3"] = data_frame[["S3"]]
        # process_df["S4"] = data_frame[["S4"]]
        # process_df["S5"] = data_frame[["S5"]]
        # process_df["S6"] = data_frame[["S6"]]
        # process_df.index = ds
        aggregate_df = process_df.resample('1T').sum()  # Summing up the energy values for every second frequency
        os.mkdir(init_object.aggregate_output_path_energy + folder_name)
        aggregate_df.to_csv(init_object.aggregate_output_path_energy + folder_name + "/"+ "aggregate_energy_" + folder_name +".csv", index=True)


if __name__ == '__main__':

    data_loader_obj = DataLoader()
    for folder_name in os.listdir(data_loader_obj.results_dir):
        data_frame_energy = data_loader_obj.load_data_history(folder_name)
        data_loader_obj.process_data(data_frame_energy,folder_name)
