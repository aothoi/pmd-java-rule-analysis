import csv
import glob
import os
import xml.etree.ElementTree as ET


def parse_pmd_rulesets_dynamically(pmd_rulesets_dir):
    """
    Dynamically parses official PMD Java ruleset XML files from scratch
    extracting strictly native PMD rule metadata.

    Parameters:
        pmd_rulesets_dir (str): Path to directory containing PMD Java ruleset XML files.

    Returns:
        list: List of dictionaries containing cataloged PMD Java rules.
    """
    # 1. Dynamically resolve quickstart default profile rules from quickstart.xml
    default_profile_rules = set()
    quickstart_files = glob.glob(
        os.path.join(pmd_rulesets_dir, "**", "*quickstart*.xml"), recursive=True
    )

    for qs_file in quickstart_files:
        try:
            tree = ET.parse(qs_file)
            root = tree.getroot()
            for elem in root.iter():
                if "}" in elem.tag:
                    elem.tag = elem.tag.split("}", 1)[1]

            for rule_ref in root.findall(".//rule"):
                ref_attr = rule_ref.attrib.get("ref")
                if ref_attr:
                    default_profile_rules.add(ref_attr.strip())
        except Exception as e:
            print(f"Warning: Could not parse quickstart file {qs_file}: {e}")

    # 2. Discover all category XML files in the target directory
    xml_files = glob.glob(
        os.path.join(pmd_rulesets_dir, "**", "*.xml"), recursive=True
    )
    category_files = [
        f for f in xml_files if "quickstart" not in os.path.basename(f).lower()
    ]

    parsed_rules = []
    rule_counter = 1

    for xml_path in category_files:
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            for elem in root.iter():
                if "}" in elem.tag:
                    elem.tag = elem.tag.split("}", 1)[1]

            base_filename = os.path.splitext(os.path.basename(xml_path))[0]
            category_name = base_filename.capitalize()
            if base_filename == "errorprone":
                category_name = "Error Prone"
            elif base_filename == "bestpractices":
                category_name = "Best Practices"
            elif base_filename == "codestyle":
                category_name = "Code Style"

            rel_category_path = f"category/java/{os.path.basename(xml_path)}"

            for rule_node in root.findall(".//rule"):
                rule_name = rule_node.attrib.get("name")
                if not rule_name:
                    continue

                pmd_rule_path = f"{rel_category_path}/{rule_name}"

                # Extract Priority level dynamically
                priority_node = rule_node.find("priority")
                if priority_node is not None and priority_node.text:
                    try:
                        priority = int(priority_node.text.strip())
                    except ValueError:
                        priority = 3
                else:
                    priority = 3

                # Custom Numeric Research ID (e.g. RULE-001, RULE-002)
                custom_rule_id = f"RULE-{rule_counter:03d}"
                rule_counter += 1

                # Resolve default profile status dynamically
                is_default = (pmd_rule_path in default_profile_rules) or (
                    rule_name in default_profile_rules
                )

                parsed_rules.append({
                    "rule_id": custom_rule_id,
                    "rule_name": rule_name,
                    "pmd_category": category_name,
                    "pmd_rule_path": pmd_rule_path,
                    "priority": priority,
                    "is_default_profile": is_default,
                })

        except Exception as e:
            print(f"Error parsing {xml_path}: {e}")

    return parsed_rules


def save_to_csv(rules_list, output_filepath):
    """Saves the parsed rules dictionary list to CSV using standard library."""
    fieldnames = [
        "rule_id",
        "rule_name",
        "pmd_category",
        "pmd_rule_path",
        "priority",
        "is_default_profile",
    ]
    with open(output_filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rules_list)


if __name__ == "__main__":
    script_directory = os.path.dirname(os.path.abspath(__file__))
    rulesets_directory = script_directory
    output_filename = os.path.join(script_directory, "pmd_java_rule_dataset.csv")

    if os.path.exists(rulesets_directory):
        rules = parse_pmd_rulesets_dynamically(rulesets_directory)
        save_to_csv(rules, output_filename)
        print(
            f"Successfully generated '{output_filename}' with {len(rules)} PMD rules!"
        )
    else:
        print(f"Directory '{rulesets_directory}' not found.")
