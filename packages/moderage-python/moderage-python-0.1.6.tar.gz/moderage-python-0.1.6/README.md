# Mode Rage client

[![PyPI version](https://badge.fury.io/py/moderage-python.svg)](https://badge.fury.io/py/moderage-python)

## What is ModeRage

ModeRage is a light-weight tool for storing experimental results and models. Experiments are referenced by their 
*metacategory* and *id*.

### Meta Categories

Experiments in ModeRage have a meta-category, which basically defines the *type* of experiment. 
Think of meta-categories as an identifier for a project that may contain many experiments or datasets of the same type.

For example, when running many experiments with several sets of hyperparameters, those experiments will be saved into 
the same meta-category.

### Ids

Once an experiment is saved it has an *id*. This can be used to load the experiment.

## Configuration

ModeRage can be started in `local` or `server` mode.

### Local

In local mode, ModeRage will save files locally to a `~/.moderage` folder

### Server

The ModeRage Server hosts experiments, data and metadata so it can be access from anywhere. 

You can view it here (CURRENTLY UNDER DEVELOPMENT):
[Server](https://gitlab.com/chrisbam4d/modage-backend)

#### UI

The ModeRage UI communicates with the ModeRage server and allows browsing of experiments and data

You can view it here (CURRENTLY UNDER DEVELOPMENT):
[UI](https://gitlab.com/chrisbam4d/moderage-ui)

## Configuration file

Configuration in ModeRage is defined in a `.mrconfig` file. If no config file is created, 
ModeRage will automatically start in `local` Mode

## Saving results

To save any number of files with some meta data you do the following:

### 1. Define a Meta object

```python
mymeta = {
    'hyperparameter1': 100,
    'hyperparameter2': 200,
    'hyperparameter3': 0.7,
}
```

### 2. (Optional) Define any files you want to upload

```python
myfiles = [
    {
        'filename': './path/to/myfile.csv',
        'caption': 'This is my file that contains my results'
    },
    {
        'filename': './path/to/mygraph.png',
        'caption': 'This is my file that contains my graph'
    },
    ...
]
```

### 4. (Optional) Reference any other experiments that this experiment is dependent on.

In many situations your experiment may rely on generated datasets or pre-trained models that also have many hyper-parameters.
You can reference those `parent` experiments by adding them to the parent object

```python
myparents = [
    {
        'id': [THE ID OF THE PARENT EXPERIEMENT],
        'metaCategory': 'generated_dataset'
    },
    {
        'id': [THE ID OF THE PARENT EXPERIEMENT],
        'metaCategory': 'pretrained_model'
    }
]
```

### 5. Call `save`

```python
experiment = mr.save('category_name', mymeta, files=myfiles)
```

## Loading results

Loading a saved experiment is simple, you just need to know the *meta-category* and the *id* of the experiment.

```python
experiment = mr.load(id, meta_category)
```

Once the experiment is loaded, the meta information and files from the experiment can be accessed.

For example: 
```python
meta = experiment.meta
parents = experiment.parents
files = experiment.files

file = experiment.get_file('mygraph.png')
```

