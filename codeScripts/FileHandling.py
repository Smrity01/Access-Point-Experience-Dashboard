from pathlib import Path
import csv

class CSVHandling :
    FileDiscriptor = 0
    writer = 0
    def __init__(self,filePath,header):
        '''
        Input Parameter:-
                    filePath: Path of csv file user wants to open
                    header: Header of file that is required to wrtie to file if file open in write mode
        Objective:
                    To open file
        '''
        config = Path(filePath)
        try:
            if config.is_file==False:
                self.FileDiscriptor = open(filePath, 'w',newline='')
                self.writer = csv.writer(self.FileDiscriptor , delimiter=',')
                self.writer.writerow(header)
                self.FileDiscriptor.flush()
            else:
                self.FileDiscriptor = open(filePath,'a',newline='')
                self.writer = csv.writer(self.FileDiscriptor , delimiter=',')
                self.FileDiscriptor.flush()
        except IOError as error :
            print("Error : " + str(error))
    
    def write_row(self,data):
        '''
            Input Parameter : data - a row which is to be write on the file
            Objective : To write data to file
            Output Parameter: -
        '''
        try:
            self.writer.writerow(data)
            self.FileDiscriptor.flush()
        except IOError as error :
            print("Error : " + str(error))
        
    def write_rows(self,data):
        '''
        Input Parameter : data - rows which is to be written on the file
        Objective : To write data to file
        Output Parameter: -
        '''
        try:
            self.writer.writerows(data)
            self.FileDiscriptor.flush()
        except IOError as error :
            print("Error : " + str(error))
            

class TextHandling :
    filename = 0
    def __init__(self,file) :
        '''
            Input Parameter:-
                        filePath: Path of text file user wants to open.
            Objective:
                        To open file
        '''
        self.filename = file
    
    def write(self,data) :
        '''
            Input Parameter : data - a row which is to be write on the file
            Objective : To write data to file
            Output Parameter: -
         '''
        try:
            file = open(self.filename,"w")
            file.write(data)
            file.close()
        except IOError as error :
            print("Error : " + str(error))  
    
    def read(self) :
        '''
            Input Parameter : -
            Objective : To read content of file
            Output Parameter: return content of file
         '''
        try :
            file = open(self.filename,"r")
            data = file.read()
            file.close()
            return data
        except IOError as error :
            print("Error : " + str(error))
     

            