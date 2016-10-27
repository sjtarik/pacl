import os
import json
import datetime


class VersionDropbox():

    def __init__(self, file_name):
        self.db = {}
        self.filename = file_name
        self.version = 0
        dt = datetime.datetime.now()
        self.timestamp = str(dt.replace(microsecond=0))

    def load_database(self):
        if not os.path.isfile(self.filename):
            self.db["history"] = [{"$version": self.version, "$timestamp": self.timestamp}]
            with open(self.filename, "w") as f:
                try:
                    json.dump(self.db, f, indent=4)
                except Exception as e:
                    print str(e) + " during initializing version db"
                    raise e
        with open(self.filename, "rw") as f:
            try:
                self.db = json.load(f)
                if "history" not in self.db:
                    raise Exception("Unexpected format for version db " + self.filename)
                if not self.db["history"]:
                    raise Exception("Empty version history unexpected " + self.filename)

                last_version = self.db["history"][-1]
                if "$version" not in last_version or "$timestamp" not in last_version:
                    raise Exception("Unexpected format for revision history " + self.filename)
                self.version = last_version["$version"] + 1
            except Exception as e:
                print str(e) + " during initializing version db"
                raise e

    def get_version_timestamp(self):
        return {"$version": self.version, "$timestamp": self.timestamp}

    def close_database(self, append_last_version):
        if append_last_version:
            with open(self.filename, "w") as f:
                try:
                    self.db["history"].append({"$version": self.version, "$timestamp": self.timestamp})
                    json.dump(self.db, f, indent=4)
                except Exception as e:
                    print "Error while persisting version db " + str(e)

if __name__ == '__main__':
    vp = VersionDropbox("./policy_version_db.json")
    vp.load_database()
    version_dict = vp.get_version_timestamp()
    print str(version_dict["$version"]) + " " + version_dict["$timestamp"]
    vp.close_database(True)
