import pandas as pd
import numpy as np
from locust import runners


from .display import WARN, DEBUG
from .core import LocustEndpointCollection



class Insight(object):
    singleton = False

    def __init__(self):
        collection = LocustEndpointCollection()
        self.container = collection.endpoint_statistics
        self.n_requests = collection.totals
        colorder = ['Name', 'Calls', 'API_Usage', 
                    'Success_Rate', 'Median', 
                    'Percentile_95', 'Quartile_Q1', 
                    'Quartile_Q3', 'IQR']

        self.data = {
            'Name' : [],
            'Calls': [],
            'API_Usage': [],
            'Success_Rate': [],
            'Percentile_95':[],
            'Quartile_Q1': [],
            'Median': [],
            'Quartile_Q3': [],
            'IQR': []
        }
        self.insights = dict()
        for frame in self.container:
            df = self.container[frame]

            calls   = self.i_call_count(df)
            usage   = self.i_api_usage(calls)
            s_rate  = self.i_success_rate(df, calls)
            percentile = self.i_percentile(df)
            quartile_gen = self.i_quartile(df)
            Q1      = next(quartile_gen)
            med     = next(quartile_gen)
            Q3      = next(quartile_gen)

            self.data['Name'].append(frame)
            self.data['Calls'].append(calls)
            self.data['API_Usage'].append(usage)
            self.data['Success_Rate'].append(s_rate)
            self.data['Percentile_95'].append(percentile)
            self.data['Quartile_Q1'].append(Q1)
            self.data['Median'].append(med)
            self.data['Quartile_Q3'].append(Q3)
            self.data['IQR'].append(Q3 - Q1)
        
        final = pd.DataFrame(self.data)
        # final.set_index('Name', inplace=True)
        final = final[colorder]
        # final.to_html('statistics.html', index=False)
        final.to_csv(path_or_buf='stats.csv')
        
    
    def i_call_count(self, df):
        return len(df.index)

    def i_api_usage(self, callcount):
        return round((float(callcount) / float(self.n_requests)) * 100.0, 1)

    def i_success_rate(self, df, calls):
        n_success   = len(df[(df['status'] == True)].index)
        return round((float(n_success) / float(calls)) * 100.0, 1)

    def i_percentile(self, df):
        return round(np.percentile(df.response_time, 95), 3)

    def i_quartile(self, df):
        for x in [25, 50, 75]:
            yield round(np.percentile(df.response_time, x), 3)



    def __new__(cls, *args, **kwargs):
        if Insight.singleton == False:
            Insight.singleton = True
            return object.__new__(cls, *args, **kwargs)
        return