def save_string_to_file(string, path):
    try:
        with open(path, 'w', encoding='utf-8') as file:
            file.write(string)
        print(f"String successfully saved to {path}")
    except Exception as e:
        print(f"An error occurred while saving the string: {e}")


def get_string_from_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as file:
            string = file.read()
        return string
    except Exception as e:
        print(f"An error occurred while reading the string: {e}")
        return None
