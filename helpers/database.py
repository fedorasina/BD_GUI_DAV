import psycopg2
from psycopg2 import sql
import guihelper as guihelper
import os
import sys

params = []

def connect(config):

        try:
            conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (config[0], config[1], config[2], config[3]))
            return True
        except:
            return False

def viewColumnNames(table):
    try:
        # VIEW A TABLE
        params = guihelper.getConfig()
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (params[0], params[1], params[2], params[3]))
        cur = conn.cursor()
        cur.execute('SELECT * FROM '+ table + ' FETCH FIRST 1 ROW ONLY')
        colnames = [desc[0] for desc in cur.description]
        guihelper.setColumnNames(colnames)
        output = f'Success. Column names of {table} are fetched.'
        return output
    except:
        err = 'Error. Table or View does not exist or cant be selected due to access level.'
        return err


def viewrange(table, pointer, data_dict={}, data_inside={}):
    try:
        params = guihelper.getConfig()
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (params[0], params[1], params[2], params[3]))
        cur = conn.cursor()
        order_by_first_column = " ORDER BY "+guihelper.getColumnNames()[0]
        condition = ' WHERE '
        condits=[]
        for item in data_dict:
            if data_inside[item] != '':
                text = ''
                if data_dict[item] == 'integer':
                    text = item + '=' + str(data_inside[item])
                if data_dict[item] == 'character varying':
                    text = item +' LIKE ' + "'%"+data_inside[item]+"%'"
                condits.append(text)

        if len(condits)!= 0:
            condition += ' AND '.join(condits)
            cur.execute('SELECT * FROM '+ table + condition + order_by_first_column + ' OFFSET ' + str(pointer) + ' FETCH FIRST 10 ROW ONLY ')
            #guihelper.addToQueryHistory('SELECT * FROM '+ table + condition + order_by_first_column + ' OFFSET ' + str(pointer) + ' FETCH FIRST 10 ROW ONLY ')
        else:
            cur.execute('SELECT * FROM '+ table + order_by_first_column + ' OFFSET ' + str(pointer) + ' FETCH FIRST 10 ROW ONLY ')
            #guihelper.addToQueryHistory('SELECT * FROM '+ table + order_by_first_column + ' OFFSET ' + str(pointer) + ' FETCH FIRST 10 ROW ONLY ')

        all = cur.fetchall()
        guihelper.setData(all)
        return 'Success!'

    except psycopg2.Error as e:
        err = 'Error selecting. Probably access level.'
        print(e)
        return err


def createNewUser(user, pwd):
    try:
        # VIEW A TABLE
        params = guihelper.getConfig()
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (params[0], params[1], params[2], params[3]))
        cur = conn.cursor()
        cur.execute("CREATE USER "+user+" WITH PASSWORD '"+pwd+"';")
        cur.execute("GRANT SELECT ON ALL TABLES IN SCHEMA public TO " +user+ ";")
        guihelper.addToQueryHistory("CREATE USER "+user+" WITH PASSWORD '"+pwd+"';")
        guihelper.addToQueryHistory("GRANT SELECT ON ALL TABLES IN SCHEMA public TO " +user+ ";")
        conn.commit()

    except psycopg2.Error as e:
        err = 'Error creating user.'
        print(e)
        return err

def insert(table):
    try:
        # VIEW A TABLE
        params = guihelper.getConfig()
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (params[0], params[1], params[2], params[3]))
        cur = conn.cursor()
        values = guihelper.getListToInsert()
        for index in range(len(values)):
            values[index] = "'"+values[index]+"'"

        #INSERT INTO song (name, author, lenght) VALUES ('Gambler','HalaCG','00:04:15');
        valnames=guihelper.getColumnNames()
        for item in valnames:
            if "id" in item:
                valnames.remove(item)

        cur.execute("INSERT INTO "+table+" ("+ ",".join(valnames) +") VALUES ("+",".join(values)+");")
        conn.commit()
        guihelper.addToQueryHistory("INSERT INTO "+table+" ("+ ",".join(valnames) +") VALUES ("+",".join(values)+");")
        output = "Success.  Inserted items: (" + ",".join(values)+")"
        return output

    except psycopg2.Error as e:
        err = 'Error inserting item.'
        print(e)
        return [err,e]

def dropUser(user):#NOT IN USE RIGHT NOW
    try:
        # VIEW A TABLE
        params = guihelper.getConfig()
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (params[0], params[1], params[2], params[3]))
        cur = conn.cursor()
        cur.execute("REVOKE ALL ON ALL TABLES IN SCHEMA public FROM "+user+";")
        cur.execute("DROP USER "+user+";")
        guihelper.addToQueryHistory("REVOKE ALL ON ALL TABLES IN SCHEMA public FROM "+user+";")
        guihelper.addToQueryHistory("DROP USER "+user+";")
        conn.commit()

    except psycopg2.Error as e:
        err = 'Error dropping user.'
        print(e)
        return err

def getUsers():
    try:
        # VIEW A TABLE
        params = guihelper.getConfig()
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (params[0], params[1], params[2], params[3]))
        cur = conn.cursor()
        cur.execute("SELECT usename FROM pg_catalog.pg_user;")
        all = cur.fetchall()
        return all

    except psycopg2.Error as e:
        err = 'Error getting users.'
        print(e)
        return err

def getDataType(table):
    try:
        params = guihelper.getConfig()
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (params[0], params[1], params[2], params[3]))
        cur = conn.cursor()
        cur.execute("select column_name, data_type from information_schema.columns where table_schema NOT IN ('information_schema', 'pg_catalog') and table_name = '"+table+"' order by table_schema, table_name;")
        all = cur.fetchall()
        print(all)
        return all
        #guihelper.setData(all)
    except psycopg2.Error as e:
        print(e)
        err = 'Error fetching query.'
        return err

def deleteItems():
    try:
        # VIEW A TABLE
        params = guihelper.getConfig()
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (params[0], params[1], params[2], params[3]))
        cur = conn.cursor()
        table = guihelper.getName()
        values = guihelper.getSelection()
        columns = guihelper.getColumnNames()
        temp_flag = False
        for item in columns:
            if "id" in item:
                temp_flag = True
                id_ = columns.index(item)
        if temp_flag:
            for item in values:
                cur.execute("DELETE FROM "+table+" WHERE "+ str(columns[id_]) +"="+str(item[id_])+";")
                guihelper.addToQueryHistory("DELETE FROM "+table+" WHERE "+ str(columns[id_]) +"="+str(item[id_])+";")
        else:
            for item in values:
                where_text = []
                for i in range(len(columns)):
                    where_text.append(str(columns[i])+"="+str(item[i]))
                cur.execute("DELETE FROM "+table+" WHERE "+ " AND ".join(where_text) +";")
                guihelper.addToQueryHistory("DELETE FROM "+table+" WHERE "+ " AND ".join(where_text) +";")
        conn.commit()
        return 'Success.'

    except psycopg2.Error as e:
        err = 'Error deleting item.'
        print(e)
        return [err,e]

def updateData(table, tselection, values):
    try:
        params = guihelper.getConfig()
        conn = psycopg2.connect("host=%s dbname=%s user=%s password=%s" % (params[0], params[1], params[2], params[3]))
        cur = conn.cursor()
        #UPDATE table_name SET column1 = value1, column2 = value2, ... WHERE condition;
        for index in range(len(values)):
            values[index] = "'"+values[index]+"'"
        valnames=guihelper.getColumnNames().copy()
        for item in valnames:
            if "id" in item:
                valnames.remove(item)
        inside = []
        for index in range(len(values)):
            inside.append(valnames[index] + " = " + values[index])

        full_row = tselection
        full_columns = guihelper.getColumnNames()
        f = False
        for item in full_columns:
            if "id" in item:
                id_ = full_columns.index(item)
                f=True
        if f:
            for item in full_row:
                condition =  str(full_columns[id_]) +"="+str(item[id_])
        else:
            for item in full_row:
                where_text = []
                for i in range(len(full_columns)):
                    where_text.append(str(full_columns[i])+"="+str(item[i]))
                condition = " AND ".join(where_text)
        
        cur.execute("UPDATE "+table+" SET "+ ", ".join(inside) +" WHERE "+condition+";")
        conn.commit()
        guihelper.addToQueryHistory("UPDATE "+table+" SET "+ ", ".join(inside) +" WHERE "+condition+";")
        output = "Success. Updated items: (" + ",".join(values)+")"
        return output

    except psycopg2.Error as e:
        err = 'Error updating item.'
        print(e)
        return [err,e]