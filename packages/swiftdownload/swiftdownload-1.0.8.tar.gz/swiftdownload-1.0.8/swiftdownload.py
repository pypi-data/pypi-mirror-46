import logging
import datetime
import time
import os
import uuid
import shutil
import click
import subprocess
from swiftclient.service import SwiftService, SwiftError
from sys import argv
logging.basicConfig(level=logging.ERROR)
logging.getLogger("requests").setLevel(logging.CRITICAL)
logging.getLogger("swiftclient").setLevel(logging.CRITICAL)
logger = logging.getLogger(__name__)


now = datetime.datetime.now()


def move_files(dest_folder, file_path, mdomid,file_name):
    #print dest_folder
    #print file_path
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    dest_folder = dest_folder +'/'+str(uuid.uuid4())
    if file_path.find(mdomid) != -1:
        #Move to desination folder with name
        shutil.move(file_path, dest_folder+file_name)
        return dest_folder+file_name

def combine_file(file_path, file_name, del_tmp_file):
    if os.path.isfile(file_path+"/"+file_name):
        os.remove(file_path+"/"+file_name)
        print("File deleted " + str(file_path+"/"+file_name))
    file_output = os.path.join(file_path,file_name)
    files = os.listdir(file_path)
    for file in files:
        os.path.join(file_path,file)
        f = open(os.path.join(file_path,file),'r') 
        fout = open(file_output,"a")
        for line in f:
           fout.write(line)
    os.remove(del_tmp_file)


def is_png(obj,mdom_name,pathToday):
    if (obj["name"].find(pathToday) != -1) and (obj["name"].find(mdom_name) != -1) and obj["name"].lower().endswith('.csv'):
       print(str(obj["name"].lower()))
       return True
    else:
       return False

@click.command()
@click.option('-m', '--mdom_name', multiple=False)
@click.option('-c', '--container', multiple=False)
@click.option('-df', '--destination_folder', multiple=False)
@click.option('-fn', '--file_rename',multiple=False)
@click.option('-t', '--topic',multiple=False)
def download_script(mdom_name,container,destination_folder,file_rename,topic):
    with SwiftService() as swift:
        try:
            #subprocess.call("/u/myproject/s.sh",shell=True) 
            list_options = {"prefix": "path"}
            list_parts_gen = swift.list(container=container)
            for page in list_parts_gen:
                pathToday = 'report/'+topic+'/'+str(now.year)+'/'+str(now.month)+'/'+str(now.day)+'/'+container+'/'+mdom_name
                if page["success"]:
                    objects = [
                        obj["name"] for obj in page["listing"] if is_png(obj,mdom_name,pathToday)
                    ]
                    for down_res in swift.download(container=container,objects=objects):
                        if down_res['success']:
                            print("'%s' downloaded" % down_res['object'])
                        else:
                            print("'%s' download failed" % down_res['object'])
                    try:
                        os.system("rm -rf " + destination_folder + "*.csv") or os.system("rm -rf " + destination_folder + "*.json")
                    except Exception as e:
                        print("Directory doesn't exist" + str(destination_folder))
                    for obj in objects:
                        tmpfile =  move_files(destination_folder, obj,mdom_name,file_rename)
                    combine_file(destination_folder,file_rename, tmpfile)
		    click.echo('Download successful')
                else:
                    raise page["error"]
                    click.echo('Download failed')
        except SwiftError as e:
            logger.error(e.value)
if __name__=='__main__':
	download()
