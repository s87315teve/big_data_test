try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET
import os
import sys, codecs
import shutil
import time
#掃描檔案
def scan_files(directory,prefix=None,postfix=None):
    files_list=[]
    for root, sub_dirs, files in os.walk(directory):
        for special_file in files:
            if postfix:
                if special_file.endswith(postfix):
                    files_list.append(os.path.join(root,special_file))
            elif prefix:
                if special_file.startswith(prefix):
                        files_list.append(os.path.join(root,special_file))
            else:
                files_list.append(os.path.join(root,special_file))
    return files_list






def read_xml(file):
    tree = ET.parse(file)    
    return tree



def iter_xml(root,name):
    c=0
    for node in root.iter(name):
        #print(node)
        c+=1
    print (c)

'''
ic=0
bc=0
for image in root.iter('Image'):
    ic+=1
    #print (image.attrib['PicPath'])
print(ic)

for com in root.iter('Component'):
    bc+=1
    #print (com.attrib['MachineDefect'])

print(bc)

'''

def checkPath(path):
    isExists=os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print("make file: "+path)



#----------main function----------

file=open('errorMsg.txt','w')

print('running...')

path = os.path.abspath('.')
path=path.replace('XML\\20190106\\AOI_2\\4711-014339-02','')
print(path)
#create path of image file
#create new path
tStart = time.time()
xmlList=scan_files(path,prefix=None,postfix='.xml')

tScan = time.time()

print('scanning took '+str(tScan-tStart)+' seconds.')

wtf_c=0
for xmlFile in xmlList:
    tree = read_xml(xmlFile)
    root=tree.getroot()
    #print(xmlFile)
    
    for i in root:
        for component in i.findall('Component'):
            #print(component.attrib['MachineDefect'])
            #print(component)
            #print(component.attrib['MachineDefect'])
            fileName=component.attrib['MachineDefect']
            #if len(fileName)<2:
                #fileName="WTF"
            for j in component.iter('Image'):
                try:
                    oldPath=j.attrib['PicPath']
                    oldPath=path+oldPath.replace('Z:\\','')
                    #oldPath=oldPath.replace('\\','/')
                    newPath=path+fileName+'\\'+oldPath.split('\\')[-1]
                    forCheckPath=path+fileName
                    checkPath(forCheckPath)
                    shutil.copy2(oldPath,newPath)
                except:
                    wtf_c+=1
                    '''
                    fileName="WTF"
                    wtf_c+=1
                    newPath=newPath+fileName+"\\"+"WTF"+str(wtf_c)
                    '''
                    file.write(str(wtf_c)+'. error file : '+xmlFile+'\nMachineDefect : '+fileName+', '+'PicPath : '+oldPath.split('\\')[-1]+'\n')
                    print(str(wtf_c)+'. error file : '+xmlFile+'\nMachineDefect : '+fileName+', '+'PicPath : '+oldPath.split('\\')[-1]+'\n')
                
                #print(j.attrib['PicPath'])
    #open xmlFile
    #find property
    #move image file
    #close xmlFile

file.close()

print('finished')
tEnd = time.time()
print ('moving files took '+str(tEnd-tScan)+' seconds.')    

print ('it took '+str(tEnd-tStart)+' seconds.')  
