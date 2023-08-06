# PropArgs
A module for systematically organizing user preferences acquired from a data store, env vars, a parameter file, the command line and/or user choices.

## How it Works

### Overview
PropArgs is initialized by sequentially loading the following five stages of input:

1. Data Store
2. Environment
3. Property File
4. Command Line
5. User

The above is the default ordering. The user may change that order.

Properties may be added in any stage except User. A property defined in one stage may be overwritten in later stages. 

Each property has a key and a value and is accessed like a dictionary:

    >>> pa = PropArgs.create_props()
    >>> pa["prop_nm"] = 1  # assigns the value 1 to the property "prop_nm"
    >>> pa["prop_name"]
    1

In addition to this, each property may have associated metadata. These are at present: a question for the
user-input prompt, a datatype, an upper bound, and a lower bound. If at any point in the loading process the
metadata rules are broken (e.g. the val exceeds the upper bound) an error will be raised.

The system has some similarities to the traitlets configuration module developed for iPython and Jupyter, but is more flexible, seeks configuration info from more sources, and is not tied to Python classes. (The property structure itself keeps the config info, but those values may be loaded into clases or not as per the needs of the application.)

### Details

#### Data Store
The Data Store will be either a JSON file or a database.

The Data Store file will be specified on initialization

    PropArgs.create_props(ds_file=file_name)

The JSON formatting is as follows:

    {
        "prop_name_1": {
            "val": 1,
            "question": "What value should this property have?",
            "atype": "INT",
            "hival": 10,
            "lowval": 0
        },
        "prop_name_2": {
            "val": "Hello World."
        },
        "prop_name_3": {
        }
    }

Note that a property need not have all (or any) fields defined. If no "val" is specified, it defaults to `None`.

Details on database data stores to come ...


#### Environment
PropArgs will read and add all the environment variables of the program in which PropArgs is initialized.
(i.e. everything in python's os.environ)


#### Property File
A property file will be specified on initialization:

    >>> pa = PropArgs.create_props(prop_file=file_name)

Currently the only Property File type supported is JSON. The formatting is the same as the Data Store's 
JSON formatting:

    {
        "prop_name_1": {
            "val": 1,
            "question": "What value should this property have?",
            "atype": "INT",
            "hival": 10,
            "lowval": 0
        },
        "prop_name_2": {
            "val": "Hello World."
        }
    }


#### Command Line
Properties will be read from the command line as follows

    $ python program_reading_props.py --props prop_1=val_1,prop_2=val_2,prop_3=val_3  #etc...

#### User
The final stage is to ask the user for input. The user will only be prompted about properties that have a question.

The default behavior is to prompt questions on the client's command line:

    >>> pa = PropArgs.create_props()
    What is the value of prop_1? ("I'm the default prop value") <enter_value>
    What is the value of prop_2? [0.0-100.0] (20) <enter_value>

However, the client program may take over and ask questions in its own way. In this case we will provide a flag
that skips the user stage, and instead the client will call `pa.get_questions()` for a JSON of the properties with
questions.

    >>> pa = PropArgs(skip_user_questions=True)
    >>> pa.get_questions()
    {
        "prop_name_1": {
            "val": 2.0,
            "question": "",
            "atype": "DBL",
            "hival": 10.0,
            "lowval": -0.5
        },
        "prop_name_2": {
            "val": "default",
            "question": "What should prop_name_2 be?"
        }
    }

## Credits
Idea - Robert Dodson

Development - Gene Callahan and Nathan Conroy
