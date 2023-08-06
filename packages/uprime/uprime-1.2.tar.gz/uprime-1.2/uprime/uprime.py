import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters
import logging

class Uprime:

    def __init__(self, source_df, sort_column_name, occurrences_column_name, subgroup_size_column_name,
                 method='all', periods=30, sd_sensitivity=3, ignore_ooc = True, ooc_rule ='either',
                 alert_name = None, realert_interval = 1, assumed_distribution = None):
        """
        :param source_df: Dataframe for which to create a u'-chart (A control chart for attributes data)
        :param sort_column_name: Column name in source_df that contains the chronological order of the points. Although
                                    this can be type int, date, or anything that will be sorted in chronological order,
                                    the chart() method used to plot control charts only supports datetime-like data
                                    as recognized by pandas.to_datetime().  If your data is not datetime-like, you may
                                    still use the DataFrame returned by the frame() method to create your own plot
                                    outside this module.
        :param occurrences_column_name: Column name in source_df that contains the number of occurences of
                                        the attribute of interest
        :param subgroup_size_column_name: Column name in source_df that contains the subgroup size for each row
        :param method: Method used to calculate u'-chart control limits. Can be 'all', 'rolling', or 'initial'
                            'all': Use all available data
                            'rolling': Use most recent rolling data (most recent X periods before current subgroup (set
                                        with "periods" parameter))
                            'initial': Use the first X periods available (Fixed interval from the first to the Xth
                                        period (set with periods parameter))
        :param periods: Number of periods to use for u'-chart calculation (only relevant when method is 'rolling' or
                        'initial')
        :param sd_sensitivity: Number of standard deviations away from the mean to set the control limits
        :param ignore_ooc: Only valid when method = 'rolling'
                            If True, ignore "out-of-control" (outside of control limits) points in calculating future
                            control limits.
                            Each ignored point is replaced with the most recent available unignored point.
                            (Note: The first X=periods points are never ignored)
        :param ooc_rule: Can be 'low', 'high', or 'either'
                            'low': alert only when point is below lower control limit
                            'high': alert only when point is above upper control limit
                            'either': alert when point is either 'low' or 'high'
        :param alert_name: User chosen name for the alert
        :param realert_interval: Supresses repeat alerts in consecutive periods before realerting.
                                    Example: Assume no subgroups fall outside of control limits until five consective
                                    subgroups in periods 6 through 10 are all outside of control limits.
                                    If realert_interval = 4, the alert column in the output DataFrame of the frame()
                                    method will only be True for 6 and 10.
                                    Alerts are supressed in periods 7, 8, and 9 because the interval between period 6
                                    (the first consecutive alert) and period 9 is lessthan 4.
                                    Default: 1 (this means that no alerts are suppressed.
        :param assumed_distribution: Default is None.
                                        Computation of sigma_z is skipped when assumed_distribution is None.
                                        Can be None, 'binomial', or 'Poisson'.
                                        The assumed underlying probability distribution for computing sigma_z.
                                        sigma_z is the ratio of total process variation to within-subgroup variation.
                                        When `method = rolling`, a different sigma_z value is calculated for each row
                                        and averaged to compute `self.sigma_z`.
                                        Otherwise, sigma_z is the same for all rows.
        """
        self.source_df = source_df
        self.sort_column_name = sort_column_name
        self.occurrences_columns_name = occurrences_column_name
        self.subgroup_size_column_name = subgroup_size_column_name
        self.periods = periods
        self.sd_sensitivity = sd_sensitivity
        self.ignore_ooc = ignore_ooc
        self.ooc_rule = ooc_rule
        self.alert_name = alert_name
        self.realert_interval = realert_interval
        self.method = method
        self.assumed_distribution = assumed_distribution
        self.sigma_z = None
        self.index_na_list = None
        self.chart_df = None

    def frame(self):
        """
        :return: A pandas DataFrame containing all the data required to plot a u'-chart
        """

        assert (self.periods > 0)
        assert (isinstance(self.periods, int))
        assert (self.sd_sensitivity > 0)
        assert (self.ooc_rule in ['low', 'high', 'either'])
        assert (self.method in ['all', 'rolling', 'initial'])
        assert (self.assumed_distribution in [None, 'binomial', 'Poisson'])

        # Create dataframe for u'-chart calculations
        df_raw = pd.concat([
            self.source_df[self.sort_column_name],
            self.source_df[self.occurrences_columns_name],
            self.source_df[self.subgroup_size_column_name]
        ], axis=1, keys=[self.sort_column_name, self.occurrences_columns_name, 'n_i'])

        # Sort df by date or period ascending
        df_raw = df_raw.sort_values(self.sort_column_name)
        df_raw = df_raw.set_index(self.sort_column_name)

        # Convert values to numeric, replacing any non coercible values with NaN
        numeric_cols = [self.occurrences_columns_name, 'n_i']
        df_raw[numeric_cols] = df_raw[numeric_cols].apply(pd.to_numeric, errors='coerce', axis=1)

        # Round any non-integer values
        df_raw = df_raw.round(decimals=0)

        # Drop any rows with NA values (which may have come from values non-coercible to numeric, or just missing values
        df = df_raw.dropna(axis=0, how='any')

        # Warn the user about dropped rows
        self.index_na_list = list(df_raw.index[~df_raw.index.isin(df.index)])
        if len(self.index_na_list) > 0:
            logging.warning(''' Ignoring the following subgroups because of NA values or non-numerically-coercible values:\n{}'''.format(self.index_na_list))

        if self.assumed_distribution == 'binomial':
            non_binomial_df = df_raw[df_raw[self.occurrences_columns_name] > df_raw['n_i']]
            if len(non_binomial_df) > 0:
                self.assumed_distribution = None
                logging.warning(" assumed_distribution cannot be 'binomial' because source_df contains rows where the number of occurences is greater than the subgroup size.")
                logging.warning(" assumed_distribution has been reset to None.")


        def control_chart_calculations(control_chart_df, periods_to_use):
            control_chart_df['u_i'] = 1.0 * control_chart_df[self.occurrences_columns_name] / control_chart_df['n_i']
            control_chart_df['u_iminus1'] = control_chart_df['u_i'].shift(1)
            control_chart_df['n_iminus1'] = control_chart_df['n_i'].shift(1)
            ubar = control_chart_df['u_i'].iloc[:periods_to_use].mean()
            control_chart_df['sd_summand_left_term'] = ((control_chart_df['n_i']) ** (0.5)) * (control_chart_df['u_i'] - ubar)
            control_chart_df['sd_summand_right_term'] = ((control_chart_df['n_iminus1']) ** (0.5)) * (control_chart_df['u_iminus1'] - ubar)
            control_chart_df['sd_summand'] = abs(control_chart_df['sd_summand_left_term'] - control_chart_df['sd_summand_right_term'])
            sd_summation = control_chart_df['sd_summand'][1:periods_to_use].sum()
            d_2 = 1.128
            w = sd_summation / (d_2 * (len(control_chart_df.iloc[:periods_to_use]) - 1))

            control_chart_df['sd'] = w / ((control_chart_df['n_i']) ** (0.5))
            control_chart_df['distance_to_control_limits'] = self.sd_sensitivity * control_chart_df['sd']
            control_chart_df['lcl'] = ubar - control_chart_df['distance_to_control_limits']
            control_chart_df['ucl'] = ubar + control_chart_df['distance_to_control_limits']
            control_chart_df['ubar'] = ubar

            if self.assumed_distribution:
                if self.assumed_distribution == 'binomial':
                    b = (1.0 - ubar) ** (0.5)
                elif self.assumed_distribution == 'Poisson':
                    b = 1.0
                self.sigma_z = w / (b * (ubar ** (0.5)))

                control_chart_df['sigma_z'] = self.sigma_z

            # Determining whether or not the current point is outside of control limits (ooc = out of control)
            control_chart_df['ooc_low'] = control_chart_df['u_i'] < control_chart_df['lcl']
            control_chart_df['ooc_high'] = control_chart_df['u_i'] > control_chart_df['ucl']
            control_chart_df['ooc'] = (control_chart_df['ooc_low'] == True) | (control_chart_df['ooc_high'] == True)

            # Determining if the out-of-control rule set by the user is broken
            if self.ooc_rule == 'either':
                control_chart_df['potential_alert'] = control_chart_df['ooc']
            elif self.ooc_rule == 'high':
                control_chart_df['potential_alert'] = control_chart_df['ooc_high']
            elif self.ooc_rule == 'low':
                control_chart_df['potential_alert'] = control_chart_df['ooc_low']

            return control_chart_df

        if self.method == 'all':
            chart_df = control_chart_calculations(df.copy(), len(df))

        elif self.method == 'initial':
            chart_df = control_chart_calculations(df.copy(), self.periods)

        elif self.method == 'rolling':
            ignore_index_values = []

            # Loop starting at period index self.periods + 1 {i=0, period=31}
            # This ensures that we have enough data to make our first observation based on past data
            for i, period in enumerate(range(self.periods + 1, len(df) + 1)):

                # Add 1 to the length of the df_slice for every index value to be ignored
                # This will make sure we still have a number of unignored indices equal to self.periods
                # {df_slice contains rows 0 through 30}
                df_slice = df.iloc[(i - len(ignore_index_values)):period].copy()

                # Get the number of previous periods that will be used in calculating current point
                # {31 - 0 - 1 = 30}
                #previous_periods_used = len(df_slice) - len(ignore_index_values) - 1

                indicies_to_delete_from_ignore_index_values = []

                if len(ignore_index_values) > 0:

                    # Check to see if the first index value in df_slice is in the ignore_index_value list
                    if df_slice.index[0] == ignore_index_values[0]:

                        # If true, add all the consecutive leading ignored values into a list
                        for j in range(len(ignore_index_values)):
                            if df_slice.index[j] == ignore_index_values[j]:
                                indicies_to_delete_from_ignore_index_values.append(j)
                            else:
                                break

                    # Remove from df slice where index is in ignore_index_values
                    # We do this to ignore out of bounds points in calculating new control limits
                    df_slice = df_slice[~df_slice.index.isin(ignore_index_values)].copy()

                    # Remove all the leading ignored index values from the ignore_index_values
                    if len(indicies_to_delete_from_ignore_index_values) > 0:
                        indicies_to_delete_from_ignore_index_values.reverse()
                        for k in indicies_to_delete_from_ignore_index_values:
                            del ignore_index_values[k]

                wip_df = control_chart_calculations(df_slice, -1)
                if i == 0:
                    chart_df = wip_df.iloc[-1].to_frame().T
                else:
                    chart_df = chart_df.append(wip_df.iloc[-1].to_frame().T)

                if self.ignore_ooc:
                    # Ignore the current point in future calculations if it is out-of-control
                    if wip_df['ooc'].iloc[-1]:
                        ignore_index_values.append(wip_df.index[-1])

            if self.assumed_distribution:
                self.sigma_z = chart_df['sigma_z'].mean()

        chart_df.sort_index(inplace=True)
        chart_df['alert_name'] = self.alert_name
        chart_df['ooc_rule'] = self.ooc_rule

        # Realert rules
        chart_df['segment'] = ((chart_df['potential_alert'] != chart_df['potential_alert'].shift()).cumsum())
        chart_df['segment_row'] = chart_df.groupby('segment').cumcount()
        chart_df['realert_modulo'] = chart_df['segment_row'].mod(self.realert_interval)
        chart_df['suppress_realert'] = (chart_df['potential_alert'] == True) & (chart_df['realert_modulo'] != 0)
        chart_df['alert'] = (chart_df['potential_alert'] == True) & (chart_df['suppress_realert'] == False)

        # Order cols for output and eliminate intermediate calculation columns
        chart_df = chart_df[['alert_name', self.occurrences_columns_name, 'n_i', 'u_i', 'lcl', 'ubar', 'ucl', 'ooc_low',
                             'ooc_high', 'ooc', 'ooc_rule', 'potential_alert', 'suppress_realert', 'alert']]

        self.chart_df = chart_df
        return self.chart_df

    def chart(self, show = False, plot_title = u"u\u2032-chart"):
        """
        Returns a matplotlib plot of a control chart
        This method is only supported when the data in the sort column is of a datetime-like format as recognized by
        pandas.to_datetime()
        :param show: If True then show and return figure.  If false only return figure.
        :param plot_title: string value for the title of the plot.  Default = "u′-chart"
        :return: <class 'matplotlib.figure.Figure'> of u'-chart
        """

        assert (self.chart_df is not None)

        register_matplotlib_converters()

        self.chart_df.index = pd.to_datetime(self.chart_df.index)

        in_control = self.chart_df[self.chart_df['potential_alert'] == False]
        suppress_high_low = self.chart_df[(self.chart_df['ooc'] == True) & (self.chart_df['potential_alert'] == False)]
        suppress_realert = self.chart_df[self.chart_df['suppress_realert'] == True]
        alert = self.chart_df[self.chart_df['alert'] == True]

        fig = plt.figure(figsize=(16, 8))

        #Use "fake" transparent line to add sigma_z to legend
        if self.assumed_distribution:
            subscript_z = r'$_z$'
            sigma_z_rounded = round(self.sigma_z, 2)
            if self.method == 'rolling':
                sigma_z_text = '{}{} = {}'.format(u'\u03C3\u0305', subscript_z, sigma_z_rounded)
            else:
                sigma_z_text = '{}{} = {}'.format(u'\u03C3', subscript_z, sigma_z_rounded)

            plt.plot(self.chart_df.index, self.chart_df['ubar'], color='black', linestyle='--', alpha=0.0, label=sigma_z_text)

        groups = [in_control, suppress_high_low, suppress_realert, alert]
        colors = ['mediumseagreen', 'dimgray', 'coral', 'firebrick']
        labels = ['In Control', 'Hi/Lo Suppressed', 'Realert Suppressed', 'Alert (Out of Control)']

        for row_group in zip(groups, colors, labels):
            if len(row_group[0]) > 0:
                plt.plot(row_group[0].index, row_group[0]['u_i'], linestyle='None', marker='o', color=row_group[1], label = row_group[2])

        plt.plot(self.chart_df.index, self.chart_df['ucl'], color='black', label='Upper Control Limit (UCL)')
        plt.plot(self.chart_df.index, self.chart_df['ubar'], color='black', linestyle='--', label=u'u\u0305 (Mean)')
        plt.plot(self.chart_df.index, self.chart_df['lcl'], color='black', label='Lower Control Limit (LCL)')
        plt.xlabel(self.sort_column_name, fontsize=16)
        plt.ylabel(self.occurrences_columns_name, fontsize=16)
        plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', ncol=1)
        plt.title(plot_title, fontsize=20)
        plt.tight_layout()
        plt.grid()

        if show:
            plt.show()

        return fig