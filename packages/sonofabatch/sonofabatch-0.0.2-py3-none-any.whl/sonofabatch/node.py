import asyncio
from sonofabatch import babel
from sonofabatch.job import Job, JobStatus


class SonOfABatchNode:
    def __init__(self, on_job_func, hostname='127.0.0.1', port=8888):
        self.hostname = hostname
        self.on_job_func = on_job_func
        self.port = port

    def start(self):
        async def _run():
            while True:
                try:
                    reader, writer = await asyncio.open_connection(self.hostname, self.port)

                    async def _log(message=None):
                        job_status = JobStatus(False, message)
                        print (job_status)
                        await job_status.to_writer(writer)

                    node_name = await babel.read_string_from_reader(reader)
                    print('Connected. Assigned node name ' + str(node_name))

                    while True:
                        job = await Job.decode(reader)
                        await self.on_job_func(job, _log)

                        job_status = JobStatus(True, None)
                        await job_status.to_writer(writer)
                except Exception as e:
                    print (e)
                    print ("Exception occurred! Attempt to reconnect in 5...")
                    await asyncio.sleep(5)

        asyncio.run(_run())
