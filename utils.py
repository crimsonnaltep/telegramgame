from yaml import load, Loader


def get_config():
    with open('config.yaml') as f:
        config = load(f, Loader=Loader)
    return config