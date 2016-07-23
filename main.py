from app import evolve

def main():
    words = ['eff', 'reff', 'ppopadom']
    rules, words = evolve.evolve(words, 5)

    print(rules)
    print(words)

if __name__=='__main__':
    main()
