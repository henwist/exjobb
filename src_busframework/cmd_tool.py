import sqlite3 as sq
import argparse as ap


parser = ap.ArgumentParser()
parser.add_argument("-r", "--retrieve", help="Return all modules in the module database")
parser.add_argument("-s","--send", help="Takes an sql statement and executes it on the database")
parser.add_argument("db", help="The database on which operations will be executed")

args = parser.parse_args()
if args.send:
    con = sq.connect(args.db)
    cur = con.cursor()
    cur.execute(args.send)
    con.commit()
    con.close()
