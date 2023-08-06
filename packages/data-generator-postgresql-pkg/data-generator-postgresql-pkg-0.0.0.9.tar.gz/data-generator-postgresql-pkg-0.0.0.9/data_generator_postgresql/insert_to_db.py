import random
import os
from datetime import datetime
import string
import psycopg2

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


# def add_to_postgrase_dummy_function(file):
    # a = random.randint(-100,100)
    # if a<=0:
        # return 1/0
    # if a>0:
        # return 1
		
def add_to_postgrase_dummy_function(file,db_name,user_name,passwd,host_name):
    conn = None
    conn = psycopg2.connect(dbname=db_name,user=user_name,password=passwd,host=host_name)
    cur = conn.cursor()
    cur.callproc('insert_dummy_function', (file,))
    if conn is not None:
        conn.close()
			
def create_paths(done_path,error_path):
    if not os.path.exists(done_path):
        os.makedirs(done_path)
    if not os.path.exists(error_path):
        os.makedirs(error_path)

def list_in_ready_path(directory, extension):
    return (f for f in os.listdir(directory) if f.endswith('.' + extension))

def add_log(message,log_file_path):
    f = open(log_file_path, 'a+')
    f.write(datetime.today().strftime("%Y-%m-%d %H:%M:%S")+'\t'+message+'\n')
    f.close()


def main(config):
    create_paths(config[3],config[4])
    ready_list = list_in_ready_path(config[2],'ready')
    actual_size = 0
    for f in ready_list:
        try:
            file = open(config[2]+f,)
            actual_size += os.path.getsize(config[2]+f)

            add_to_postgrase_dummy_function(file,config[7],config[8],config[9],config[10])
            os.rename(file.name,config[3]+os.path.splitext(os.path.basename(file.name))[0] + ".done")
            file.close()
            #add_log('added to database\t'+os.path.basename(file.name)+ '   \t moved to DONE folder')
            if actual_size>gb_to_bytes(float(config[12])):
                break
                
        except(Exception, psycopg2.DatabaseError) as error:
            os.rename(file.name,config[4]+os.path.splitext(os.path.basename(file.name))[0] + ".err")
            add_log('\t'+os.path.basename(file.name) +'   \t moved to ERROR folder',config[5])
            pass

def execute_insertion(conf_path):
    config = read_conf(conf_path)
    main(config)