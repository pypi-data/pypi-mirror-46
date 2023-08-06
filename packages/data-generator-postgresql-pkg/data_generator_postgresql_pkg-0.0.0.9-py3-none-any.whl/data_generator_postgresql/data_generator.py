import psycopg2
from datetime import datetime
import string
import random
import os
import time


#read conf file
def read_conf():
    with open("conf.cnf") as f:
        config = f.readlines()
    config = [x.strip() for x in config]
    f.close()
    return config


def read_conf_file_line(line_number):
    return config[line_number]


#config file in list row by row
config = read_conf()

#define connection here
database_name = read_conf_file_line(7)
username = read_conf_file_line(8)
password = read_conf_file_line(9)
hostname= read_conf_file_line(10)

#define tables here
#tables = ['test','users','nana'] #11
tables = (read_conf_file_line(11)).strip().split(' ') #11

landing_zone=read_conf_file_line(2) 
log_file_path=read_conf_file_line(5)

#rows count in file
write_count = int(read_conf_file_line(1))

#adds datatypes synonims in list 
#(if we got `varchar` in confg file -> add `str` to this list)
#(also if we got `text` in confg file -> add `str` to this list)
t_cfg = []

#total files size
total_files_num = int(read_conf_file_line(6))

files_num = 0


#get the schema for each table, to understand what datatype each column got
def execute_query(table_name,cursor):
    cursor.execute("""SELECT column_name,data_type FROM information_schema.columns WHERE table_name = '{}';""".format(table_name))
    records = list(cursor.fetchall())
    return records

#a function what adds values to t_cfg
def temp_cnf(first_line_of_cnfg_file):
    f=first_line_of_cnfg_file
    if ('integer' in f) or ('bigint' in f) or ('smallint' in f) or ('int' in f):
        t_cfg.append('int')
    if ('character' in f) or ('text' in f) or ('varchar' in f):
        t_cfg.append('str')
    if ('timestamp' in f) or ('date' in f):
        t_cfg.append('date')

#get random values for particular data type
def get_random(unit):
    if (unit[2] == 'int' and 'int' in t_cfg):
        return random.randint(1,9)
    if (unit[2] == 'str' and 'str' in t_cfg):
        return random.choice(string.ascii_letters)
    if (unit[2] == 'date' and 'date' in t_cfg):
        return datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    return "NULL"

#check synonims
def get_synonim_datatype(unit):
    if 'integer' in unit or 'bigint' in unit or 'smallint' in unit or 'int' in unit:
        return 'int'
    if 'character' in unit or 'text' in unit:
        return 'str'
    if 'timestamp' in unit or 'date' in unit:
        return 'date'


#convert list to string with `|` delimiter
def list_to_String(s): 
    myString = '|'.join(str(x) for x in s)
    return myString

#adds a colomn to schema, with datatypes synonims, looks like temp_cnf function
#if we got `text` or `varchar` at schema datatype, adds a datatype synonim
def append_types_to_schema(rec):
    types = []
    for row in rec:
        a = list(row)
        a.append(get_synonim_datatype(row[1]))
        types.append(a)
    return types

#writes line to file
def write_to_file(num,file,types):
    #add_log('Writing file    \t'+os.path.basename(file.name)+ '\t file in WRITING path ')
    global files_num
    files_num+=1
    line=[]
    for i in range(num):
        for row in types:
            line.append(get_random(row))
        file.write("\""+list_to_String(line)+"\""+"\n")
        line = []

def close_all_open_sources():
    cursor.close()
    conn.close()

def open_connection_to_db(db_name,user_name,host_name,passwd):
    conn = psycopg2.connect(dbname=db_name, 
                        user=user_name, 
                        password=passwd, 
                        host=host_name)
    return conn.cursor()

def create_paths():
    if not os.path.exists(landing_zone):
        os.makedirs(landing_zone)

def add_log(message):
    f = open(log_file_path, 'a+')
    f.write(datetime.today().strftime("%Y-%m-%d %H:%M:%S")+'\t'+message+'\n')
    f.close()

def main_func():
    cursor = open_connection_to_db(database_name,username,hostname,password)
    records = []
    types = []
    temp_cnf(read_conf_file_line(0))
    create_paths()
    global files_num
    while(files_num<total_files_num):
        for table in tables:
            file = open(landing_zone+table+"_"+datetime.today().strftime("%Y-%m-%d_%H:%M:%S")+".writing","a")
            records = execute_query(table,cursor)
            types = append_types_to_schema(records)
            write_to_file(write_count,file,types)
            os.rename(file.name,landing_zone+os.path.splitext(os.path.basename(file.name))[0] + ".ready")
            #add_log('Ready\t\t\t'+os.path.basename(file.name)+ '\t moved to READY folder')
            if files_num==total_files_num:
                break
    cursor.close()


while(True):
    start_time = datetime.now()
    main_func()
    spent_time = (datetime.now()-start_time).total_seconds()
    files_num=0
    t_cfg=[]
    time.sleep(15-spent_time)