from pathlib import Path
import csv
class CSVHandling() :
    FileDiscriptor = 0
    writer = 0
    def __init__(self,filePath,header):
        config = Path(filePath)
        if(config.is_file == False):
            self.FileDiscriptor = open(filePath, 'w',newline='')
            self.writer = csv.writer(self.FileDiscriptor , delimiter=',')
            self.writer.writerow(header)
            self.FileDiscriptor.flush()
            
        else:
            self.FileDiscriptor = open(filePath,'a',newline='')
            self.writer = csv.writer(self.FileDiscriptor , delimiter=',')
    def write_data(self,data):
        self.writer.writerow(data)
        self.FileDiscriptor.flush()

            
            