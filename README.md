__jargon__ is a *minimalistic* vocabulary trainer which lets (and makes) you define your vocabulary on your own. When you train your vocabulary, __jargon__ keeps track of your success on every word, and trains your weakest words most.

# Install

In order to install __jargon__, the following prerequisites are required:

+ [`git`](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) (optional, pre-installed on Linux and Mac)
+ [`Python 3.8`](https://www.python.org/downloads/)
+ [`virtualenv`](https://pypi.org/project/virtualenv/) (optional)
+ `pip` (usually installed with Python)

With these prerequisites installed, open a terminal, move to the location you want to install __jargon__ to and type:

```
git clone git@github.com:jonathan-scholbach/jargon.git
cd jargon
virtualenv env --python=python3.8
pip install -r requirements.txt
```

If you do not have `git` installed and do not want to install it, just download the directory from https://github.com/jonathan-scolbach/jargon and proceed from the second line. If you do not have `virtualenv` installed and do not want to install it, you can skip the third line. This will install the requirements globally on your machine.

# Create Custom Vocabulary

## Format
Your custom vocabulary must be put in a [csv](https://en.wikipedia.org/wiki/Comma-separated_values) file which has three columns, separated by semicolon (`";"`). The first column contains the vocabulary in the target language you want to train, the second column contains the translation of the vocabulary into your native language, the third column must be called "success". Keep it empty, it will be used to track your performance for each vocabulary.

If you want to name multiple synonyms in one of the languages, separate them by comma.

# Run

In order to run __jargon__, you need to move into the directory you have installed __jargon__ to. If you were using the virtual environment during install, you have to activate it first, by typing in a terminal:

On Linux / macOS:

```
source env/bin/activate
```
 
On Windows:

```
env\Scripts\activate.bat
```

Now you can run the Python script:

```
python train.py <RELATIVE PATH TO YOUR VOCABULARY CSV> 
```

For example:

```
python train.py ../lessons/advanced_english_from_german.csv 
```

If you do not provide the path to your vocabulary, `vocabulary.csv` will be used as a default.

To finish your exercise, just type `"x"` when prompted for the vocabulary answer.

# Missing Features

__jargon__ is minimalistic, it is written just to provide an easy way to exercise on custom vocabulary. Hence there are some functionalities you might miss:

## Multiple Users

__jargon__ does not have built-in functionality to keep track of learning progress of different users. However, multiple users can track their performance individually by creating separate vocabulary files or directories per user.

## Lessons

__jargon__ does not separate vocabulary in different lessons. However, you can organize your different lessons in different vocabulary csv files.

## Typo Correction

__jargon__ does not correct for your typos during exercise. Only the very correct word spelling is accepted, as stated in your vocabulary csv file. You have to type correctly.
