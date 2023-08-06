import asyncio
from sonofabatch import babel
from sonofabatch.job import Job, JobStatus


class SonOfABatchMaster:
    def __init__(self, hostname='0.0.0.0', queue_service_port=8888, populate_service_port=9999):
        self.hostname = hostname
        self.populate_service_port = populate_service_port
        self.queue_service_port = queue_service_port
        self.nodes = {}
        self.nodes_lock = asyncio.locks.Lock()
        self.job_queue = asyncio.Queue()

    async def _register_new_node(self, reader, writer):
        await self.nodes_lock.acquire()

        node_name = None
        while node_name is None or node_name in self.nodes:
            node_name = babel.generate_random_node_name()

        self.nodes[node_name] = (reader, writer)
        self.nodes_lock.release()

        return node_name

    async def handle_queue_connection(self, reader, writer):
        node_name = await self._register_new_node(reader, writer)
        # addr = writer.get_extra_info('peername')

        print(node_name)

        await babel.write_string_to_writer(writer, node_name)
        while True:
            job = await self.job_queue.get()
            try:
                await job.encode(writer)
                job_status = await JobStatus.from_reader(reader)
                while not job_status.is_done:
                    print (job_status)
                    job_status = await JobStatus.from_reader(reader)
            except:
                print ("Exception occurred waiting for job status. Killing connection and requeuing")
                job.increment_failure_count()
                await self.job_queue.put(job)
                break


    async def handle_populate_connection(self, reader, writer):
        while True:
            try:
                job = await Job.decode(reader)
                await self.job_queue.put(job)
                print ("Received job. Queue size: " + str(self.job_queue.qsize()))
            except:
                print ("Populate connection closed.")
                break

    async def start_queue_service(self):
        await asyncio.start_server(master.handle_queue_connection, host=self.hostname, port=self.queue_service_port)

    async def start_populate_service(self):
        await asyncio.start_server(master.handle_populate_connection, host=self.hostname, port=self.populate_service_port)

    async def start_debug_service(self):
        while True:
            print("Queue size: " + str(self.job_queue.qsize()))
            await asyncio.sleep(5)

    def attach_to_event_loop(self, loop):
        loop.run_until_complete(master.start_queue_service())
        loop.run_until_complete(master.start_populate_service())
        loop.run_until_complete(master.start_debug_service())



if __name__ == '__main__':
    master = SonOfABatchMaster(hostname='0.0.0.0', queue_service_port=8888, populate_service_port=9999)

    loop = asyncio.get_event_loop()
    master.attach_to_event_loop(loop)
    loop.run_forever()