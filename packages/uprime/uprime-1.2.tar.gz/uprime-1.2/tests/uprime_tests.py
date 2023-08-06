import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from uprime import Uprime
import pandas as pd


directory = os.path.dirname(os.path.realpath(__file__))
relative_file_path = 'uprime_test_data.csv'
full_path = os.path.join(directory, relative_file_path)
df = pd.read_csv(full_path)

def ooc_stats(chart_dataframe):
    ooc = len(chart_dataframe[chart_dataframe['ooc'] == True])
    ooc_low = len(chart_dataframe[chart_dataframe['ooc_low'] == True])
    ooc_high = len(chart_dataframe[chart_dataframe['ooc_high'] == True])
    potential_alert = len(chart_dataframe[chart_dataframe['potential_alert'] == True])
    suppress_realert = len(chart_dataframe[chart_dataframe['suppress_realert'] == True])
    alert = len(chart_dataframe[chart_dataframe['alert'] == True])

    return {'ooc': ooc, 'ooc_low': ooc_low, 'ooc_high': ooc_high, 'potential_alert': potential_alert,
            'suppress_realert': suppress_realert, 'alert': alert}

class UprimeTester(unittest.TestCase):

    def setUp(self):
        pass

    def test_rolling_periods(self):
        up = Uprime(df, 'date', 'occurrences', 'subgroup_size', method='rolling', periods=41)
        up_df = up.frame()
        self.assertEqual(len(up_df), len(df) - up.periods - len(up.index_na_list))

    def test_initial_periods(self):
        up = Uprime(df, 'date', 'occurrences', 'subgroup_size', method='initial', periods=22)
        up_df = up.frame()
        self.assertEqual(len(up_df), len(df) - len(up.index_na_list))

    def test_all_periods(self):
        up = Uprime(df, 'date', 'occurrences', 'subgroup_size', method='all', periods=1000)
        up_df = up.frame()
        self.assertEqual(len(up_df), len(df) - len(up.index_na_list))

    def test_exclusions(self):
        up = Uprime(df, 'date', 'occurrences', 'subgroup_size', method='all')
        up.frame()
        self.assertEqual(['2019-06-10', '2019-06-12', '2019-06-14', '2019-06-16', '2019-06-27', '2019-06-28'], up.index_na_list)

    def test_sort(self):
        up = Uprime(df, 'date', 'occurrences', 'subgroup_size')
        up.frame()
        pd.testing.assert_frame_equal(up.chart_df, up.chart_df.sort_index())

    def test_sd_sensitivity(self):
        up_adjusted_sd_sensitivity = Uprime(df, 'date', 'occurrences', 'subgroup_size', sd_sensitivity=4.23)
        up_adjusted_sd_sensitivity.frame()

        up = Uprime(df, 'date', 'occurrences', 'subgroup_size')
        up.frame()

        pd.testing.assert_series_equal((up.chart_df['ucl'] - up.chart_df['ubar'])*(4.23/3.0),
                                       (up_adjusted_sd_sensitivity.chart_df['ucl'] - up_adjusted_sd_sensitivity.chart_df['ubar']))
        pd.testing.assert_series_equal((up.chart_df['ubar'] - up.chart_df['lcl'])*(4.23/3.0),
                                       (up_adjusted_sd_sensitivity.chart_df['ubar'] - up_adjusted_sd_sensitivity.chart_df['lcl']))

    def test_ooc(self):
        up_rolling = Uprime(df, 'date', 'occurrences', 'subgroup_size', method='rolling', periods=30, realert_interval=4, ooc_rule='high')
        up_rolling.frame()
        ooc_rolling = ooc_stats(up_rolling.chart_df)

        up_initial = Uprime(df, 'date', 'occurrences', 'subgroup_size', method='initial', periods=30, realert_interval=4, ooc_rule='high')
        up_initial.frame()
        ooc_initial = ooc_stats(up_initial.chart_df)

        up_all = Uprime(df, 'date', 'occurrences', 'subgroup_size', method='all', realert_interval=4, ooc_rule='high')
        up_all.frame()
        ooc_all = ooc_stats(up_all.chart_df)


        def ooc_assertions(oocs):
            self.assertEqual(9, oocs['ooc'], oocs['ooc_low'] + oocs['ooc_high'])
            self.assertEqual(8, oocs['potential_alert'])
            self.assertEqual(6, oocs['suppress_realert'])
            self.assertEqual(2, oocs['alert'])

        ooc_assertions(ooc_rolling)
        ooc_assertions(ooc_initial)
        ooc_assertions(ooc_all)

if __name__ == '__main__':
    unittest.main()