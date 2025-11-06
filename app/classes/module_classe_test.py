class dataOK :
    """ classe pour définir les caractéristiques d'un Amphi"""
    
    def __init__(self ,ok ) :
        self.ok = ok
        
    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__})"
    