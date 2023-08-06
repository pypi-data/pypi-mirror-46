from dator import Dator


def main():
    dator = Dator('/usr/src/app/config.yml')
    df = dator.extract()
    df = dator.transform(df)
    dator.load(df)


if __name__ == '__main__':
    main()
