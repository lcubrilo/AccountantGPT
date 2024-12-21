import os
import json
from pathlib import Path

def generate_project_structure(root_dir):
    structure = {}

    for root, dirs, files in os.walk(root_dir):
        current_dir = structure
        if current_dir == '.\\.venv': continue
        path = Path(root).relative_to(root_dir)
        for part in path.parts:
            current_dir = current_dir.setdefault(part, {})
        current_dir["__files__"] = files

    return structure

if __name__ == "__main__":
    root_directory = "."  # Current directory, change this if needed
    output_file = "project_structure.json"

    structure = generate_project_structure(root_directory)
    
    with open(output_file, "w") as f:
        json.dump(structure, f, indent=2)

    print(f"Project structure has been written to {output_file}")
