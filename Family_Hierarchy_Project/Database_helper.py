import sqlite3


class DB:
    def __init__(self):
        self.connection = sqlite3.connect("family.db")
        self.connection.execute("PRAGMA foreign_keys = 1")
        self.crsr = self.connection.cursor()

        print("Connected to the Database")

        self.create_table()
        print("Table Created")

    def create_table(self):
        self.crsr.execute("DROP TABLE IF EXISTS PERSON")
        sql_command = """CREATE TABLE Person (
                        id INTEGER PRIMARY KEY,
                        first_name VARCHAR(20),
                        last_name VARCHAR(20),
                        gender CHAR(1),
                        dob DATE,
                        dod DATE,
                        father_id INTEGER,
                        mother_id INTEGER,
                        FOREIGN KEY (father_id) REFERENCES Person(id),
                        FOREIGN KEY (mother_id) REFERENCES Person(id));"""
        self.crsr.execute(sql_command)

    def add_data(self, id, first_name, last_name, gender, dob, dod, father_id, mother_id):
        sql_command = f"INSERT INTO PERSON VALUES (?, ?, ?, ?, ?, ?, ?, ?) "
        data = (id, first_name, last_name, gender, dob, dod, father_id, mother_id)
        self.crsr.execute(sql_command, data)
        self.connection.commit()
        print("Data added successfully")

    def update_first_name(self, id, first_name):
        if first_name is None:
            sql_command = f"UPDATE Person SET first_name = NULL WHERE id = {id}"
        else:
            sql_command = f"UPDATE Person SET first_name = {first_name} WHERE id = {id}"
        self.crsr.execute(sql_command)

    def update_last_name(self, id, last_name):
        if last_name is None:
            sql_command = f"UPDATE Person SET last_name = NULL WHERE id = {id}"
        else:
            sql_command = f"UPDATE Person SET last_name = '{last_name}' WHERE id = {id}"
        self.crsr.execute(sql_command)

    def update_gender(self, id, gender):
        if gender is None:
            sql_command = f"UPDATE Person SET gender = NULL WHERE id = {id}"
        else:
            sql_command = f"UPDATE Person SET gender = '{gender}' WHERE id = {id}"
        self.crsr.execute(sql_command)

    def update_dob(self, id, dob):
        if dob is None:
            sql_command = f"UPDATE Person SET dob = NULL WHERE id = {id}"
        else:
            sql_command = f"UPDATE Person SET dob = {dob} WHERE id = {id}"
        self.crsr.execute(sql_command)

    def update_dod(self, id, dod):
        if dod is None:
            sql_command = f"UPDATE Person SET gender = NULL WHERE id = {id}"
        else:
            sql_command = f"UPDATE Person SET gender = {dod} WHERE id = {id}"

        self.crsr.execute(sql_command)

    def update_father_id(self, id, father_id):
        if father_id is None:
            sql_command = f"UPDATE Person SET father_id = NULL WHERE id = {id}"
        else:
            sql_command = f"UPDATE Person SET father_id = {father_id} WHERE id = {id}"

        self.crsr.execute(sql_command)

    def update_mother_id(self, id, mother_id):
        if mother_id is None:
            sql_command = f"UPDATE Person SET mother_id = NULL WHERE id = {id}"
        else:
            sql_command = f"UPDATE Person SET mother_id = {mother_id} WHERE id = {id}"

        self.crsr.execute(sql_command)

    def update_tuple(self, id, first_name="$", last_name="$", gender="$", dob="$", dod="$", father_id="$", mother_id="$"):
        if first_name != "$":
            self.update_first_name(id, first_name)
        if last_name != "$":
            self.update_last_name(id, last_name)
        if gender != "$":
            self.update_gender(id, gender)
        if dob != "$":
            self.update_dob(id, dob)
        if dod != "$":
            self.update_dod(id, dod)
        if father_id != "$":
            self.update_father_id(id, father_id)
        if mother_id != "$":
            self.update_mother_id(id, mother_id)

        self.connection.commit()

        print("Values updated successfully")

    def delete_tuple(self, delete_id):
        self.crsr.execute(f"SELECT id FROM Person WHERE mother_id == {delete_id}")
        output = self.crsr.fetchall()
        if len(output):
            for id in output:
                id = id[0]
                self.update_mother_id(id, mother_id=None)
        else:
            self.crsr.execute(f"SELECT id FROM Person WHERE father_id == {delete_id}")
            output = self.crsr.fetchall()
            for id in output:
                id = id[0]
                self.update_father_id(id, father_id=None)

        self.crsr.execute(f"DELETE FROM Person WHERE id = {delete_id}")

        self.connection.commit()

        print("Deletion is Successful")

    def calculate_unique_person(self, ):
        sql_command = "SELECT count(id) from Person"
        self.crsr.execute(sql_command)
        output = self.crsr.fetchall()
        print(output)
        return output

    def close_db(self):
        self.connection.close()
        print("Connection closed")


if __name__ == "__main__":
    db_engine = DB()

    try:
        db_engine.add_data(1, "sidhant", "chauhan", "M", "1999-12-02", None, None, None)
    except sqlite3.Error as e:
        print(e)

    try:
        db_engine.add_data(2, "Madhu", "Rana", "F", "1972-11-22", None, None, None)
    except sqlite3.Error as e:
        print(e)

    try:
        db_engine.add_data(3, "Sanjeev", "Chauhan", "M", None, None, None, None)
    except sqlite3.Error as e:
        print(e)

    try:
        db_engine.add_data(4, "Savitri", "Rana", "F", "1950-01-01", None, None, None)
    except sqlite3.Error as e:
        print(e)

    try:
        db_engine.update_tuple(1, father_id=8)
    except sqlite3.Error as e:
        print(e)

    try:
        db_engine.update_tuple(1, father_id=3, mother_id=6)
    except sqlite3.Error as e:
        print(e)

    try:
        db_engine.update_tuple(1, father_id=3)
    except sqlite3.Error as e:
        print(e)

    try:
        db_engine.update_tuple(1, father_id=3, mother_id=2)
    except sqlite3.Error as e:
        print(e)

    try:
        db_engine.update_tuple(2, mother_id=4)
    except sqlite3.Error as e:
        print(e)

    try:
        db_engine.delete_tuple(3)
    except sqlite3.Error as e:
        print(e)

    try:
        db_engine.delete_tuple(2)
    except sqlite3.Error as e:
        print(e)

    # try:
    #     db_engine.delete_tuple(4)
    # except sqlite3.Error as e:
    #     print(e)

    try:
        db_engine.calculate_unique_person()
    except sqlite3.Error as e:
        print(e)