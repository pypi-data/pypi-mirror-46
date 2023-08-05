# What it is

treep is a project manager, where "project" refers to a collection of git repositories.
It aims to:

- cloning and performing batch git actions on all repositories contained in the workspace
- having an overview of the workspace (e.g. which repositories are ahead of master ?)
- helping compiling the workspace even if this latest comprises package supporting different compilation methods (e.g. cmake, pip, catkin)

To use treep you need:

- to install treep
- to create a folder called 'treep_XXX' (replace XXX by anything of your choices) containing at least: 
    - a file repositories.yaml in which the URLs of repositories are given
    - a file projects.yaml which defines projects (i.e. grouping of repositories that can be cloned/managed together)


# installation

Treep supports python2.7 and python 3

```bash

pip install treep

```

# configuration

Example of **repositories.yaml** file:

```yaml
my_robot:
    path: src/robots/
    origin: robot
    branch: master
    compilation: catkin
my_controller:
    path: src/controllers/
    origin: git@github.com:my_name/my_controller.git
    compilation: cmake
my_logger:
    path: src/utils
    origin: git@github.com:my_name/my_logger.git
    compilation: pip
```

- path : relative path in which the repositories will be cloned by treep (e.g. /src/robots will resolve to \<absolute path to treep_XXX\>/../workspace/src/robot)
- origin : the URL of the repository, or a URL prefix defined in configuration.yaml (e.g. "robot", explained later in this file)
- branch (optional) : branch to checkout. Master by default
- compilation (optional) : will be used by treep to generate compilation scripts (explained later in this file). This need a file configuration.yaml to be also present.

Example of **projects.yaml** file:

```yaml
ROBOT:
    parent_projects: []
    repos: [my_robot,my_controller]
FULL_ROBOT
    parent_projects: [ROBOT]
    repos: [my_logger]
```

This file declare 2 projects:

- ROBOT (which contains my_robot and my controller) 
- FULL_ROBOT (which contains my_robot, my_controller and my_logger)

Example of **configuration.yaml** file

The repositories.yaml file above uses 4 tags that requires definition: catkin, cmake, pip and robot. They are to be defined:

```yaml
origin_prefixes:
    robot: 'git@github.com:my_account/'
compilation:
    catkin:
        default: {install=True}
    pip:
        default: {pip_executable: 'pip', user=True}
    cmake:
        default: {clean: True, multiprocess: True, cmake_suffix: ""}
```

- declaring "robot" as origin_prefixes allowed to declare the origin of "my_robot" in repositories.yaml as just "robot". Treep will resolve the url of "my_robot" to git@github.com:my_account/my_robot.git
- compilation supports natively "catkin", "pip" and "cmake". Setting compilation tags in configuration.yaml and using them in repositories.yaml will allow treep to generate compilation scripts for the workspace, as described later in this document

# Usage

Once treep has been installed and the treep configuration folder has been created (in this example in ~/Software):

```bash
# we assume treep_xxx folder is in ~/Software
cd ~/Software 
treep
```

will display all arguments supported by treep. We hope they are self explanatory.

For example, assuming that treep_xxx/projects.yaml defines a project "FULL_ROBOT":

```bash
treep --projects # will display list of known projects, including "FULL_ROBOT"
treep --clone FULL_ROBOT # will clone all repos of "FULL_ROBOT"
treep --status # will display state of the workspace
```

# Autocompletion

treep uses argcomplete to provide autocompletion.
More info here:

[https://github.com/kislyuk/argcomplete](https://github.com/kislyuk/argcomplete)

In short, to activate autocompletion, run in a terminal (may need sudo rights):

```bash
activate-global-python-argcomplete
```

# Generating yaml configuration files

**repositories.yaml** and **projects.yaml** files can be generated automatically using the command **treep_to_yaml** :

- clone all the repositories of interest in a folder called "workspace"
- from the folder containing "workspace", call "yaml_to_treep"

For example:

```bash
mkdir ~/Software
cd ~/Software
mkdir workspace
cd workspace
mkdir src/
cd src
clone git@github.com:vincentberenz/playful_kinematics.git
clone git@github.com:vincentberenz/lightargs.git
cd ~/Software
treep_to_yaml 
```

# Using several configuration folders

Treep supports using several configuration folders at once, which then need to be in the same folder. Treep will behave as if using a single configuration folder which defines the repositories and projects of both folders.

# Generating a compilation script for the workspace

## natively supported

In the example above, **repositories.yaml** was defining:

```yaml
my_robot:
    path: src/robots/
    origin: robot
    branch: master
    compilation: catkin
```

and **configuration.yaml**:

```yaml
compilation:
    catkin:
        default: {install=True}
```

If "my_robot" has been cloned in the workspace, this will result in :


```bash
treep --compilation-script
```

to generate a file **compilation.sh** which will call the suitable bash commands to build the workspace (in this case using catkin_make).
If other repositories with other tags (e.g pip, cmake) have been cloned, compilation.sh will also contain the commands to compile them.

## custom made

It is possible to use custom developed python scripts for generating compilation.sh. For this you need to create in treep_xxx a file **compilation.py**:

```python
def my_script_generator(workspace_path,
                        package_name,
                        package_path,
                        arg1="1",
                        arg2="2"):
                        
    # here write code for returning the bash script string that
    # will perform compilation of the code in workspace_path/package_path
                        
```

To create such script, you may take for example inspiration from : [https://git-amd.tuebingen.mpg.de/amd-clmc/treep/blob/master/treep/cmake.py](https://git-amd.tuebingen.mpg.de/amd-clmc/treep/blob/master/treep/cmake.py)

This file **compilation.py** allows the file **configuration.yaml** to define for example:

```yaml
compilation:
    my_script_generator:
        default: {}
        my_gen: {arg1:"5"}
```

which then would allow in **repositories.yaml**:


```yaml
my_robot:
    path: src/robots/
    origin: robot
    branch: master
    compilation: my_script_generator
my_controller:
    path: src/controllers/
    origin: git@github.com:my_name/my_controller.git
    compilation: my_gen
```

# Credit

Treep has been developed and is maintained by the Max Planck Institute for Intelligent Systems, Tuebingen, Germany

# Versions changes

## version 1.34

- fixed typos in README
- added this log of changes in README
- fixed bug in checkout branch
- pulling with orange output when pulling worked but did not update the repo for any valid reason

## version 1.33

- updated README.md and fixed setup.py to use it for project description

## version 1.32

- fixed bug in status, does not attempt to create status from non git repo anymore
- cloning now also cloning submodules
- fixed display of status and pull of repos (better tabulation)
- pulling, fetching and cloning now multiprocess
- added compilation script generation

## version 1.31

- process calls: transforming output to unicode for support of python3
- files: yaml loader compatible both newer and older versions of pyyaml
- status : display of status message improved for python3
- status : does not fail anymore on detached head

## version 1.3
