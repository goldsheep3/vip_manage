import yaml


def read_yaml(language_file):
    try:
        with open(language_file, 'r', encoding='utf-8') as file:
            data = yaml.load(file, Loader=yaml.FullLoader)
            return data
    except FileNotFoundError:
        print(f"File not found: {language_file}")
        return None
    except yaml.YAMLError as e:
        print(f"Error reading YAML file {language_file}: {e}")
        return None
