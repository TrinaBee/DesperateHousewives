'''
Ich bin ein Nachfolger-Modul
'''

def nachfolger(x:int) -> int:
    '''
    Funktion für den Nachfolger
    :param x: einziger Parameter - INT
    :return: der Nachfolger vom Parameter
    '''
    return x+1

if __name__=='__main__':
    print('Projekt A:', nachfolger(8))