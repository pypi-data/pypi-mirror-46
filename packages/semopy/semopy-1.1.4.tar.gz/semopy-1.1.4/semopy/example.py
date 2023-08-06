import pandas as pd
import os


__mod = '''# structural part
eta3 ~ x1 + x2
eta4 ~ x3
x3 ~ eta1 + eta2 + x1 + x4
x4 ~ eta4
x5 ~ x4
# measurement part
eta1 =~ y1 + y2 + y3
eta2 =~ y3
eta3 =~ y4 + y5
eta4 =~ y4 + y6
# additional covariances
eta2 ~~   x2
y5 ~~   y6'''

def get_model():
    global __mod
    return __mod

def get_data():
    d = os.path.dirname(os.path.abspath(__file__))
    data = pd.read_csv('{}/example_data.txt'.format(d), sep=',', indexcol=0)
    return data
