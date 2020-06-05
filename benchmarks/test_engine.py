import engine.engine as engine


def test_engine_fast(benchmark):
    words, rules = benchmark(
        engine.run_engine, ["aba", "bːɒtl", "b\u02D0ɒtl", "b\u02D0ɒbtdolie"]
    )

    assert words == ["ab͡βaː", "bːɒːdl", "bːɒːdl", "bːɒːbddoːliːe"]
    assert rules == [
        {
            "name": "Gemination",
            "description": "Plosives become lengthened between vowels.",
            "before": {"positive": ["syllabic"]},
            "after": {"positive": ["syllabic"]},
            "conditions": {
                "positive": ["consonantal"],
                "negative": ["continuant", "delayedrelease", "sonorant", "long"],
            },
            "applies": {"positive": ["long"]},
        },
        {
            "name": "Affrication",
            "description": "Plosives become affricates between vowels.",
            "before": {"positive": ["syllabic"]},
            "after": {"positive": ["syllabic"]},
            "conditions": {
                "positive": ["consonantal"],
                "negative": ["continuant", "delayedrelease", "sonorant"],
            },
            "applies": {"positive": ["delayedrelease"]},
        },
        {
            "name": "Degemination",
            "description": "Geminated consonants are shortened after vowels.",
            "before": {"positive": ["syllabic"]},
            "conditions": {"positive": ["long"]},
            "applies": {"negative": ["long"]},
        },
        {
            "name": "Lengthening",
            "description": "Vowels are lengthened after voiced consonants.",
            "conditions": {"positive": ["syllabic"], "negative": ["long"]},
            "before": {"positive": ["voice", "consonantal"]},
            "applies": {"positive": ["long"]},
        },
        {
            "name": "Voicing",
            "description": "Consonants become voiced after voiced segments.",
            "before": {"positive": ["voice"]},
            "conditions": {"negative": ["voice"]},
            "applies": {"positive": ["voice"]},
        },
    ]


def test_engine_slow(benchmark):
    with open("benchmarks/benchmark_input.txt", "r") as words_in:
        input_words = [word.strip() for word in words_in]

    words, rules = benchmark(engine.run_engine, input_words, generations=50)
