import unittest
import os
from simulate_realtime_to_csv import simulate_realtime_to_csv

class TestSimulation(unittest.TestCase):
    def test_simulation(self):
        realtime_file = simulate_realtime_to_csv(season_year="2024", month="11", day="25", output_file="realtime_data.csv")
        self.assertTrue(os.path.exists("realtime_data.csv"))
        get_time = lambda f: os.stat(f).st_mtime

        fn = realtime_file
        prev_time = get_time(fn)
        for i in range(3):
            self.assertNotEqual(get_time(fn), prev_time)
            prev_time = get_time(fn)
            time.sleep(20)

if __name__ == "__main__":
    unittest.main()

