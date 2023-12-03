# Secret Santa Drawing

The program randomly pairs people with additional constraint on which people can't be paired together. 

## Requirements:

Requirements are listed in environment.yml
You can install and create an environment with all the dependencies with `mamba`:

```
mamba env create -f environment.yml
mamba activate secret_santa
```

## Dev config:

```
pre-commit install
pre-commit run --all-files
```
