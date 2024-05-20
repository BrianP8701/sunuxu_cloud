# # Step 1: Verify None of the Lines are the Same and Remove All ® Symbols
# def process_mls_file(input_file, output_file):
#     with open(input_file, 'r') as file:
#         lines = file.readlines()

#     # Remove duplicates and ® symbols
#     unique_lines = set()
#     processed_lines = []
#     for line in lines:
#         clean_line = line.replace('®', '').strip()
#         if clean_line and clean_line not in unique_lines:
#             unique_lines.add(clean_line)
#             processed_lines.append(clean_line)

#     with open(output_file, 'w') as file:
#         for line in processed_lines:
#             file.write(line + '\n')

# # Usage
# process_mls_file('mls.txt', 'processed_mls.txt')

import enum
import re

# Step 2: Convert to Dictionary and Create Enum
def convert_to_dict_and_enum(input_file):
    state_mls_dict = {}
    current_state = None

    with open(input_file, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue
            if line.isalpha():  # Assuming state names are alphabetic
                current_state = line
                state_mls_dict[current_state] = []
            else:
                state_mls_dict[current_state].append(line)

    def clean_enum_name(name):
        # Remove parentheses and their contents
        name = re.sub(r'\(.*?\)', '', name)
        # Replace / with _, & with AND, and delete '
        name = name.replace('/', '_').replace('&', 'AND').replace("'", '')
        # Replace spaces and other characters with underscores
        name = re.sub(r'\W+', '_', name)
        # Ensure no double underscores
        name = re.sub(r'_+', '_', name)
        # Remove leading and trailing underscores
        name = name.strip('_')
        return name.upper()

    # Create Enum
    mls_enum = enum.Enum('MLS', {clean_enum_name(mls): mls for state in state_mls_dict for mls in state_mls_dict[state]})

    return state_mls_dict, mls_enum

# Usage
state_mls_dict, MLS = convert_to_dict_and_enum('processed_mls.txt')

# Print the dictionary
# print(state_mls_dict)

# Print the enum definition
print("class MLS(enum.Enum):")
for mls in MLS:
    print(f"    {mls.name} = \"{mls.value}\"")