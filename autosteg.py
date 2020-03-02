from stegano import lsb, tools
from shutil import copyfile
import os
import argparse

def get_args():
    #creating an argument parser to retrieve the UserID from CLI
    parser = argparse.ArgumentParser()
    #defining "-u" to be a valid argument
    parser.add_argument("-u")
    parser.add_argument("-d")
    args = parser.parse_args()
    #setting UID to the value from -u argument
    return args.u, args.d

def convert_image(file):
    file = (tools.open_image(file)).convert("RGBA")
    print("converted file", file)
    return file

def hide_data(UID, files, modelDirectory, newDirectory):
    i=0
    for i in range(0,len(files)):
        file=modelDirectory + "/" + files[i]
        newfile = (newDirectory + "/" + files[i])
        print("File name: ", file)
        if file.lower().endswith(('.png', '.jpg', '.jpeg')):
            print("image mode: ",(tools.open_image(file)).mode)
            if ((tools.open_image(file)).mode not in ["RGB", "RGBA"]):
                file = convert_image(file)
            fileObject = lsb.hide(file, UID)
            fileObject.save(newfile)
        else:
            copyfile(file,newfile)

def create_notice():    
    notice = "This model was distributed to user:\n" + UID + "\nUnder the pretence that it is not to be distributed in any form. Failiure to do so will result in action taken againt the user."
    with open((newDirectory + "/notice.txt"), "w") as noticefile:
        noticefile.write(notice)
        


UID, modelDirectory =get_args()

#creating a directory in the previous folder, parent directory to be changed
#in deployment
newDirectory = "../temp/" + UID
modelDirectory = "../" + modelDirectory

#checking to make sure directory doesnt already exist
if os.path.isdir(newDirectory):
    print("directory exists already. Exiting")
    quit()
    
#creating directory
os.mkdir(newDirectory)

#making sure the new path was created
if not (os.path.exists(newDirectory) and os.path.exists(modelDirectory)):
    quit()

#creating a list of files in model directory
files=[f for f in os.listdir(modelDirectory) if os.path.isfile(os.path.join(modelDirectory, f))]


hide_data(UID, files, modelDirectory, newDirectory)
create_notice()

    





