import random
import os
from datetime import datetime
import string

#read conf file
def read_conf():
    with open("conf.cnf") as f:
        config = f.readlines()
    config = [x.strip() for x in config]
    f.close()
    return config


def read_conf_file_line(line_number):
    return config[line_number]


def gb_to_bytes(number):
    return number*1073741824


#config file in list row by row
config = read_conf()

landing_zone=read_conf_file_line(2) 
done_path = read_conf_file_line(3) 
error_path = read_conf_file_line(4)
log_file_path= read_conf_file_line(5)

total_files_size = gb_to_bytes(float(read_conf_file_line(12)))

def add_to_postgrase_dummy_function(file):
    a = random.randint(-100,100)
    if a<=0:
        return 1/0
    if a>0:
        return 1

def create_paths():
    if not os.path.exists(done_path):
        os.makedirs(done_path)
    if not os.path.exists(error_path):
        os.makedirs(error_path)

def list_in_ready_path(directory, extension):
    return (f for f in os.listdir(directory) if f.endswith('.' + extension))

def add_log(message):
    f = open(log_file_path, 'a+')
    f.write(datetime.today().strftime("%Y-%m-%d %H:%M:%S")+'\t'+message+'\n')
    f.close()


def main():
    create_paths()
    ready_list = list_in_ready_path(landing_zone,'ready')
    actual_size = 0
    for f in ready_list:
        try:
            file = open(landing_zone+f,)
            actual_size += os.path.getsize(landing_zone+f)

            add_to_postgrase_dummy_function(file)
            os.rename(file.name,done_path+os.path.splitext(os.path.basename(file.name))[0] + ".done")
            file.close()
            #add_log('added to database\t'+os.path.basename(file.name)+ '   \t moved to DONE folder')
            if actual_size>total_files_size:
                break
                
        except ZeroDivisionError:
            os.rename(file.name,error_path+os.path.splitext(os.path.basename(file.name))[0] + ".err")
            add_log('error occured    \t'+os.path.basename(file.name) +'   \t moved to ERROR folder')
            pass

def execute_insertion():
    main()