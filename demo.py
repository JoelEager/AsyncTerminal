import asyncio

import AsyncTerminal as terminal

async def main():
    terminal.writeln("Non-blocking input demo for AsyncTerminal:")
    terminal.writeln("\t(Press q to quit.)\n")

    count = 1

    while True:
        terminal.write("I is doing things: " + str(count))
        count += 1

        if terminal.isInputWaiting():
            terminal.writeln(", and got some input without being blocked: " + terminal.readInput())
        else:
            terminal.writeln("")

        await asyncio.sleep(1)

def quitHandler(charIn):
    terminal.endTasks()
    mainTask.cancel()

try:
    terminal.registerInputHandler(quitHandler, filterString="q")
    mainTask = asyncio.get_event_loop().create_task(main())
    asyncio.get_event_loop().run_until_complete(mainTask)
except (KeyboardInterrupt, asyncio.CancelledError):
    # Exit cleanly on ctrl-c or cancellation
    pass