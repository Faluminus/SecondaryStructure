import os
import logging
import subprocess



#PATHS
inputFileWIN = 'data/raw/mmCIF'
outputFileWIN = 'data/raw/AMINtoSEC.csv'
log_dir = 'scripts/logs/'






#COMMANDS
def CommandDSSP(inputFile):
    commandDSSP = f'dssp {inputFile} --output-format dssp'
    return commandDSSP






#LOGGING

# Logger setup
log_file = os.path.join(log_dir, "app.log")
logging.basicConfig(filename=log_file,
                    format='%(asctime)s %(message)s',
                    filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.INFO)





#FUNCTIONS

def CheckForDownloaded():
    with open(os.path.join(log_dir, "app.log"),'r') as logs:
        lineNum = len(logs.readlines())
        return lineNum
        

def ProteinPaths(divided_path):
    protein_paths = os.listdir(divided_path)
    return protein_paths

def ProcessDSSP(dsspData):
    allData = ["",""]
    lines = dsspData.splitlines()
    i = False
    for line in lines:

        if i:
            structure = line[16]
            aminoacid = line[13]
            allData[0] += aminoacid
            allData[1] += structure

        if line.startswith('  #'):
            i = True
        
    
    return allData





#MAIN
divided_names = os.listdir(inputFileWIN)

finalDataset = open(outputFileWIN,'a',newline="")
finalDataset.write("AminoAcidSeq,SecondaryStructureSeq")
finalDataset.close()

num_of_already_downloaded = CheckForDownloaded()
currently_downloading = 0


for divided in divided_names:
    proteins = ProteinPaths(inputFileWIN + divided)
    for protein in proteins:
        if 23471 < currently_downloading:
            print(protein + ':doing_DSSP')
            args = subprocess.run(CommandDSSP(inputFileWIN + '/' + divided + '/' + protein),capture_output=True, text=True, shell=True).stdout
            print(protein + ':done_DSSP')
            print(protein + ':procesing_DSSP')
            processed_dssp = ProcessDSSP(args)
            print(protein + ':procesing_done_DSSP')
            if processed_dssp != ['','']:
                finalDataset = open(outputFileWIN,'a',newline="")
                finalDataset.write('\n'+processed_dssp[0]+','+processed_dssp[1])
                finalDataset.close()
                logger.info(protein + ':was_processed')
                print(protein + ':was_processed')
            else:
                logger.info(protein + ':wasnt_processed')
                print(protein + ':wasnt_processed')
        currently_downloading+=1
