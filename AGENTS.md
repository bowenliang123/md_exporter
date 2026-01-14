# AGENTS.md

## Project Overview

`md_exporter`, aka `Markdown Exporter`, is a project for exporting Markdown text to files in other formats, such as HTML, PPTX, CSV, etc. This project can be used as either a [Dify Plugin](https://docs.dify.ai/en/develop-plugin/dev-guides-and-walkthroughs/tool-plugin) or a Claude [Agent Skill](https://agentskills.io/specification).

### Dependencies

#### Dependencies Manager
- `uv` is preferred as the dependencies manager.
- project dependencies are defined in `pyproject.toml`.
- `uv pip` can be used as `pip` replacement to install the required Python packages.

#### Required Python Dependencies
- try the best to keep `requirements.txt` aligned with dependencies defined in `pyproject.toml`.
- when running the project as a Dify Plugin
    - `requirements.txt` will be used to install the required Python packages with `pip`
    - `dify_plugin` is only required when running the project as a Dify Plugin.


### Dify Plugin

This project can be used as a Dify Plugin. 

#### Run the plugin locally

Run the plugin locally with `uv`:
```bash
uv run python -m main
```

As it's running as Dify plugin, it will try to connect to a Dify server, which is not always available.
It's alright and ignorable to see the following error message:
1. `Failed to connect to localhost:5003`, as the Dify server is not running.
2. `Broken pipe`, as the Dify server switched the accepted `REMOTE_INSTALL_KEY` which is set and should be the same in `.env` on plugin side.

#### Scripts and Resources used for Dify Plugin
- `manifest.xml` - Dify Plugin manifest file.
- `tools` - Dify Tools
    - `tools/md_to_XXX` - Dify Tool implementation code for converting Markdown to XXX format in `tools/md_to_XXX/md_to_XXX.py` and Dify tool specification in `tools/md_to_XXX/md_to_XXX.yaml`.
- `/scripts/services/*.py` - Shared python code used for Dify Plugin and Agent Skill.
- `.env` - Environment variables for running the Dify Plugin
- `/_assets` - Assets used by both Dify Plugin, such as Dify Plugin icons, images used in `README.md`, etc.
- `/assets` - Assets used by both Agent Skill and Dify Plugin, such as file templates used for generating `.docx` and `.pptx` files

### Claude Agent Skill

The main usage of the Agent Skill can be found in `SKILL.md`.
The `SKILL.md` tells how to use the Agent Skill, including the arguments, options, and examples.

Unlike the Dify Plugin, the Agent Skill is not running as a server. It should be able to be executed locally.


For example, to translate a Markdown table to Excel file `.xlsx`, run the following command:

```bash
uv run --with 'dep1,dep2~=1.0.0,dep3>=2.0.0' python scripts/md_to_xlsx.py <input> <output> [options]
```

#### Scripts and Resources used for Dify Plugin
- `SKILL.md` - Agent Skill specification file and the usage guides and examples of the kills.
- `/scripts/md_to_XXX.py` - Skill implementation code for converting Markdown to XXX format.
- `/scripts/services/*.py` - Shared python code used for Dify Plugin and Agent Skill.
- `/assets` - Assets used by both Agent Skill and Dify Plugin, such as file templates used for generating `.docx` and `.pptx` files

## Development Guide

### Code Linting and Formatting

- do the linting and formatting every time the Python code is modified and before running the code.
- run `dev/reformat` to lint and format the code with `ruff`.
- The ruff rules and configs are defined in `ruff.toml`.

### Testing
- test files are located in the `tests` folder, which are testing the each script and tool of Agent Skills and can be run in standalone
- - run `dev/test` to test all scripts with `pytest`.

### Exclusions
- The `md2pptx-X.Y.Z` folder contains upstream code of `md2pptx` project used for Markdown to PPTX conversion. The content of this folder should be kept as-is and excluded from linting, formatting, and testing.
