from app import evolve


def main():
    words = ['something']
    rewrite = [('o', 'ə'), ('me', 'm'), ('th', 'θ'), ('ing', 'ɪŋ')]

    rules, words = evolve.evolve(words, 5, rewrite)

    print(rules)
    print(words)

if __name__=='__main__':
    main()
