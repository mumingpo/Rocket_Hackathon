import pandas as pd

path = "./csv_hma/psam_h25.csv"
boston_puma_codes = ["03301", "03302", "03303", "03304", "03305", "03306", "03400"]

def load_data():
  with open("./csv_hma/psam_h25.csv", 'r') as f:
    df = pd.read_csv(f)
  ## all the entries with matching area code in PUMA
  view = df[df["PUMA"].isin(["03301", "03302", "03303", "03304", "03305", "03306", "03400"])]
  ## all the entries with rent
  view = view[view["RNTP"].notnull()]

  return view
  
def housing_price(df):
  inflation = {2013:1.054015, 2014:1.036463, 2015:1.034680, 2016:1.021505, 2017:1.}
  for rooms in range(1, 6):
    s = 0
    view = df[df["BDSP"] == rooms]
    for year in range(2013, 2018):
      view2 = view[round(view["SERIALNO"]/1000000000) == year]
      #print(rooms, year)
      #print(view2["RNTP"].describe())
      s += view2["RNTP"].describe()["25%"]*inflation[year]
  
    print("{} room: {}".format(rooms, s/5))