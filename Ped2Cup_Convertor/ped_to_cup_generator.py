_Author_ = "Karthik Vaidhyanathan"


from Initalizer import Initialize
import csv
import json
import pandas as pd
from Custom_Logger import logger
import math

init_object = Initialize()


class Ped_To_Cup_Generator():
    # Class to perform conversion from pedsim data to cupcarbon natural event data generato
    def __init__(self):
        # Load the configuration json
        self.config_json = init_object.config_json
        self.loaded_config = {}
        try:
            # load the json
            with open(self.config_json,"r") as json_file:
                self.loaded_config = json.load(json_file)

        except Exception as e:
            print (e)
            logger.error(e)


    def write_sensor_data(self,sensor_name, data_frame):
        # Write sensor data to the specified filename
        f = open(init_object.output_path+sensor_name + ".evt", "w")
        for index in range(1, self.loaded_config["columns"], 1):
            # print(df_rows["Unnamed: " + str(index)])
            #sensor_data = data_frame["Unnamed: " + str(index)].sum()
            sensor_data = data_frame["0." + str(index)].sum()
            f.write("1.0" + " " + str(sensor_data) + ".0000000" + "\n")
        f.close()
        #print ("here")

    def data_convertor(self):
    # csv to data generator
        df = pd.read_csv(init_object.data_path + init_object.data_file,delimiter=';',index_col=0)


        print (self.loaded_config)
        df.index = df.index.str.strip()

        #print(df)

        #row_data1 = df.loc[['             {0;0}','             {1;0}','             {2;0}'],:]

        sensor_id_dict  = self.loaded_config["id_map"] #contains the sensor id map
        for key in sensor_id_dict.keys():
            sensor_name = key
            range_dict = sensor_id_dict[key]

            # get the origin and diagonal coordinates
            x1 = range_dict[0][0]
            y1 = range_dict[0][1]
            x2 = range_dict[1][0]
            y2 = range_dict[1][1]

            print (x1, y1)
            print (x2,y2)

            # collect the datapoints that needs to be collected

            loc_list = [] # the list that is required to be fetched from the pandas dataframe

            #loc_list.append("{"+str(x2)+";"+str(y2)+"}")



            for x1_iterator in range(x1,x2+1,1):
                loc_list.append("{"+str(x1_iterator)+";"+str(y1)+"}")

            for x2_iterator in range(x1+1,x2,1):
                # Not required to traverse till x2+1 as already y2 iterator takes care of this
                loc_list.append("{"+str(x2_iterator)+";"+str(y2) + "}")

            for y1_iterator in range(y1+1,y2+1,1):
                loc_list.append("{"+str(x1)+";"+str(y1_iterator)+"}")

            for y2_iterator in range(y1+1,y2+1,1):
                loc_list.append("{"+str(x2) +";" + str(y2_iterator)+"}")

            #print (loc_list)



            #row_data1 = df.loc[['{0;0}','{0;1}'],:]
            row_data1 = df.loc[loc_list,:]
            #row_data1 = df.iloc[[1:5,5:8],:]
            self.write_sensor_data(sensor_name,row_data1,)

            #break

        '''
        df_rows = df.iloc[1000:1100]
        sum = 0
        for index in range(1,300,1):
            #print(df_rows["Unnamed: " + str(index)])
            print (df_rows["Unnamed: "+str(index)].sum())


        print(df)
        with open(init_object.data_path + init_object.data_file) as csvfile:
            csvreader = csv.reader(csvfile, delimiter=';',)
            count = 0
            for row in csvreader:
                print (row[2])
        '''

if __name__ == '__main__':
    ped_to_cup_object = Ped_To_Cup_Generator()
    ped_to_cup_object.data_convertor()