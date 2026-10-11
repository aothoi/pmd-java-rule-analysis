import os
import pandas as pd


def analyze_pmd_rule_dataset(csv_filepath):
    """
    Performs exploratory data analysis on pmd_java_rule_dataset.csv.
    Generates summary tables for categories, priorities, and default profile distribution.
    """
    if not os.path.exists(csv_filepath):
        print(f"Error: Target dataset file '{csv_filepath}' not found.")
        return None

    df = pd.read_csv(csv_filepath)
    total_rules = len(df)

    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append(f"       PMD JAVA RULE DATASET ANALYSIS SUMMARY (N={total_rules})")
    report_lines.append("=" * 60)
    report_lines.append("")

    # 1. Category Distribution
    report_lines.append("[1] CATEGORY DISTRIBUTION:")
    cat_dist = df['pmd_category'].value_counts().to_frame(name='Count')
    cat_dist['Percentage (%)'] = (cat_dist['Count'] / total_rules * 100).round(2)
    report_lines.append(cat_dist.to_string())
    report_lines.append("")

    # 2. Priority Level Breakdown
    report_lines.append("[2] PRIORITY LEVEL DISTRIBUTION:")
    prio_dist = df['priority'].value_counts().sort_index().to_frame(name='Count')
    prio_dist['Percentage (%)'] = (prio_dist['Count'] / total_rules * 100).round(2)
    report_lines.append(prio_dist.to_string())
    report_lines.append("")

    # 3. Default Profile (Quickstart) Ratio
    report_lines.append("[3] DEFAULT PROFILE (QUICKSTART) DISTRIBUTION:")
    def_dist = df['is_default_profile'].value_counts().to_frame(name='Count')
    def_dist['Percentage (%)'] = (def_dist['Count'] / total_rules * 100).round(2)
    report_lines.append(def_dist.to_string())
    report_lines.append("")

    # 4. Priority vs. Default Profile Cross-Tabulation
    report_lines.append("[4] PRIORITY VS. DEFAULT PROFILE CROSS-TABULATION:")
    prio_def_ct = pd.crosstab(df['priority'], df['is_default_profile'], margins=True, margins_name='Total')
    report_lines.append(prio_def_ct.to_string())
    report_lines.append("")

    # 5. Category vs. Default Profile Cross-Tabulation
    report_lines.append("[5] CATEGORY VS. DEFAULT PROFILE CROSS-TABULATION:")
    cat_def_ct = pd.crosstab(df['pmd_category'], df['is_default_profile'], margins=True, margins_name='Total')
    report_lines.append(cat_def_ct.to_string())
    report_lines.append("")

    # 6. Priority Statistics by Category
    report_lines.append("[6] PRIORITY STATS BY CATEGORY:")
    prio_stats = df.groupby('pmd_category')['priority'].agg(
        Rule_Count='count',
        Mean_Priority='mean',
        Min_Priority='min',
        Max_Priority='max'
    ).round(2)
    report_lines.append(prio_stats.to_string())
    report_lines.append("")

    report_text = "\n".join(report_lines)
    print(report_text)

    # Save to Markdown report file
    output_dir = os.path.dirname(csv_filepath)
    report_filepath = os.path.join(output_dir, "pmd_java_rule_analysis_report.md")
    with open(report_filepath, "w", encoding="utf-8") as f:
        f.write("# PMD Java Rule Dataset Analysis Report\n\n```\n" + report_text + "\n```\n")

    print(f"\nSuccessfully generated analysis report at: '{report_filepath}'")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    target_csv = os.path.join(script_dir, "pmd_java_rule_dataset.csv")

    analyze_pmd_rule_dataset(target_csv)
