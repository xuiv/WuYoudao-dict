# global functions
   
def is_alphabet(uchar):
    if (u'\u0041' <= uchar <= u'\u005a') or \
            (u'\u0061' <= uchar <= u'\u007a') or uchar == '\'':
        return True
    else:
        return False
        
        
