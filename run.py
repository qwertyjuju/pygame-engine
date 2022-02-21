from engine import Engine


def main():        
    g = Engine('settings.json', logging_active=1)
    g.run()


if __name__ == '__main__':
    main()
