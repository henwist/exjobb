#use https://pypi.python.org/pypi/hcsr04sensor/1.2.0 already programmed library.
from sklearn.ensemble import RandomForestRegresssor as rf
import sqlite3
import datetime
import src_busframework as bf
import numpy

class visitor_counter:
    conn
    cursor
    visitor_count

    def __init__(db='placeholder.db'):
        self.conn = sqlite3.connect(db)
        self.cursor = self.conn.cursor

    def main():
        ultrasoundsensor1 = new bf.i2c_bus(1)
        ultrasoundsensor2 = new bf.i2c_bus(2)
        tempsensor = new bf.i2c_bus(3)
        pressensor = new bf.i2c_bus(4)

        #Detta bör antagligen köras i en egen tråd om möjligt annars behöver vi nog hitta ett annat
        #sätt att göra det på.
        if (ultrasoundsensor1.activated):
            values = ultrasoundsensor1.read()
            values.append(',')
            values.append(ultrasoundsensor2.read())
            values.append(',')
            values.append(tempsensor.read())
            values.append(',')
            values.append(pressensor.read())
            values.append(',')
            values.append(visitor_count++)
            cursor.execute('''INSERT INTO visistor_data VALUES (?, ?, ?, ?, ?)''', values)

        elif(ultrasoundsensor2.activated):
            visitor_count--

        # Sen behöver vi göra prediktioner regelbundet, kanske hårdkoda det till var tionde minut.
        # Alternativt skulle vi kunna göra prediktioner efter var tionde besökare efter att tillräckligt
        # många besökare anlänt för att vi ska kunna börja predicera.

    if __name__ == '__main__':
        main()


     def getPrediction():
         model = getData()
         n_features = model.shape[0]
         n_samples = model.shape[1]
         esitmator = rf.RandomForestRegresssor(numpy.random.ranomstate(0), n_estimators = 1000)
         estimator.fit(model)
         return estimator.predict(n_features, n_samples)

     def getData():
         curTime = datetime.datetime.now().time()
         self.cursor.execute('''SELECT * WHERE time<=? || time>?''', curTime, curTime - (0, 10, 0, 0, 0))


     def initDb(name):

         self.cursor.execute('''CREATE TABLE ?''', name)
