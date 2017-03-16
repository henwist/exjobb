from sklearn.ensemble import RandomForestRegressor
import numpy as np

import datetime

dt = datetime.datetime
td = datetime.timedelta

cdt = dt.now()
X=[]

X.append([cdt.year, cdt.month, cdt.day, cdt.weekday(), cdt.hour, cdt.minute//10])

cdt += td(0,11,0,0,55,0,0)
X.append([cdt.year, cdt.month, cdt.day, cdt.weekday(), cdt.hour, cdt.minute//10])

cdt += td(0,1,0,0,16,0,0)
X.append([cdt.year, cdt.month, cdt.day, cdt.weekday(), cdt.hour, cdt.minute//10])

cdt += td(0,6,0,0,15,0,0)
X.append([cdt.year, cdt.month, cdt.day, cdt.weekday(), cdt.hour, cdt.minute//10])

cdt += td(0,5,0,0,12,0,0)
X.append([cdt.year, cdt.month, cdt.day, cdt.weekday(), cdt.hour, cdt.minute//10])

cdt += td(0,14,0,0,15,0,0)
X.append([cdt.year, cdt.month, cdt.day, cdt.weekday(), cdt.hour, cdt.minute//10])

cdt += td(0,11,0,0,55,0,0)
X.append([cdt.year, cdt.month, cdt.day, cdt.weekday(), cdt.hour, cdt.minute//10])

cdt += td(0,5,0,0,15,0,0)
X.append([cdt.year, cdt.month, cdt.day, cdt.weekday(), cdt.hour, cdt.minute//10])

cdt += td(0,2,0,0,12,0,0)
X.append([cdt.year, cdt.month, cdt.day, cdt.weekday(), cdt.hour, cdt.minute//10])

print X

y = [1.256400,
     1.430750,
     1.369910,
     1.359350,
     1.305680,
     1.287750,
     1.245970,
     1.282280,
     1.365710]

#warm_start=True is not supported on current sklearn
model = RandomForestRegressor(n_estimators=100, max_depth=2)
model.fit(np.array(X), y)

#model.fit(np.array(X).reshape(-1,1), y)

X_predict = []

cdt += td(0,2,0,0,12,0,0)
X_predict.append([cdt.year, cdt.month, cdt.day, cdt.weekday(), cdt.hour, cdt.minute//10])

cdt += td(0,11,0,0,15,0,0)
X_predict.append([cdt.year, cdt.month, cdt.day, cdt.weekday(), cdt.hour, cdt.minute//10])

cdt += td(0,10,0,0,15,0,0)
X_predict.append([cdt.year, cdt.month, cdt.day, cdt.weekday(), cdt.hour, cdt.minute//10])

y_predict = model.predict(np.array(X_predict))

print "prediction: ", y_predict
