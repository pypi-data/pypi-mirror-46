from sonofabatch.job import Job
import asyncio
import fileinput

async def run():
    reader, writer = await asyncio.open_connection('127.0.0.1', 9999)
    for line in fileinput.input():
        line = line.strip()
        job = Job(line)
        await job.encode(writer)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
