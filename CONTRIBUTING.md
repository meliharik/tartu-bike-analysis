# Contributing to Tartu Bike Analysis

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## 🎯 Project Overview

This is a comprehensive data analysis project for the Tartu Smart Bike system, covering:
- Data preprocessing and cleaning
- Exploratory data analysis
- Statistical testing
- Machine learning models
- Interactive visualizations
- Network analysis

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Git
- pip

### Setup Development Environment

```bash
# Clone the repository
git clone https://github.com/meliharik/tartu-bike-analysis.git
cd tartu-bike-analysis

# Install dependencies
pip3 install -r requirements.txt

# Run data preprocessing (required first)
python3 scripts/01_data_preprocessing.py

# Run complete analysis pipeline
python3 scripts/02_run_eda.py

# (Optional) Launch dashboard
streamlit run dashboard.py
```

## 📝 Code Style Guidelines

### Python Style
- Follow **PEP 8** style guide
- Use meaningful variable names
- Add docstrings to all functions
- Keep functions focused (single responsibility)

### Example Function Format

```python
def calculate_metric(data):
    """
    Brief description of what the function does.

    Args:
        data (pd.DataFrame): Description of parameter

    Returns:
        dict: Description of return value
    """
    # Implementation
    pass
```

### Module Organization

The project follows a modular architecture:

```
scripts/analysis/
├── module_name.py          # Focused on one analysis type
└── utils/
    ├── plotting.py          # Reusable plotting functions
    └── reporting.py         # Report generation
```

Each module should:
- Have a clear, single purpose
- Include comprehensive docstrings
- Use helper functions from `utils/`
- Return results in a consistent format

## 🔧 Making Changes

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 2. Make Your Changes

- Keep commits atomic (one logical change per commit)
- Write clear commit messages
- Test your changes thoroughly

### 3. Commit Message Format

```
type: brief description

Detailed explanation (if needed)

- Bullet points for changes
- Related issue numbers (#123)
```

**Types**: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

**Examples**:
```
feat: add DBSCAN clustering for spatial analysis

- Implement DBSCAN algorithm for GPS hotspot detection
- Create visualization for cluster results
- Update report with findings
```

```
fix: correct timezone handling in datetime conversion

Fixes #42
```

### 4. Test Your Changes

Before submitting:

```bash
# Run the complete pipeline
python3 scripts/02_run_eda.py

# Check for errors
# Verify output files are generated correctly
# Test dashboard (if applicable)
streamlit run dashboard.py
```

## 📊 Adding New Analysis

If you're adding a new analysis module:

1. **Create module in `scripts/analysis/`**
   ```python
   # scripts/analysis/new_analysis.py
   def run_new_analysis(routes, report):
       """
       Run new analysis.

       Args:
           routes (pd.DataFrame): Routes dataframe
           report (MarkdownReport): Report object

       Returns:
           dict: Analysis results
       """
       # Your analysis code
       pass
   ```

2. **Add to orchestrator (`02_run_eda.py`)**
   ```python
   from analysis.new_analysis import run_new_analysis

   # In main execution
   new_results = run_new_analysis(routes, report)
   all_results['new_analysis'] = new_results
   ```

3. **Create visualizations**
   - Use `plotting.save_figure()` helper
   - Save to appropriate subdirectory
   - Follow 300 DPI standard

4. **Update documentation**
   - Add to README.md
   - Update technical architecture section
   - Add to visualization list

## 🐛 Reporting Issues

### Bug Reports

Include:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Python version and OS
- Error messages/stack traces

### Feature Requests

Include:
- Clear description of the feature
- Use case/motivation
- Example of how it would work
- Any relevant research papers or methods

## 📚 Documentation

When adding features:
- Update README.md
- Add docstrings to all functions
- Include examples in code comments
- Update relevant sections in reports

## ✅ Pull Request Process

1. **Ensure all tests pass**
2. **Update documentation**
3. **Add clear PR description**:
   ```markdown
   ## What
   Brief description of changes

   ## Why
   Motivation for changes

   ## How
   Technical approach

   ## Testing
   How you tested the changes
   ```

4. **Link related issues** (`Fixes #123`)
5. **Wait for review**

## 🎨 Visualization Guidelines

- Use consistent color schemes (check `config.py`)
- Save at 300 DPI
- Include clear titles and labels
- Use appropriate chart types
- Follow existing style patterns

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## 📞 Questions?

- Open an issue for questions
- Tag with `question` label
- Check existing issues first

## 🙏 Thank You!

Your contributions make this project better. Whether it's:
- Fixing bugs
- Adding features
- Improving documentation
- Reporting issues

Every contribution is valuable!

---

**Happy Coding!** 🚀
