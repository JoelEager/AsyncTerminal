import asyncio

import AsyncTerminal as terminal

async def main():
    count = 1

    while True:
        print("I is doing things: " + str(count), end="")
        count += 1

        if terminal.isInputWaiting():
            inputedChars = terminal.readBuffer()

            if "q" in inputedChars:
                print("")
                return

            print(" and I got some input: " + inputedChars)
        else:
            print("")

        await asyncio.sleep(1)

try:
    asyncio.get_event_loop().run_until_complete(main())
except KeyboardInterrupt:
    # Exit cleanly on ctrl-c
    pass