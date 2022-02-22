from engine import Engine


def main():        
    g = Engine('settings.json', enable_logging=1)
    g.run()


if __name__ == '__main__':
    main()
