import csv
import os
import pandas as pd
import matplotlib.pyplot as plt
import fileinput
columns=[];rows=[];aoa = []
config="0012v2.cfg"
resultsall="all_results"
resultscl="results_clalpha.txt"
resultscd="results_cdalpha.txt"
file_flow="flow.vtu"
file_surfaceflow="surface_flow.vtu"
file_history="history.csv"
minaoa=0;maxaoa=15;stepsize=1
command_run1="cmd /c mpiexec -n "
command_run2=" SU2_CFD.exe 0012v2.cfg"
command_mkdir="mkdir ";command_move="move "
command_checkprocess='tasklist | find /i "SU2">>checkprocess.txt'
command_numberofcores="WMIC CPU Get NumberofCores"
os.system(command_numberofcores)
numberofcores=str(input("How many core would you like to use for analysis?"))
open(resultscl, 'w').close()   #Clears the Cl results from previous runnings.
open(resultscd, 'w').close()   #Clears the CD results from previous runnings.
os.system(command_mkdir+resultsall)
for angle in range(minaoa, maxaoa + 1, stepsize):
    aoa.append(angle)
    os.system(command_run1+numberofcores+command_run2)
    os.system(command_checkprocess)
    if os.path.getsize("checkprocess.txt")==0:   #Checks whether another SU2_CFD process is also running
        filename = file_history
        with open(filename, "r") as csvfile:
            csvreader = csv.reader(csvfile)
            columns = next(csvreader)
            for row in csvreader:
                rows.append(row)
        wherecl=columns.index('       "CL"       ')
        wherecd=columns.index('       "CD"       ')
        iterationval=len(rows)
        row1=rows[iterationval-1]
        convergedcl=row1[wherecl]
        convergedcd=row1[wherecd]
        with open(resultscl, 'a') as f0:
            f0.write(str(angle)+","+convergedcl+"\n")
        with open(resultscd, 'a') as f3:
            f3.write(str(angle)+","+convergedcd+"\n")
    else:
        print("There is another running SU2_CFD.exe process on your computer, please terminate the other processes.")
    os.system("del checkprocess.txt")
    os.system(command_mkdir+resultsall+"\\"+str(angle))
    os.system(command_move+file_flow+" "+os.getcwd()+"\\"+resultsall+"\\"+str(angle))
    os.system(command_move + file_surfaceflow + " " + os.getcwd() + "\\" + resultsall + "\\" + str(angle))
    os.system(command_move + file_history + " " + os.getcwd() + "\\" + resultsall + "\\" + str(angle))
    for line in fileinput.input(config, inplace=True):
            if line.startswith('AOA='):
                print("AOA="+str(angle))
            else:
                print(line.strip())
datacd=pd.read_csv(resultscd, sep=',\s+',header=None,engine="python")
datacd= pd.DataFrame(datacd)
x = datacd[0]
y = datacd[1]
plt.xlabel("Angle of Attack")
plt.ylabel("Cd")
plt.xlim(minaoa,maxaoa)
plt.ylim(min(y),max(y))
plt.plot(x, y,'r')
plt.legend(["Cd vs. Alpha Graph"],bbox_to_anchor=(1.01, 1.1),fontsize=10)
plt.savefig(resultscd+".png",dpi=100)
datacl=pd.read_csv(resultscd, sep=',\s+',header=None,engine="python")
datacl= pd.DataFrame(datacl)
x = datacl[0]
y = datacl[1]
plt.xlabel("Angle of Attack")
plt.ylabel("Cl")
plt.xlim(minaoa,maxaoa)
plt.ylim(min(y),max(y))
plt.plot(x, y,'r')
plt.legend(["Cl vs. Alpha Graph"],bbox_to_anchor=(1.01, 1.1),fontsize=10)
plt.savefig(resultscl+".png",dpi=100)