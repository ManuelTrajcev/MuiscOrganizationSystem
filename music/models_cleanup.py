# Open the file with UTF-16 encoding, which handles the BOM and null bytes.
with open("models.py", "r", encoding="utf-16") as f:
    content = f.read()

# Now write it back to the file as UTF-8, which should not have null bytes.
with open("models.py", "w", encoding="utf-8") as f:
    f.write(content)

print("File has been re-encoded to UTF-8.")
