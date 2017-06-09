#
# Database manager for handling transactions with mongodb
#

from pymongo import MongoClient


class Mdb:

    def __init__(self, host, port, authdb, dbname, dbuser, dbpass):
        conn_str = "mongodb://%s:%s@%s:%d/%s" \
                   % (dbuser, dbpass,
                      host, port, authdb)
        client = MongoClient(conn_str)
        self.db = client[dbname]

        print "[Mdb] connected to database :: ", self.db

    def add_vacancy(self, title, location, salary, summary):
        rec = {
            'title': title,
            'location': location,
            'salary': salary,
            'summary': summary
        }
        self.db.job_vacancy.insert(rec)


if __name__ == "__main__":
    # quick test connecting to localdb
    mdb = Mdb('127.0.0.1', 27017, 'admin', 'carrermaker', 'admin', '123')
    # mdb.add_vacancy('weaveBytes', 'kharar', '10000', 'its python job')
