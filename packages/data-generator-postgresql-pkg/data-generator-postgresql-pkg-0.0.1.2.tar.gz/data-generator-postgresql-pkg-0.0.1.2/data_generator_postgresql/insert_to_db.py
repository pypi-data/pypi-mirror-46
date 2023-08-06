import random
import os
from datetime import datetime
import string
import psycopg2
import fcntl


#read conf file
def read_conf(conf_path):
    with open(conf_path) as f:
        config = f.readlines()
    config = [x.strip() for x in config]
    f.close()
    return config


def read_conf_file_line(line_number):
    return config[line_number]


def gb_to_bytes(number):
    return number*1073741824
		
def add_to_postgrase_dummy_function(file,db_name,user_name,passwd,hostname):
    conn = None
    conn = psycopg2.connect(dbname=db_name,user=user_name,password=passwd,host=hostname)
    cur = conn.cursor()
    cur.callproc('insert_dummy_function', (file,))
    if conn is not None:
        conn.close()
			
def create_paths(done_path,error_path):
    if not os.path.exists(done_path):
        os.makedirs(done_path)
    if not os.path.exists(error_path):
        os.makedirs(error_path)

#
def list_in_ready_path(directory,extension):
    return (f for f in os.listdir(directory) if f.endswith('.' + extension))
    


def add_log(message,log_file_path):
    f = open(log_file_path, 'a+')
    f.write(datetime.today().strftime("%Y-%m-%d %H:%M:%S")+'\t'+message+'\n')
    f.close()

def create_log_table(conn):
    cur = conn.cursor()
    cur.execute("""Create table if not exists log_files(file_name varchar);""")
    conn.commit()

def main(config):
    create_paths(config[3],config[4])
    ready_list = list_in_ready_path(config[2],'ready')
    conn = None
    conn = psycopg2.connect(dbname=config[7],user=config[8],password=config[9],host=config[10])
    cur = conn.cursor()
    create_log_table(conn)
    actual_size = 0
    for f in ready_list:
        file = open(config[2]+f,)
        try:
            cur.execute("""Select * from log_files where file_name='{}';""".format(f))
            records = list(cur.fetchall())
            print(records)

            if not records:
                add_to_postgrase_dummy_function('{'+f+'}',config[7],config[8],config[9],config[10])
                cur.execute("""INSERT INTO log_files(file_name) VALUES('{}');""".format(f))
                conn.commit()
                actual_size += os.path.getsize(config[2]+f)

                os.rename(file.name,config[3]+os.path.splitext(os.path.basename(file.name))[0] + ".done")
                file.close()
                #add_log('added to database\t'+os.path.basename(file.name)+ '   \t moved to DONE folder')
                if actual_size > gb_to_bytes(float(config[12])):
                    break
            else:
                add_log('\t'+os.path.basename(file.name) +'   \t\t DUPLICATION',config[5])
        except(Exception, psycopg2.DatabaseError) as error:
            os.rename(file.name,config[4]+os.path.splitext(os.path.basename(file.name))[0] + ".err")
            add_log('\t'+os.path.basename(file.name) +'   \t moved to ERROR folder',config[5])
            pass


def execute_insertion(conf_path):
    fh=open('insert_to_db.temp','a')
    try:
        fcntl.flock(fh,fcntl.LOCK_EX|fcntl.LOCK_NB)
        config = read_conf(conf_path)
        main(config)
    except:
        os._exit(0)
