#use https://pypi.python.org/pypi/hcsr04sensor/1.2.0 already programmed library.
from sklearn.ensemble import RandomForestRegresssor as rf
import sqlite3
import datetime


class visitor_counter:
    conn
    cursor

    def __init__(db='placeholder.db'):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor

    def main():

    if __name__ == '__main__':
        main()


     def getPrediction():
         model = getData()
         rf.fit(model)
         return rf.predict()

     def getData():
         curTime = datetime.datetime.now().time()
         self.cursor.execute('''SELECT * WHERE time<=? || time>?''', curTime, curTime - (0, 10, 0, 0, 0))


     def insertRow():
         values = sensors.read()
         self.cursor.execute('''INSERT INTO visitor_data VALUES (?,?,?)''', values)


     def initDb(name):

         self.cursor.execute('''CREATE TABLE visitor_data(?, ?)''')
