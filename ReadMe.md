# GFPS (GirlFriend Potential Score)

This repo contains an algorithm to assess whether or not a girl is worth pursuing. This
scale is based on looks, personally traits, and red flags. There is a self evaluation,
an initial evaluation that can be updated, and a relationship specific evaluation (v0.0.1 just has the girlfriend evaluation feature). 

The person is then ranked based on their own personality traits, and difficiencies between
the two of you are pointed out.

## setup

This repo is quite lightweight, just needing pandas and its dependencies. a virtual environment may not be necessary. 

```bash
# clone repo and change to directory
git remote set-url origin https://github.com/Yellowcactus23/GFPS.git
cd GFPS/

# set up virtual environment
python -m venv venv

source venv/Scripts/activate

pip install -r requirements.txt
```

## Usage

From here simply run: 

```bash
python bin/gfps.py
```

You will be prompted to:
1. Fill out your own assessment
2. Fill out the questions for the person you are evaluating
3. Have the options to:
    a. update entries
    b. compare entries
    c. set reminders to for new evaluations

## Editing params

Params can be edited in the `data/score_params.json` folder. The ranking params are 
based on relative percentages and are meant to be fixed. 

