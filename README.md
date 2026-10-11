# PMD Java Rule Analysis (`pmd-java-rule-analysis`)

> Automated taxonomy extraction and data analysis for PMD (v7.28.0) Java static analysis rules.

---

## 📦 Repository Structure

- **`rulesets/`**: Official PMD v7.28.0 Java ruleset XML definitions (including `quickstart.xml`).
- **`parse_pmd_rules.py`**: Zero-dependency Python script to parse XML rulesets into a structured CSV dataset.
- **`pmd_java_rule_dataset.csv`**: Taxonomy dataset cataloging all 325 PMD Java rules.
- **`pmd_rule_dataset_analyzer.py`**: Zero-dependency Python script performing exploratory data analysis on the dataset.
- **`pmd_java_rule_analysis_report.md`**: Markdown summary report generated automatically by the analyzer script.

---

## 🛠️ Parser & Analyzer Overview

### **Taxonomy Parser (`parse_pmd_rules.py`)**
- **Dynamic XML Parsing**: Recursively extracts metadata directly from PMD XML ruleset definitions without hardcoded lookup dictionaries.
- **Custom Research IDs**: Assigns structured numeric research identifiers (`RULE-001` through `RULE-325`).
- **Profile Resolution**: Cross-references rules against `quickstart.xml` to flag default profile membership (`is_default_profile`).
- **Zero Dependencies**: Built entirely on standard Python 3 modules (`xml.etree`, `csv`, `glob`, `os`).

### **Dataset Analyzer (`pmd_rule_dataset_analyzer.py`)**
- **Statistical Summaries**: Computes rule distributions across PMD categories, severity priorities (1–5), and Quickstart default inclusion.
- **Cross-Tabulation**: Evaluates relationship between rule priority/category and default profile status.
- **Automated Reporting**: Prints formatted tables to console and exports `pmd_java_rule_analysis_report.md`.
- **Zero Dependencies**: Fully portable using Python standard library (`csv`, `collections`).

---

## 📊 Dataset Description (`pmd_java_rule_dataset.csv`)

The dataset catalogs **325 active PMD Java rules** across 6 schema fields:

| Field Name | Type | Description | Example |
| :--- | :--- | :--- | :--- |
| `rule_id` | String | Custom research numeric identifier | `RULE-001` |
| `rule_name` | String | Official PMD rule name | `AvoidSqlConcatenation` |
| `pmd_category` | String | High-level PMD category | `Security` |
| `pmd_rule_path` | String | Official PMD XML reference path | `category/java/security.xml/AvoidSqlConcatenation` |
| `priority` | Integer | PMD severity priority level (1 = Highest, 5 = Lowest) | `1` |
| `is_default_profile` | Boolean | Quickstart profile inclusion flag (`True`/`False`) | `True` |

---

## 🚀 Steps to Run

### **1. Extract the Taxonomy Dataset**
Ensure `rulesets/` (containing PMD XMLs and `quickstart.xml`) is in your working directory, then run:

```bash
python3 parse_pmd_rules.py
```
*Output*: Generates `pmd_java_rule_dataset.csv` (325 rules).

### **2. Run Dataset Analysis**
To generate summary statistics and the markdown report:

```bash
python3 pmd_rule_dataset_analyzer.py
```
*Output*: Displays terminal analysis and exports `pmd_java_rule_analysis_report.md`.

---

## 📈 Dataset Analysis Results (N=325)

### **1. Category Distribution**
- **Error Prone**: 100 rules (30.77%)
- **Best Practices**: 71 rules (21.85%)
- **Code Style**: 64 rules (19.69%)
- **Design**: 45 rules (13.85%)
- **Performance**: 25 rules (7.69%)
- **Multithreading**: 12 rules (3.69%)
- **Documentation**: 6 rules (1.85%)
- **Security**: 2 rules (0.62%)

### **2. Priority Level Distribution**
- **Priority 1 (Highest)**: 19 rules (5.85%)
- **Priority 2**: 19 rules (5.85%)
- **Priority 3 (Default/Medium)**: 265 rules (81.54%)
- **Priority 4**: 21 rules (6.46%)
- **Priority 5 (Lowest)**: 1 rule (0.31%)

### **3. Default Profile (Quickstart) Distribution**
- **Non-Default (`False`)**: 203 rules (62.46%)
- **Default Profile (`True`)**: 122 rules (37.54%)

### **4. Priority vs. Default Profile Cross-Tabulation**
| Priority Level | Non-Default (`False`) | Default (`True`) | Total |
| :---: | :---: | :---: | :---: |
| **1 (Highest)** | 9 | 10 | 19 |
| **2** | 9 | 10 | 19 |
| **3** | 171 | 94 | 265 |
| **4** | 13 | 8 | 21 |
| **5 (Lowest)** | 1 | 0 | 1 |
| **Total** | **203** | **122** | **325** |

### **5. Category vs. Default Profile Cross-Tabulation**
| PMD Category | Non-Default (`False`) | Default (`True`) | Total |
| :--- | :---: | :---: | :---: |
| **Best Practices** | 47 | 24 | 71 |
| **Code Style** | 39 | 25 | 64 |
| **Design** | 33 | 12 | 45 |
| **Documentation** | 3 | 3 | 6 |
| **Error Prone** | 51 | 49 | 100 |
| **Multithreading** | 5 | 7 | 12 |
| **Performance** | 23 | 2 | 25 |
| **Security** | 2 | 0 | 2 |
| **Total** | **203** | **122** | **325** |

### **6. Priority Statistics by Category**
- **Best Practices**: 71 rules (Mean Priority: 2.97 | Range: 2–4)
- **Code Style**: 64 rules (Mean Priority: 2.95 | Range: 1–4)
- **Design**: 45 rules (Mean Priority: 2.78 | Range: 1–3)
- **Documentation**: 6 rules (Mean Priority: 3.00 | Range: 3–3)
- **Error Prone**: 100 rules (Mean Priority: 2.86 | Range: 1–5)
- **Multithreading**: 12 rules (Mean Priority: 2.83 | Range: 1–4)
- **Performance**: 25 rules (Mean Priority: 2.88 | Range: 1–3)
- **Security**: 2 rules (Mean Priority: 3.00 | Range: 3–3)
