import re
import os
import sys


def extract_device_name(template_file):
    # Use regex to match the pattern 'config_<device_name>.template.txt'
    file_name = template_file.split('/')[2]
    match = re.match(r'config_(.+)\.template\.txt', file_name)
    if match:
        return match.group(1)
    else:
        print(
            f"[ERROR] Could not extract device name from {file_name}. Ensure it follows the 'config_<device_name>.template.txt' pattern.")
        return None


def replace_variables(template_file, device_name, script_path):
    # Read the template file
    template_path_file = os.path.join(script_path, template_file)
    with open(template_path_file, 'r') as file:
        template_content = file.read()

    # Find all variables in the template file marked as $VARIABLE_NAME
    found_vars = re.findall(r'\$(\w+)', template_content)
    undefined_vars = []

    # Replace defined variables in the template and add quotes around the values
    for var_name in found_vars:
        # Get the environment variable
        var_value = os.getenv(var_name)

        if var_value is None:
            undefined_vars.append(var_name)
        else:
            # Replace the variable with its value wrapped in quotes
            template_content = re.sub(rf'\${var_name}', f'{var_value}', template_content)

    # Check for undefined variables
    if undefined_vars:
        print(
            f"[WARNING] Undefined environment variables in {template_file} for device {device_name.upper()}: {', '.join(undefined_vars)}")

    # Save the updated configuration back as the new configuration file
    base_dir = os.path.dirname(template_file)  # This will give the template directory
    parent_dir = os.path.dirname(base_dir)  # This will give the directory the template folder is in and other partial configs are in.
    complete_path = os.path.join(script_path, parent_dir)
    file_path = os.path.join(complete_path, f'config_{device_name}.partial.txt')
    with open(file_path, 'w') as file:
        file.write(template_content)

    print(f"[INFO] Processed and updated {template_file} for device {device_name.upper()}.")


def main(template_files):
    script_path = os.path.dirname(os.path.abspath(__file__))
    for template_file in template_files:
        # Extract device name from the template file name
        device_name = extract_device_name(template_file)

        if device_name:  # Proceed only if device name is correctly extracted
            replace_variables(template_file, device_name, script_path)


if __name__ == "__main__":
    # Pass configuration files as command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python3 substitute_variables.py frinx_topo_1/device_templates/config_r1_pe1.template.txt frinx_topo_1/device_templates/config_r1_pe2.template.txt ...")
    else:
        main(sys.argv[1:])
