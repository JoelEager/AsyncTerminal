import asyncio

import AsyncTerminal as terminal

async def main():
    count = 1

    while True:
        terminal.write("I is doing things: " + str(count))
        count += 1

        if terminal.isInputWaiting():
            inputedChars = terminal.readBuffer()

            terminal.writeln(" and I got some input: " + inputedChars)

            if "q" in inputedChars:
                return

        else:
            terminal.writeln("")

        await asyncio.sleep(1)

try:
    asyncio.get_event_loop().run_until_complete(main())
except KeyboardInterrupt:
    # Exit cleanly on ctrl-c
    pass