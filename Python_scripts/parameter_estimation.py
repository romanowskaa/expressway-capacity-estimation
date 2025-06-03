import pandas as pd
import math

class BasicSection:
    """
    Class of functions to calculate traffic metrics at basic sections of dual-carriageway uninterrupted traffic facilities
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

    # def calculate_avg_speed(self):






# bs = BasicSection(road_class='A', access_points=5, speed_limit=120, area_type=1, adt=30000, hv_share = 0.1, profile='DASM', lanes=2, gradient=0.02, section_length=10)
# bs = BasicSection(road_class='S', access_points=7, speed_limit=110, area_type=0, adt=120000, hv_share = 0.08, profile='DASD', lanes=3, gradient=0.03, section_length=10)
bs = BasicSection(road_class='GPG', access_points=12, speed_limit=90, area_type=1, adt=60000, hv_share = 0.12, profile='DGPG', lanes=2, gradient=0.04, section_length=8)
# bs = BasicSection(road_class='GPG', access_points=12, speed_limit=90, area_type=1, adt=6000, hv_share = 0.3, profile='DGPG', lanes=2, gradient=0.05, section_length=8)

print(bs.calculate_opt_speed())