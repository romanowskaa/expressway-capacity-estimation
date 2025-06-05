import pytest
from Python_scripts.backend import BasicSection

class TestBasicSection:

    def setup_method(self):
        self.bs1 = BasicSection(road_class='A', access_points=5, speed_limit=120, area_type=1, adt=30000, hv_share = 0.1, profile='DASM', lanes=2, gradient=0.02, section_length=10)
        self.bs2 = BasicSection(road_class='S', access_points=7, speed_limit=110, area_type=0, adt=120000, hv_share = 0.08, profile='DASD', lanes=3, gradient=0.03, section_length=10)
        self.bs3 = BasicSection(road_class='GPG', access_points=12, speed_limit=90, area_type=1, adt=60000, hv_share = 0.12, profile='DGPG', lanes=2, gradient=0.04, section_length=8)
        self.bs4 = BasicSection(road_class='GPG', access_points=12, speed_limit=90, area_type=1, adt=6000, hv_share = 0.3, profile='DGPG', lanes=2, gradient=0.05, section_length=8)

    def test_calculate_access_point_density(self):
        assert self.bs1.calculate_access_point_density() == 0.5, f"Expected {0.5}, but got {self.bs1.calculate_access_point_density()}"
        assert self.bs2.calculate_access_point_density() == 0.7, f"Expected {0.7}, but got {self.bs2.calculate_access_point_density()}"
        assert self.bs3.calculate_access_point_density() == 1.5, f"Expected {1.5}, but got {self.bs3.calculate_access_point_density()}"
    
    def test_calculate_ffs(self):
        assert self.bs1.calculate_ffs() == 125, f"Expected {125}, but got {self.bs1.calculate_ffs()}"
        assert self.bs2.calculate_ffs() == 113, f"Expected {113}, but got {self.bs2.calculate_ffs()}"
        assert self.bs3.calculate_ffs() == 102, f"Expected {102}, but got {self.bs3.calculate_ffs()}"

    def test_calculate_hourly_volume(self):
        assert self.bs1.calculate_hourly_volume() == 1500, f"Expected {1500}, but got {self.bs1.calculate_hourly_volume()}"  # 1 2
        assert self.bs2.calculate_hourly_volume() == 10800, f"Expected {10800}, but got {self.bs2.calculate_hourly_volume()}"  # 0 3
        assert self.bs3.calculate_hourly_volume() == 2850, f"Expected {2850}, but got {self.bs3.calculate_hourly_volume()}"  # 1 2

    def test_calculate_k15(self):
        assert self.bs1.calculate_k15() == 0.92, f"Expected {0.92}, but got {self.bs1.calculate_hourly_volume()}"
        assert self.bs2.calculate_k15() == 1, f"Expected {1}, but got {self.bs2.calculate_hourly_volume()}"
        assert self.bs3.calculate_k15() == 0.94, f"Expected {0.94}, but got {self.bs3.calculate_hourly_volume()}"
        assert self.bs4.calculate_k15() == 0.87, f"Expected {0.87}, but got {self.bs4.calculate_hourly_volume()}"

    def test_estimate_base_capacity(self):
        assert self.bs1.estimate_base_capacity() == 2225, f"Expected {2225}, but got {self.bs1.estimate_base_capacity()}"
        assert self.bs2.estimate_base_capacity() == 2115, f"Expected {2115}, but got {self.bs2.estimate_base_capacity()}"
        assert self.bs3.estimate_base_capacity() == 1960, f"Expected {1960}, but got {self.bs3.estimate_base_capacity()}"

    def test_calculate_ew(self):
        assert self.bs1.calculate_ew() == 1.14, f"Expected {1.14}, but got {self.bs1.calculate_ew()}"
        assert self.bs2.calculate_ew() == 1.15, f"Expected {1.15}, but got {self.bs2.calculate_ew()}"
        assert self.bs3.calculate_ew() == 1.34, f"Expected {1.34}, but got {self.bs3.calculate_ew()}"

    def test_calculate_flow(self):
        assert self.bs1.calculate_flow() == 929, f"Expected {929}, but got {self.bs1.calculate_flow()}"
        assert self.bs2.calculate_flow() == 4032, f"Expected {4032}, but got {self.bs2.calculate_flow()}"
        assert self.bs3.calculate_flow() == 1956, f"Expected {1956}, but got {self.bs3.calculate_flow()}"

    def test_calculate_utilization(self):
        assert self.bs1.calculate_utilization() == 0.42, f"Expected {0.42}, but got {self.bs1.calculate_utilization()}"
        assert self.bs2.calculate_utilization() == 1.91, f"Expected {1.91}, but got {self.bs2.calculate_utilization()}"
        assert self.bs3.calculate_utilization() == 1, f"Expected {1}, but got {self.bs3.calculate_utilization()}"

    def test_calculate_opt_speed(self):
        assert self.bs1.calculate_opt_speed() == 84, f"Expected {0.42}, but got {self.bs1.calculate_opt_speed()}"
        assert self.bs2.calculate_opt_speed() == 78.6, f"Expected {1.91}, but got {self.bs2.calculate_opt_speed()}"
        assert self.bs3.calculate_opt_speed() == 68.4, f"Expected {1}, but got {self.bs3.calculate_opt_speed()}"