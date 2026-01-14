---
name: markdown-exporter
description: An Markdown exporter for transform Markdown text to DOCX, PPTX, XLSX, PDF, PNG, HTML, MD, CSV, JSON, JSONL, XML files, and extract code blocks in Markdown to Python, Bash,JS and etc files. Also known as the md_exporter skill.
allowed-tools: 
disable: false
---


## ✨ What is Markdown Exporter?

**Markdown Exporter** is a powerful skill that transforms your Markdown text into a wide variety of professional formats. Whether you need to create polished reports, stunning presentations, organized spreadsheets, or code files—this tool has you covered.


## Prerequisites

To use the Markdown Exporter skill, ensure you have the following prerequisites installed:
- Python 3.11 or higher
- (optional) uv package manager


## 📦 Usage

### Overview
All scripts provided in this project are Python scripts located in the `scripts/` directory. All required Python dependencies are declared in the project's [pyproject.toml](./pyproject.toml) file.

### Recommended Execution Method
We strongly recommend using the `uv` package manager for running the scripts, as it simplifies dependency management and execution. Here's how to proceed:

1. **Check if `uv` is installed**:
   ```bash
   uv --version
   ```
   If `uv` is not installed, you can install it following the official instructions at https://docs.astral.sh/uv/getting-started/installation/ or use the alternative method described below.

2. **Execute scripts with `uv`**:
   ```bash
   uv run --with package1,package2,package3 python scripts/some_script.py <args> [options]
   ```
   Replace `package1,package2,package3` with the actual dependencies required for the script (refer to pyproject.toml). This command automatically installs the specified dependencies and runs the script in one step.

### Alternative Execution Method (Without `uv`)
If you don't have `uv` installed, you can use `pip` to manage dependencies:

1. **Check Python version**:
   Ensure you have Python 3.11 or higher installed:
   ```bash
   python --version
   ```

2. **Install dependencies**:
   ```bash
   pip install package1 package2 package3
   ```
   Replace `package1 package2 package3` with the actual dependencies required for the script.

3. **Run the script**:
   ```bash
   python scripts/some_script.py <args> [options]
   ```

### Important Notes
- Always navigate to the root directory of the project before executing any scripts.
- The exact dependencies required for each script are specified in the project's pyproject.toml file.
- For simplicity, you can install all dependencies at once using:
  ```bash
  pip install -r requirements.txt  # If requirements.txt is available
  # or
  uv run --with-all python scripts/some_script.py <args> [options]  # Using uv
  ```


## 🔧 Scripts

### md_to_csv - Convert Markdown tables to CSV

Converts Markdown tables to CSV format.

```bash
python scripts/md_to_csv.py <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path or Markdown text
- `output` - Output CSV file path

**Options:**
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
python scripts/md_to_csv.py ./abc.md ./tt.csv
```


### md_to_pdf - Convert Markdown to PDF

Converts Markdown text to PDF format with support for Chinese, Japanese, and other languages.

```bash
python scripts/md_to_pdf.py <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path or Markdown text
- `output` - Output PDF file path

**Options:**
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
python scripts/md_to_pdf.py ./abc.md ./output.pdf
```


### md_to_docx - Convert Markdown to DOCX

Converts Markdown text to DOCX format using pandoc.

```bash
python scripts/md_to_docx.py <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path or Markdown text
- `output` - Output DOCX file path

**Options:**
- `--template` - Path to DOCX template file (optional)
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
python scripts/md_to_docx.py ./abc.md ./output.docx
python scripts/md_to_docx.py ./abc.md ./output.docx --template ./template.docx
```


### md_to_xlsx - Convert Markdown tables to XLSX

Converts Markdown tables to XLSX format with multiple sheets support.

```bash
python scripts/md_to_xlsx.py <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path or Markdown text
- `output` - Output XLSX file path

**Options:**
- `--force-text` - Convert cell values to text type (default: True)
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
python scripts/md_to_xlsx.py ./abc.md ./output.xlsx
```


### md_to_pptx - Convert Markdown to PPTX

Converts Markdown text to PPTX format using md2pptx.

```bash
python scripts/md_to_pptx.py <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path or Markdown text
- `output` - Output PPTX file path

**Options:**
- `--template` - Path to PPTX template file (optional)

**Example:**
```bash
python scripts/md_to_pptx.py ./abc.md ./output.pptx
```


### md_to_codeblock - Extract Codeblocks to Files

Extracts code blocks from Markdown and saves them as individual files.

```bash
python scripts/md_to_codeblock.py <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path or Markdown text
- `output` - Output file or directory path

**Options:**
- `--compress` - Compress all code blocks into a ZIP file

**Example:**
```bash
python scripts/md_to_codeblock.py ./abc.md ./output_dir
python scripts/md_to_codeblock.py ./abc.md ./output.zip --compress
```


### md_to_json - Convert Markdown Tables to JSON

Converts Markdown tables to JSON or JSONL format.

```bash
python scripts/md_to_json.py <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path or Markdown text
- `output` - Output JSON file path

**Options:**
- `--style` - JSON output style: `jsonl` (default) or `json_array`
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
python scripts/md_to_json.py ./abc.md ./output.json
python scripts/md_to_json.py ./abc.md ./output.json --style json_array
```


### md_to_xml - Convert Markdown to XML

Converts Markdown text to XML format.

```bash
python scripts/md_to_xml.py <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path or Markdown text
- `output` - Output XML file path

**Options:**
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
python scripts/md_to_xml.py ./abc.md ./output.xml
```


### md_to_latex - Convert Markdown Tables to LaTeX

Converts Markdown tables to LaTeX format.

```bash
python scripts/md_to_latex.py <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path or Markdown text
- `output` - Output LaTeX file path

**Options:**
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
python scripts/md_to_latex.py ./abc.md ./output.tex
```


### md_to_html - Convert Markdown to HTML

Converts Markdown text to HTML format using pandoc.

```bash
python scripts/md_to_html.py <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path or Markdown text
- `output` - Output HTML file path

**Options:**
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
python scripts/md_to_html.py ./abc.md ./output.html
```


### md_to_html_text - Convert Markdown to HTML Text

Converts Markdown text to HTML and outputs to stdout.

```bash
python scripts/md_to_html_text.py <input>
```

**Arguments:**
- `input` - Input Markdown file path or Markdown text

**Example:**
```bash
python scripts/md_to_html_text.py ./abc.md
```


### md_to_png - Convert Markdown to PNG Images

Converts Markdown text to PNG images (one per page).

```bash
python scripts/md_to_png.py <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path or Markdown text
- `output` - Output PNG file path or directory path

**Options:**
- `--compress` - Compress all PNG images into a ZIP file
- `--strip-wrapper` - Remove code block wrapper if present

**Example:**
```bash
python scripts/md_to_png.py ./abc.md ./output.png
python scripts/md_to_png.py ./abc.md ./output.png --compress
```


### md_to_md - Convert Markdown to MD File

Saves Markdown text to a .md file.

```bash
python scripts/md_to_md.py <input> <output>
```

**Arguments:**
- `input` - Input Markdown file path or Markdown text
- `output` - Output MD file path

**Example:**
```bash
python scripts/md_to_md.py ./abc.md ./output.md
```


### md_to_linked_image - Extract Image Links to Files

Extracts image links from Markdown and downloads them as files.

```bash
python scripts/md_to_linked_image.py <input> <output> [options]
```

**Arguments:**
- `input` - Input Markdown file path or Markdown text
- `output` - Output file or directory path

**Options:**
- `--compress` - Compress all images into a ZIP file

**Example:**
```bash
python scripts/md_to_linked_image.py ./abc.md ./output_dir
python scripts/md_to_linked_image.py ./abc.md ./output.zip --compress
```


## 📝 Notes

- All scripts support both file paths and direct Markdown text as input
- When providing direct Markdown text as input, the script will treat the first argument as the text content
- For scripts that generate multiple files (e.g., multiple tables, multiple code blocks), the output filename will be automatically numbered
- Use the `--strip-wrapper` option to remove code block wrappers (```) from the input Markdown
- For PPTX conversion, ensure the `md2pptx` directory is available in the `tools/md_to_pptx/` directory