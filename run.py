from engine import ENGINE


def main():
    ENGINE.set_logger()
    ENGINE.run('data|settings.json')

if __name__ == '__main__':
    main()
