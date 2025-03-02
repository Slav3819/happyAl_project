import tg_bot

def print_hi(name):
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


if __name__ == '__main__':
    print_hi('Bot AI start')
    tg_bot.asyncio.run(tg_bot.main())

