from pynwb.epoch import TimeIntervals
import pandas as pd

TimeIntervals.from_dataframe(pd.DataFrame(
    {'start_time': [.1, 2.], 'stop_time': [.8, 2.3], 'label': ['hello', 'there']}), name='name')