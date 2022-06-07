import pandas as pd
from dash_spa.components.table import filter_df

df = pd.read_csv('pages/data/customers.csv')

#
# https://json-generator.com/#
# https://www.convertcsv.com/json-to-csv.htm
#
# [
#   '{{repeat(300, 300)}}',
#   {
#     index: '{{index()}}',
#     isActive: '{{bool()}}',
#     balance: '{{floating(1000, 4000, 2, "$0,0.00")}}',
#     age: '{{integer(20, 40)}}',
#     eyeColor: '{{random("blue", "brown", "green")}}',
#     name: '{{firstName()}} {{surname()}}',
#     gender: '{{gender()}}',
#     company: '{{company().toUpperCase()}}',
#     email: '{{email()}}',
#     phone: '+1 {{phone()}}',
#     address: '{{integer(100, 999)}} {{street()}}, {{city()}}, {{state()}}, {{integer(100, 10000)}}',
#     registered: '{{date(new Date(2014, 0, 1), new Date(), "YYYY-MM-ddThh:mm:ss Z")}}',
#   }
# ]

def test_simple():

    assert len(df) == 300

    result = filter_df(df, "{isActive} eq true")
    assert len(result) == 160

    result = filter_df(df, "{isActive} eq true && {eyeColor} eq blue")
    assert len(result) == 45


