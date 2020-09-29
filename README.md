__jargon__ is a minimalistic vocabulary trainer. Its main purpose is to keep creating and sharing your custom vocabulary simple, making it easier to learn domain-specific vocabulary. During practise, __jargon__ keeps track of your learning progress on every item, and trains your weakest items most.

# Install

In order to use __jargon__, you need to have Python [`Python 3.8`](https://www.python.org/downloads/) installed. Other (`Python 3.x` versions might work as well, but I haven't tested this).

With Python 3.8  installed, open a terminal, move to the location you want to install __jargon__ to, and clone the repository from GitHub (If you do not have `git` installed and do not want to install it, just download the directory from https://github.com/jonathan-scolbach/jargon.)

```
git clone git@github.com:jonathan-scholbach/jargon.git
```

That's it, you are set.

# Create Custom Vocabulary

Your custom vocabulary must be put in a [`csv`](https://en.wikipedia.org/wiki/Comma-separated_values) file which has to have two columns, separated by semicolon (`";"`). You can create this file with a simple text editor or, if this is more convenient for you, with a spreadsheet program such as [OpenOffice](https://www.openoffice.org/product/calc.html) Calc, Microsoft Excel or GoogleSheets

The first column contains the vocabulary in the target language you want to train. The second column contains the translation of the vocabulary into your native language.

If you want to name multiple synonyms in one of the languages, write them into the same cell, separated by comma.

For an example, have a look at the example csv file `example_vocabulary.csv` in the repository.

# Run

__jargon__ does not have a graphical user interface, but runs on the command line (terminal). In order to run __jargon__, you need to move into the directory you have installed __jargon__ to (in a terminal). 
Now you can run the Python script:

```
python3 practise.py <RELATIVE PATH TO YOUR VOCABULARY CSV> 
```

For example:

```
python3 practise.py ../lessons/advanced_english_from_german.csv 
```


## Options

When you invoke the script, you can (optionally) set several flags which change the way your knowledge is tested:

+ `-a` (or, with the same effect: `--alternatives`): This will make the program consider the synonyms as valid answers. If it is not set, all the synonyms have to be named by the user for the answer to be considered valid.

+ `-t` (or, with the same effect: `--typo`): This will make the program consider answers valid if they contain a typo.

+ `-i` (or, with the same effect: `--invert`): This flips the order of languages in the vocabulary file. It will make the program consider present you questions in the target language and ask for answers in your native language.

Besides setting these flags, you can (optionally) specify the following variables:

+ `-u` (or, with the same effect: `--user`): You can enter a user's name to keep track of progress individually.


## Finish

To finish your exercise, just type `"x"` when prompted for the vocabulary answer.
