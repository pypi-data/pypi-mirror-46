# Experiment replay

## Description

Simple utils to record the commands you run. It was developped with ML experiments
in mind. Where you often tweak your code just a little before launching an experiment
and when after a few days/weeks you come back you want to know how you achieved such
amazing results you don't remember and it takes a long time to achieve again.

This library is extremely simple. You can't run any experiment that is not committed
so you have a commit to know what was changed and why. It also stores the exact command
line you used so that configuration hacking is also remembered. It uses the git commit
message to store that data so it does not require any external tool.

## Install

`pip install experiment_replay`

## Usage

It's simple to enable an experiment just do  in your `train.py` file for instance

```python
import experiment_replay

## My code

if __name__ == "__main__":
    experiment_replay.setup()
    my_training_loop()
```

Then when you actual run your training let's say `python train.py --batch-size=16`.

You can then do:

`python -m experiment_replay` to get the list of all the commands you ran with
experiment_replay enabled.

```
Experiments :
Date                       Id     Commit                                   Command             
2019-05-13 14:53:35.410538 472a12 f9dfe80125ea4856ce368270bce3aeb980829b2c python example.py  
```

You can they replay it with `python -m experiment_replay 472a12`
