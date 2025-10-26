from dataclasses import  dataclass
from classes.c1_classe_chargementCsv import chargementCSV

@dataclass( init=False)  # parce qu'il y a un __init__
class champsApogee  :  
    codeApogee   : list[str]
    valeurApogee : list[str]  
       
    def __init__(self, dataBrutes :  chargementCSV  ):
        self.codeApogee    = dataBrutes.apogee.entete
        self.valeurApogee  = dataBrutes.apogee.data[0]
        print('1)',self.codeApogee)
        print('2)',self.valeurApogee)
        
    def valeurCode(self,codeApogeeVoulu):        
        for index, code in enumerate(self.codeApogee) :
            if codeApogeeVoulu==code :
                return self.valeurApogee[index]           
        return ""
            
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
