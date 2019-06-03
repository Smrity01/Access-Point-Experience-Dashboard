from pathlib import Path
import csv
class CSVHandling() :
    FileDiscriptor = 0
    writer = 0
    def __init__(self,filePath,header):
        config = Path(filePath)
        try:
            if(config.is_file == False):
                self.FileDiscriptor = open(filePath, 'w',newline='')
                self.writer = csv.writer(self.FileDiscriptor , delimiter=',')
                self.writer.writerow(header)
                self.FileDiscriptor.flush()

            else:
                self.FileDiscriptor = open(filePath,'a',newline='')
                self.writer = csv.writer(self.FileDiscriptor , delimiter=',')
        except IOError as error :
            print("Error : " + str(error))
    
    def write_row(self,data):
        try:
            self.writer.writerow(data)
            self.FileDiscriptor.flush()
        except IOError as error :
            print("Error : " + str(error))
        
    def write_rows(self,data):
        try:
            self.writer.writerows(data)
            self.FileDiscriptor.flush()
        except IOError as error :
            print("Error : " + str(error))
            
            