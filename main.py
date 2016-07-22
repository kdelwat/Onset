import evolve

from table import Table

def main():
    inventory = (Table('pulmonicinventory.csv'), None, None)
    words = ['ppotato', 'paraddʰise']
    evolve.evolve(inventory, words, 5)

if __name__=='__main__':
    main()
