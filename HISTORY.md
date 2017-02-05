# History #

## 2.0.0 ##

- Completely rewrote the evolution algorithm, using phonetic features rather
  than regexes.
- Evolution now optimises a given phonetic measurement when selecting rules to
  apply.
- Saving and loading rules now works perfectly.
- Applied rules are displayed cleanly in terms of features.
- The interface has been improved to provide more feedback to the user
- Fixed a bug that broke orthographic-to-IPA transcriptions
- Many miscellaneous bug fixes

## 1.0.0 ##

**Initial public version**

- Evolve a language for a given number of generations.
- See descriptions of all rules applied.
- Apply transcription rules from the language's orthography to IPA (so that an
  existing word list can be easily used).
- Evolve both forward and backward in time, i.e. the app can generate a child
  language or a parent language.
- Save and load generated rules to apply to new words.
