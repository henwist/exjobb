#use https://pypi.python.org/pypi/hcsr04sensor/1.2.0 already programmed library.
from sklearn.ensemble import RandomForestRegresssor as rf
import sqlite3
import datetime

def main():

if __name__ == '__main__':
    main()


 def getPrediction():
     model = getData()
     rf.fit(model)
     return rf.predict()

 def getData():
     conn = sqlite3.connect('placeholder.db')
     cursor = conn.cursor

     curTime = datetime.datetime.now().time()
     c.execute('''SELECT * WHERE time<=? || time>?''', curTime, curTime - (0, 10, 0, 0, 0))
