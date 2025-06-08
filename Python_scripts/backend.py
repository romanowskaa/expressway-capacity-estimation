import pandas as pd
import numpy as np
import math

class BasicSection:
    """
    Class of functions to calculate traffic metrics at basic section of dual-carriageway uninterrupted traffic facility
    """
    def __init__(self, road_class, access_points, speed_limit, area_type, adt, hv_share, 
                 profile, lanes, gradient=0, section_length=10):
        self.road_class = road_class
        self.access_points = access_points
        self.speed_limit = speed_limit
        self.area_type = area_type
        self.adt = adt
        self.hv_share = hv_share
        self.profile = profile
        self.lanes = lanes
        self.gradient = gradient
        self.section_length = section_length

        # load dfs from csv files
        self.u50_table = pd.read_csv('data_tables\\u50.csv')
        self.ew_table = pd.read_csv('data_tables\\ew_rate.csv')
        self.los_table = pd.read_csv('data_tables\\psr_bound.csv')
        self.capacity_table = pd.read_csv('data_tables\\capacity.csv')


    def calculate_access_point_density(self):
        """
        Calculates the density of access points given in number per 10 km section, 5 km upstream and 5 km downstream from the cross-section analysed.
        """
        return round(self.access_points / self.section_length, 2)
    
    def calculate_ffs(self):
        """
        Calculates free-flow speed, which is a speed of light vehicles in conditions of low traffic volumes.
        """

        if self.road_class == 'A':
            ffs = round(82.2 
            - 10.7 * self.calculate_access_point_density()
            + 7.7 * self.area_type
            + 0.334 * self.speed_limit)
        elif self.road_class == 'S':
            ffs = round(83.5 
            - 10.7 * self.calculate_access_point_density()
            + 7.7 * self.area_type
            + 0.334 * self.speed_limit)
        else:
            ffs = round(80.5 
            - 10.7 * self.calculate_access_point_density()
            + 7.7 * self.area_type
            + 0.334 * self.speed_limit)
        
        return ffs
    
    def calculate_hourly_volume(self):
        """
        Calculates hourly traffic volume (in one direction) from annual average daily traffic (ADT) based on u50 factor.
        """
        u50_row = self.u50_table[(self.u50_table['Profile'] == self.profile) & (self.u50_table['ADT_min'] <= self.adt) & (self.u50_table['ADT_max'] >= self.adt)]
        u50 = float(u50_row.iloc[0]['u50'])
        volume = int(self.adt * u50 / 2)
        
        return volume 
    
    def calculate_k15(self):
        """
        Calculates k15 factor, based on hourly traffic volume.
        """
        if self.calculate_hourly_volume() >= 1000:
            if self.area_type == 0:
                k15 = 0.482 + 0.063 * math.log(self.calculate_hourly_volume() / self.lanes)
            elif self.area_type == 1:
                k15 = 0.725 + 0.029 * math.log(self.calculate_hourly_volume() / self.lanes)
        else:
            k15 = 0.87
        
        return round(k15, 2)

    def estimate_base_capacity(self):
        """
        Calculates base capacity based on free flow speed (ffs). If ffs out-of-range for the method, lower or upper boundary is adopted.
        """
        ffs = self.calculate_ffs()
        
        # assess capacity if ffs out-of-range
        if self.road_class == 'A':
            if ffs > 130:
                ffs = 130
            elif ffs < 90:
                ffs = 90
        elif self.road_class == 'S':
            if ffs > 120:
                ffs = 120
            elif ffs < 90:
                ffs = 90
        else:
            if ffs > 110:
                ffs = 110
            elif ffs < 80:
                ffs = 80
        
        df = self.capacity_table
        cap_row = df[(df['ffs'] == ffs) & (df['road_class'] == self.road_class)]
        base_capacity = int(cap_row.iloc[0]['base_capacity'])
        
        return base_capacity

    def calculate_ew(self, est_util_rate=0.75):
        """
        Calculates conversion factor for heavy vehicles share and vertical alignment.
        """
        # set gradient category
        if self.gradient <= 0.02:
            max_gradient = 0.02
        elif self.gradient <= 0.03:
            max_gradient = 0.03
        elif self.gradient <= 0.04:
            max_gradient = 0.04
        else:
            max_gradient = 0.05

        # calculate light vehicles conversion factor
        Es_row = self.ew_table[(self.ew_table['veh_type'] == 'lv') 
                               & (self.ew_table['max_gradient'] == max_gradient)]
        Es = float(Es_row.iloc[0]['conv_factor'])
        
        # calculate heavy vehicles conversion factor
        Ec_row = self.ew_table[(self.ew_table['veh_type'] == 'hv') 
                               & (self.ew_table['road_class'] == self.road_class) 
                               & (self.ew_table['lanes'] == self.lanes)
                               & (self.ew_table['max_util_rate'] == est_util_rate)
                               & (self.ew_table['max_gradient'] == max_gradient)]
        Ec = float(Ec_row.iloc[0]['conv_factor'])

        # calculate weighted conversion factor
        Ew = round(Es * (1 - self.hv_share) + Ec * self.hv_share, 2)

        return Ew

    def calculate_flow(self):
        """
        Calculates traffic flow at the section (expressed in light vehicles per hour per 1 lane)
        """
        flow = round(self.calculate_hourly_volume()
                     * self.calculate_ew()
                     / (self.lanes * self.calculate_k15()))
        
        # checking the condition for max utilization rate in conversion factors (Ew) table
        if flow / self.estimate_base_capacity() >= 0.75:
            flow = round(self.calculate_hourly_volume()
                     * self.calculate_ew(est_util_rate=1)
                     / (self.lanes * self.calculate_k15()))

        return flow

    def calculate_utilization(self):
        """
        Calculates utilization rate as a 'flow' to 'base capacity' rate
        """
        util_rate = round(self.calculate_flow() / self.estimate_base_capacity(), 2)
        return util_rate

    def calculate_opt_speed(self):

        ffs = self.calculate_ffs()
        
        # assess opt_speed if ffs out-of-range
        if self.road_class == 'A':
            if ffs > 130:
                ffs = 130
            elif ffs < 90:
                ffs = 90
        elif self.road_class == 'S':
            if ffs > 120:
                ffs = 120
            elif ffs < 90:
                ffs = 90
        else:
            if ffs > 110:
                ffs = 110
            elif ffs < 80:
                ffs = 80
        
        df = self.capacity_table
        opt_speed_row = df[(df['ffs'] == ffs) & (df['road_class'] == self.road_class)]
        opt_speed = float(opt_speed_row.iloc[0]['opt_speed'])
        
        return opt_speed

    def van_aerde_calculations(self):
        """
        Returns data frame with Van Aerde model calculations with speed step 0.01.
        Model parameters are adopted from capacity table and above calculations. 
        Jam density is an empirical value adopted based on own research.
        """
        # model parameters
        capacity = self.estimate_base_capacity()
        opt_speed = self.calculate_opt_speed()
        ffs = self.calculate_ffs()
        jam_density = 150

        # Van Aerde model coefficients
        m = (2* opt_speed - ffs) / ((ffs - opt_speed)**2)
        c2 = 1 / (jam_density * (m + 1/ffs))
        c1 = m * c2
        c3 = (1/opt_speed) * ((opt_speed/capacity) - c1 - c2/(ffs - opt_speed))

        # create df for model calculations with first column with speed decreasing by 1 in each row
        data = {'speed': [round(float(speed),2) for speed in np.arange(ffs, -0.01, -0.01)]}
        df = pd.DataFrame(data)
        df['density'] = round(1 / (c1 + c2/(ffs - df['speed']) + c3 * df['speed']), 2)
        df['volume'] = round(df['speed'] * df['density'], 2)

        return df

    def calculate_avg_speed(self):
        """
        Calculates average speed at the flow if capacity is not exceeded.
        
        """
        # calculated only for uninterrupted flow
        opt_density = 26.5

        df_all_densitites = self.van_aerde_calculations()
        df = df_all_densitites[df_all_densitites['density'] <= opt_density]

        # find the closest volume to flow in df['volume'] 
        # method 1 from https://www.geeksforgeeks.org/finding-the-nearest-number-in-a-dataframe-using-pandas/  
        if self.calculate_utilization() <= 1:
            flow = self.calculate_flow()
            differences = np.abs(df['volume'] - flow)
            nearest_index = differences.argsort()[0]
            nearest_volume = float(df['volume'].iloc[nearest_index])
            nearest_volume_row = df[df['volume'] == nearest_volume]
            avg_speed = float(nearest_volume_row.iloc[0]['speed'])
            return avg_speed
        else:
            print("Avg cannot be estimated because of exceeding the road capacity.\n" \
            "The method can be applied only for uncongested traffic conditions.")

    def calculate_density(self):
        """
        Calculates density based on fundamental relationship of traffic flow (flow to avg speed) 
        """
        try:
            density = round(self.calculate_flow() / self.calculate_avg_speed(), 1)
            return density
        except Exception:
            print("Density cannot be calculated for congested traffic regime.")

    def assess_los(self):
        """
        Assesses the level of service based on density and boundaries defined in los_table
        """
        df = self.los_table
        density = self.calculate_density()
        df['lane_density'] = pd.to_numeric(df['lane_density'])
        try:
            for index, row in df.iterrows():
                if density <= row['lane_density']:
                    return row['LOS']
        except:
            return "F"

    def extract_los_density(self):
        """
        Returns LOS critical density
        """
        df = self.los_table
        density = float(df[df['LOS'] == self.assess_los()]['lane_density'])
        return density

    def calculate_metrics_at_density(self, density):
        """
        Calculates speed and flow at given density
        :param: density(float): lane density expressed in pc/km/lane
        """
        df = self.van_aerde_calculations()
        differences = np.abs(df['density'] - density)
        nearest_index = differences.argsort()[0]
        nearest_density = float(df['density'].iloc[nearest_index])
        nearest_density_row = df[df['density'] == nearest_density]
        speed = float(nearest_density_row.iloc[0]['speed'])
        flow = float(nearest_density_row.iloc[0]['volume'])
        return speed, flow
    




bs = BasicSection(road_class='A', access_points=5, speed_limit=120, area_type=1, adt=30000, hv_share = 0.1, profile='DASM', lanes=2, gradient=0.02, section_length=10)
# bs = BasicSection(road_class='S', access_points=7, speed_limit=110, area_type=0, adt=120000, hv_share = 0.08, profile='DASD', lanes=3, gradient=0.03, section_length=10)
# bs = BasicSection(road_class='GPG', access_points=12, speed_limit=90, area_type=1, adt=60000, hv_share = 0.12, profile='DGPG', lanes=2, gradient=0.04, section_length=8)
# bs = BasicSection(road_class='GPG', access_points=12, speed_limit=90, area_type=1, adt=6000, hv_share = 0.3, profile='DGPG', lanes=2, gradient=0.05, section_length=8)

print(bs.extract_los_density())

# speed, flow = bs.calculate_metrics_at_density(6.5)
# print(speed, flow)  # Output: John 25