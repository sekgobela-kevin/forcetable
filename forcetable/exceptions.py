

class FieldError(Exception):
    '''Errors relating to fields'''

class FieldNotFound(FieldError):
    '''Failed to find field or is missing'''
    pass

class PrimaryFieldError(FieldError):
    '''Erros relating to primary field'''

class PrimaryFieldNotFound(FieldNotFound, PrimaryFieldError):
    '''Failed to find primary field or is missing'''
    pass

