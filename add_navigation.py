import os
import re

PROJECT_FOLDER = "."

folders = {
    "html": "HTML",
    "css": "CSS",
    "javascript": "JavaScript"
}

def add_navigation(file_path, folder):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    home_link = '<a href="../index.html">Home</a>'
    programs_link = '<a href="index.html">Back to Programs</a>'

    # Do not add navigation if it already exists
    if home_link in content and programs_link in content:
        return False

    navigation = f"""
<nav>
    <a href="../index.html">Home</a>
    <a href="index.html">Back to Programs</a>
</nav>
"""

    # Add navigation immediately after <body>
    body_match = re.search(r"<body[^>]*>", content, re.IGNORECASE)

    if body_match:
        position = body_match.end()
        content = (
            content[:position]
            + navigation
            + content[position:]
        )
    else:
        print(f"Skipped: {file_path} - <body> tag not found")
        return False

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return True


total_files = 0
updated_files = 0
skipped_files = 0

for folder, section_name in folders.items():

    folder_path = os.path.join(PROJECT_FOLDER, folder)

    if not os.path.exists(folder_path):
        print(f"Folder not found: {folder_path}")
        continue

    for filename in os.listdir(folder_path):

        # Only process the numbered program files
        if folder == "html" and not re.fullmatch(r"html\d+\.html", filename):
            continue

        if folder == "css" and not re.fullmatch(r"css\d+\.html", filename):
            continue

        if folder == "javascript" and not re.fullmatch(r"js\d+\.html", filename):
            continue

        file_path = os.path.join(folder_path, filename)

        total_files += 1

        try:
            if add_navigation(file_path, folder):
                updated_files += 1
                print(f"Updated: {folder}/{filename}")
            else:
                skipped_files += 1

        except Exception as e:
            print(f"Error in {file_path}: {e}")


print("\n==============================")
print("NAVIGATION UPDATE COMPLETE")
print("==============================")
print(f"Program files found : {total_files}")
print(f"Files updated       : {updated_files}")
print(f"Files already done  : {skipped_files}")
print("==============================")