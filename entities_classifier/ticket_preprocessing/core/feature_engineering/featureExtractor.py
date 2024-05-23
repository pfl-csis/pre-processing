import logging
from abc import ABCMeta


class FeatureExtractor(metaclass=ABCMeta):
    """
    Class for reading Markdown tickets and converting them into a dictionary.
    This class allows tickets in Markdown format of undefined length or section count.
    Attributes:
        `file_path` (str): The path to the Markdown ticket file.\n
        `verbose` (bool): Flag to determine whether to log messages for debugging purposes. \n
        `data` (dict): Dictionary containing the markdown ticket data.\n
    Methods:
        `log(msg)`: Logs messages if the `verbose` flag is set to True.\n
        `read_md_template()`: Reads the Markdown ticket file and returns its contents.\n
        `md_to_dict()`: Converts the Markdown ticket into a dictionary.\n
        `run()` : Executes the full conversion flow and returns the data dictionary
    """
  
    def __init__(self, file_path="./", verbose=True):
        """
        Initializes a FeatureExtractor instance.

        Args:
            `file_path` (str): The path to the Markdown ticket file. Defaults to "./".
            `verbose` (bool): Flag to determine whether to log messages for debugging purposes. Defaults to True.
        """
        self.file = file_path
        self.verbose = verbose
        logging.basicConfig(filename="./logs/ticketReader.log", encoding="utf-8", level=logging.DEBUG)
        

    def log(self, msg):
        """
        Logs messages if the `verbose` flag is set to True.

        Args:
            `msg` (str): The message to log.
        """
        if self.verbose:
            logging.debug(msg)


    def read_md_template(self):
        """
        Reads the Markdown ticket file and returns its contents.

        Returns:
            `str`: The contents of the Markdown ticket file.
        
        Raises:
            `IOError`: If the Markdown ticket file cannot be found.
        """
        try:
            self.log("Opening file at path: %s" % self.file)
            with open(self.file, 'r') as file:
                return file.read()
        except:
            raise IOError("Can't find Markdown ticket")


    
    def repeatedSectionHandler(self, line):
        """
        This function handles repeated sections
        """
        section_name = line[3:]
        
        section_nr = 1
        while section_name in self.data:
            new_name = section_name + str(section_nr)
            if new_name in self.data:
                section_nr += 1
                continue
            self.data[new_name] = {}
            self.section_name = new_name
            self.field_name = ""
            break
        
        if section_name not in self.data:
            self.section_name = section_name
            self.field_name = ""
            self.data[section_name] = {}    


    def entitiesHandler(self, line):
        split_line =  line.split(": ",1)
        print("FIELD1 %s" % self.field_name)
        if len(split_line) == 1:
            print("FIELD2 %s" % self.field_name)
            self.data[self.section_name][self.field_name] += "".join(split_line) + "\n"
            return
        
        if split_line[1] == "" and self.field_name == "":
            self.field_name = split_line[0]
            self.data[self.section_name][self.field_name] = ""
        

        else:
            self.field_name = split_line[0]
            field_val = split_line[1]
            self.data[self.section_name][self.field_name] = field_val
            self.field_name = ""
            
    def multilineHandler(self, line):
        if self.data[self.section_name] == {}:
            self.data[self.section_name] = "" 
        if "Entities" in self.section_name:   
            self.data[self.section_name][self.field_name] += "\n" + line.strip().strip()
        else:
            self.data[self.section_name] += "\n" + line.strip().strip()
                

    def run(self):
        """
        Converts the Markdown ticket into a dictionary.
        Runs the data reader and returns the data dictionary constructed from the investigation ticket.
        """
        text = self.read_md_template()
        self.data = {}
        self.section_name = ""
        self.field_name = None
        line_counter = 0
        for line in text.split("\n"):
            if line == "":# and self.section_name != "":
                print("Section name: %r" % bool(self.section_name))
                print("Section name: %s\n\n" % (self.section_name))
                if not self.section_name:
                                       continue
                elif not self.field_name and "Entities" not in self.section_name :
                    self.data[self.section_name] += "\n"
                    continue
                elif bool(self.field_name):
                    self.data[self.section_name][self.field_name] += "\n"
                    continue
                else:
                    continue
                
            self.log("Current line:\n> %s" % line)
            self.log("Current Section: %s\tfield_name: %s\field: %s\n" 
                        % (self.section_name, self.field_name, self.field_name))
            
            # Handling the static first two lines  
            if line_counter == 0:
                split_line = line.split(" ",2)
                self.data["Alert Name"]=split_line[2]
                self.data["Alert ID"]= split_line[1][0:-1] #removing ":"
            
            if line_counter == 1:
                split_line = line.split(": ",1)
                self.data["Incident ID"]=split_line[1]
            
            ## Handling sections
            if line.startswith("## "):
                self.repeatedSectionHandler(line)
                        
            
            
            elif "Entities" in self.section_name:
                
                self.entitiesHandler(line)
                         
            elif self.section_name != "":
                self.multilineHandler(line)
                
                
                        
            line_counter+=1    

        return 0


   
 


