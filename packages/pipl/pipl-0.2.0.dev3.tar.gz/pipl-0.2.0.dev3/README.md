

pipl
====

**Package Index PipeLine**

Experimental pip/devpi based pipeline dependency platform


Why 
------

I have so many time heard that "CG Production is hard to industrialise because
every production is almost a prototype".
As a developer this excuse bothered me a lot because if one thinks that CG
productions are prototypes, how could he handle developing - the art of creating
something that solves a problem that has never been (correctly) solved before :D
That's as prototype as it gets !

Still, software developement has found its path to industrialization, and so
should CG Production.

So I've started to compare the CG project classical bits to the Dev ones, and
it hit me: There is very little difference between the two, let's use the DevOp
tools to build a CG Pipeline.

`pipl` is an attempt at making this idea real. (read "proof of concept / prototype')

How
------

One of the fundamental blocks at the core of a CG pipeline is the dependency
management. The idea behind `pipl` is to use python's packaging system as the
central dependency resolver.

Once every bit of the pipeline can be represented as a python package,
all the dependencies are automaticaly handled by a documented, robust and versatil
eco-system (Thanks the the Python Packaging Authority: www.pypa.io)

Official PyPA tools like setuptools, pip, virtalenv, pipenv... can be used
to resolve dependencies in isolated environments, manage updates, support
rc verions, lock dependencies, etc...

This idea also opens a great opportunity: use CI/CD system to react to package
publication. QA with tox is a obvious idea, but one can imagine anything if
the CI/CD system is used to execute 'pipeline' packages that process data from
upstream packages and generate/update+publish packages.

That would be leveraging another great advantage of treating everything as a python package: it is inherently procedural and executable, so everything *can* become
procedural and executable.

"What version of Maya should I use to open this scene ?" is a question no more:
Imagine that the task "Shot 303-909 Animation" is a python package with console_script entry_points like "OpenScene". This command would be available by simply activating a virtualenv, completely configured by adding dependencies to the task package.

`pipl` is not intended solely for shell usage. The CLI is a first citizen but care is given to have a nice python API two so that one can easily add a GUI/Workflow system on top (our plans include using www.kabaretstudio.com for that)

Last but not least, another nice feature gained by the usage of python packages is the entry_point system. By using it as a plugin system, pipl_pipe defines a extremely customisable framework: almost every aspect can be overridden by simply installing a package. The system is also very extensible, your are free to implement any pipeline and workflow.


Overview
------------
You will create and configure a `project`, then install or develop your `pipeline` inside a `workspace`, then publish them to the project index.
With the pipeline as dependency, you will create `Task` packages that will give the users the tools to create and edit `Assets`. 
When the users publish the `Task` package (to a stage index), a CI/CD handler will test them (QA) and push them to another stage index where another CI/CD handler will process them to create `Product` packages that store references to their associated `Assets`. Those `Products` will in turn be used as dependencies by some other tasks, and so on...

The `pipl` CLI workflow looks like this:

- **Create a project**
It's a folder with a special structure inside it.
- **Start the project's server**
It's a devpi server where all packages will be stored.
It's like our own personal PyPI...
- **Configure the project**
There are a few important steps now that the server is up:
	- You should change the root password, the default is "".
	- You **must** create the default package index
	- You may want to add some "users" (index owners)
	- You may want to add some staging indexes.
	- You **must** upload pipl-pipe packl to the defaut package index
	(nb: this is not implemented yet - *l o l* )
- **Create a Workarea** (optional, there's a default one)
It's a folder that knows which pipl project it belong to.
- **Create a Workspace**
It's a folder inside a Workarea that contains a virtualenv and can edit
packages.
- **Create a Packl**
It's a python package with special stuffing to make it simpler and programmatically controllable.
A packl can contain arbitrary python code, or represent a `Taks` or a `Product`.
- **Add Dependencies**
This install some packls from the project index and "links" them to your packl.
- **Edit the Packl**
	- If it's a code package, like the one configuring/implementing your pipeline (envset, configs, editors, asset types, asset store, product types, etc...), you should be able to use your favourite IDE.
	- If it's a *Task* package, it should provide some tools to auto-edit them. Just start the workspace-shell to use those tools.
	- If it's a *Product* package, the *Task* generating it will handle edition two.
- **Publish the Packl**
Depending on your worflow, you will publish directly to the project index or to a staging index where a CI/CD handler can run QA or processing tools.

Pipeline Implementation
------------------------------
So how do I "define my pipeline" within this system ?

	Note: This is not functionnal yet and very likely to change A LOT :p

The core functionalities of the pipeline, a.k.a the "pipeline framework", are provided by the pipl_pipe package. That's where the concepts of Assets, Products, Tasks, etc... are defined. And that's what gives you the tools to define your owns.

The pipl_pipe packl defines the `pipl_pack.services` object.
As every packl in the project will have a direct or indirect dependency to the pipl_pipe packl, this object is available everywhere.

It contains "*services*" like `config` which provide named configuration dicts, and `asset_store` which resolves asset paths based on a Product, an Asset type name and an Asset revision.

The first step to define your pipeline is to declare your configs, your Asset types, etc... Do let you do so, `pipl_pipe` uses the entry_point system.

**Config**

An `pipl_pip.config` entry_point will be automatically loaded as a config named by the entry name.
In your setup.py (or more likely, your \_\_setupl__.py), you just need to have:

	entry_points = {
	    'pipl_pipe.config': [
		# This is your asset_store config:
	        'asset_store = my_config:ASSET_STORE_CONFIG',
	        # You can define whatever name you want:
	        'kabaret = my_config:KABARET_CONFIG',
	    ]
	}

**Asset types**

Note that the term `Asset` may not be used here like you are used to.
By `Asset` we mean "*A file or a folder that is generated by a user or a process and that exists with a different version/revision for each generation*".
More pragmatically, Assets are file that cannot be embedded in a python package, most likely because they are to big.

`pipl` take on those files is inspired by git-lfs: just hold a reference to the asset inside the package and delegate their storage (in our case, to the `asset_store` service)

The reason why you will want to define your own Asset subclasses is that Asset are responsible for their managed file *basenames*. So implementing a **naming convention** is done by defining your Asset types (and also overriding the `asset_store` service which is responsible for Asset managed file *paths*, see the "*Custom Services*" section below)

	Note: This bothers me and we'll probably find a proper way to have all the naming convention implemented is Asset only, or in the asset_store only.

Defining Asset types is easy, just inherit `pipl_pipe.asset_store.Asset`  and register your public Asset types with the `pipl_pipe.asset_store.register()` decorator:

	from pipl_pipe.asset_store import Asset, registered

	class _MayaScene(Asset):
	    pass

	@registered
	class MayaAscii(_MayaScene):
	    def __init__(self, storage, product, asset_name):
	        super(MayaAscii, self).__init__(
	            storage, product, asset_name, 'ma'
	        )
This means that in order to use a specific Asset type, you will need a dependency to the package defining it **AND** you will need to import it (or the registration won't be triggered).

This is so to avoid polluting your python with unused Asset. As you are likely to implement all your assets in a single package, using entry_points would load them all. With the classical import method you can split them into submodules and only load the ones you need.

	Note: this is an obvious case of early optimisation and is likely to get replaced by entry_points :p)

**Custom Services**
     
Services are loaded on the entry_point group `pipl_pipe.services`, with the name of the service. Just provide a factory function (or a class) that accept a config as argument. If a config of the same name exists, it will automatically be provided.

This is for example how you would provide your own `asset_store` service. (nb: this is not true in current imp. but it will be soon ^^)

You can even add your own extra services, you don't have overwrite an existing one.

**Product**

The Products are the part you will work on most. They are defining all the procedures and all the code to apply them.

A Product is a packl containing code that instantiates a Product class.

Products packls have enty_points for each of their Asset, giving managing tools the ability
to act on all Assets of a given workspace (i.e. to copy all assets in workspace's asset storage and be able to work w/o access to the project)

Products have (typed) entry_points for them, so that Products and Tasks depending on them can access them. The Product base class has functions to get dependencies based on their type.

The Product types are available in the `tasks` service. You install yours with the entry_point `pipl_pipe.task_type`. 

Each Product has a dependency to the package declaring its Product type.

	NB: using a service to get a base class feels weird :/ 

	TODO: polish this section (how to declare product types ?)
	
**Task**
                                           
Tasks are a special types of Product.

If you know why we must use abstract dependencies when developing a library and concrete dependencies when developing an application, know that a Product is a library and a Task is an application.

If you don't, just keep on not caring ;)

A Task is a packl containing code that instantiates a Task class.

A `Task` defines (thru entry_points) executable commands (build a scene using upstream packls, open maya with a particular scene, view a sequence of images, ...) and can edit/create/publish packages (Products).

This is where you build a scene, let the user edit it, then export/render Products from it (in a CI/CD handler)

There should be only one task per workspace (I don't know why yet but it feels important and I'll probably find why later ;) )

Tasks creation is done by creating a new packl and executing the command `create_task <packl_name> <task_type>`in the workspace shell.
This command is declared by pipl_pipe and will edit the packl \_\_init__.py and \_\_setupl__.py to turn it into the desired task.

The Task types are available in the `tasks` service. You install yours with the entry_point `pipl_pipe.task_type`.
 
	TODO: polish this section (Task type declaration)

**EnvSet**

EnvSet are packl that instantiate an EnvSet class.

Their purpose is close to what you do with rez: resolve environment variable based on dependencies and specified requirements.

There is an EnvSet package per dependency+requirement since we handle both with package dependencies.

	Note: EnvSet are not yet implemented (nor well defined)

**Tools/Editors**
                         
Tasks provide commands, but those commands don't need to be defined in the Tasks. Tools/Editor packages would be used as 'edit' extra_requires and would use EnvSet to define commands.

Editor dependencies would be installed only in user workspace (not in CI/CD ones) thanks to the extra_requires machinery.

	Note: This is not well defined yet.


Installation
------------

Create a virtual env, install and update using pip:

.. code-block:: text

    $ pip install -U pipl


Usage
-----

The package defines the `pipl` command line tool.

Use `pipl --help` to list available commands:

.. code-block:: text

    (venv) $ pipl --help
    Usage: pipl [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      packl
      proj
      work

Use `pipl COMMAND --help` to list sub commands:

.. code-block:: text

    (venv) $ pipl proj --help
    Usage: pipl proj [OPTIONS] COMMAND [ARGS]...

    Options:
      --help  Show this message and exit.

    Commands:
      create  Creates a new project at path
      index   Project indexes administration.
      start   Start project's server in **foreground**.
      user    Project users administration.


When appropriate, commands will guess the *current* project/workspace/package
from current path. Use an extra argument to override current path.


Project Init
------------

Create a project and navigate into it:

.. code-block:: text
    
    (venv):~ $ pipl proj create /path/to/MyProject

Open a new shell within the same virtualenv and start the project's server:

.. code-block:: text
    
    (venv):~ $ cd /path/to/MyProject
    (venv):/path/to/MyProject $ pipl proj start

Now in your first shell, you can list users:

.. code-block:: text
    
    (venv):~ $ cd /path/to/MyProject
    (venv):/path/to/MyProject $ pipl proj user list
    Resolving Project path from .
    Found Project at /path/to/MyProject
    Connecting to http://localhost:3141 (user:None, pass:None)
    Found 1 user(s) in project /path/to/MyProject:
          root
    Disconnected.


Root's default password is an empty string.
Admin commands will need it, be sure to use "" and not '' in command lines.

The best is to change it asap:

.. code-block:: text
     
    (venv):/path/to/MyProject $ pipl proj user set "" root --password 123
    Resolving Project path from .
    Found Project at /path/to/MyProject
    Connecting to http://localhost:3141 (user:root, pass:None)
    Disconnected.


Now you can create some users using the new root password:

.. code-block:: text
    
    (venv):/path/to/MyProject $ pipl proj user add 123 bob b0b bob@pipl.io
    Resolving Project path from .
    Found Project at /path/to/MyProject
    Connecting to http://localhost:3141 (user:root, pass:***)
    Disconnected.


You will need some index to store your package. The default one can be 
created with:

.. code-block:: text
    
    (venv):/path/to/MyProject $ pipl proj index create-default 123
    Resolving Project path from .
    Found Project at /path/to/MyProject
    Creating default project index for "."
    Connecting to http://localhost:3141 (user:root, pass:***)
    Disconnected.

    (venv):/path/to/MyProject $ pipl proj index list-indexes
    Resolving Project path from .
    Found Project at /path/to/MyProject
    Connecting to http://localhost:3141 (user:None, pass:None)
    Found 2 Index(es) in project /path/to/MyProject:
               root/PROJ
    Disconnected.


Workspaces Creation
-------------------
	
	removed outdated doc


Package Creation
----------------

	removed outdated doc (beware: the "pipl pack" command is obsolete)

Package Setup
-------------

	removed outdated doc (beware: the "pipl pack" command is obsolete)

Package Edition
---------------

	removed outdated doc (beware: the "pipl pack" command is obsolete)

Package Upload
--------------

	removed outdated doc (beware: the "pipl pack" command is obsolete)



