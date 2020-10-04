__jargon__ is a minimalistic vocabulary trainer. Its main purpose is to keep creating and sharing your custom vocabulary simple, making it easier to learn domain-specific vocabulary. During practise, __jargon__ keeps track of your learning progress on every item, and trains your weakest items most.

# Install

In order to use __jargon__, you need to have Python [`Python 3.8`](https://www.python.org/downloads/) installed. Other (`Python 3.x` versions might work as well, but I haven't tested this).

With Python 3.8  installed, open a terminal, move to the location you want to install __jargon__ to, and clone the repository from GitHub (If you do not have `git` installed and do not want to install it, just download the directory from https://github.com/jonathan-scolbach/jargon.)

```
git clone git@github.com:jonathan-scholbach/jargon.git
```

That's it.

# Create Custom Vocabulary

You can organize your vocabulary in _lessons_ and _courses_. A _lesson_ is a collection of vocables you want to train, and a _course_ is a collection of lessons.

## Lessons

You can create a lesson by creating a simple [`csv`](https://en.wikipedia.org/wiki/Comma-separated_values) file with either two or three columns, separated by semicolon (`";"`). You can create this file with a simple text editor or, if this is more convenient for you, with a spreadsheet program such as [OpenOffice](https://www.openoffice.org/product/calc.html) Calc, Microsoft Excel or GoogleSheets

The first column contains the vocable in the target language you want to train. The second column contains the vocable translated in your native language. The third column optionally contains a hint for the vocable. It is not mandatory to provide a third column; if you have a hint for some vocables in the file, you can still leave the third column empty for other vocables.

If you want to name multiple synonyms of the vocable in one of the languages, write them into the same cell, separated by a pipe (`"|"`).

For an example, have a look at the example csv file `example_vocabulary.csv` in the repository.

## Courses

For creating a course, simply put the csv files of the lessons into one directory. The lessons will be named and sorted by their filename. For sorting purposes, you can add a prefix to the name, separated by a double underscore (`"__"`) which will be ignored for the naming of the lesson. So, for instance, name your lessons like so:

+ `A__Nouns I.csv`
+ `B__Verbs I.csv`
+ `C__Idioms.csv`
+ `D__Nouns II.csv`
+ `E__Adjectives / Adverbs.csv`
+ `Z__Verbs II.csv`

Make sure all your lessons file names have the `.csv` file extension, because only those files will be recognized as lessons.

You can also include one `.txt` file in the course's directory which is supposed to contain a short description of the course.

# Run

## Start

__jargon__ does not have a graphical user interface, but runs on the command line (terminal). In order to run __jargon__, you need to move into the directory you have installed __jargon__ to (in a terminal). 
Now you can run the Python script:

```
python3 jargon.py <RELATIVE PATH TO THE COURSE DIRECTORY> 
```

For example, to run the course "advanced_english" in the 

```
python3 jargon.py ../en/advanced_english
```


## Options

When you invoke the script, you can (optionally) set several flags which change the way your knowledge is tested:

+ `-a` (or, with the same effect: `--alternatives`): This will make the program consider the synonyms as valid answers. If it is not set, all the synonyms have to be named by the user for the answer to be considered valid.

+ `-t` (or, with the same effect: `--typo`): This will make the program consider answers valid if they contain a typo.

+ `-i` (or, with the same effect: `--invert`): This flips the languages in the vocabulary file, i.e. it will make the program present questions in the target language and ask for answers in your native language.

Besides setting these flags, you can (optionally) specify the following variables:

+ `-u` (or, with the same effect: `--user`): You can enter a user's name to keep track of progress individually.


## During the Exercise

When prompted for a certain vocable, you can ask for a hint to be displayed by typing a question mark (`"?"`) instead of an answer.

To finish your exercise, just type `"x"` when prompted for the vocable.