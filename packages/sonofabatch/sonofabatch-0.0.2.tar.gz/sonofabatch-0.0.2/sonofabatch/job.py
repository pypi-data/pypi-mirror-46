from sonofabatch import babel


class JobStatus:
    def __init__(self, is_done, message=None):
        self.is_done = is_done
        self.message = message

    @staticmethod
    async def from_reader(reader):
        is_done = await babel.read_bool_from_reader(reader)
        if is_done:
            return JobStatus(True, None)

        message = None
        has_message = await babel.read_bool_from_reader(reader)
        if has_message:
            message = await babel.read_string_from_reader(reader)

        return JobStatus(False, message)

    async def to_writer(self, writer):
        if self.is_done:
            await babel.write_bool_to_writer(writer, True)
            return

        await babel.write_bool_to_writer(writer, False)  # Not done

        if self.message is None:
            await babel.write_bool_to_writer(writer, False)  # No message
            return

        await babel.write_bool_to_writer(writer, True)  # Has message
        await babel.write_string_to_writer(writer, self.message)

    def __str__(self):
        return 'done' if self.is_done else 'not done' + \
                                             str('' if self.message is None else ('; ' + self.message))


class Job:
    def __init__(self, name, failure_count=0):
        self.name = name
        self.failure_count = failure_count

    async def encode(self, writer):
        await babel.write_string_to_writer(writer, self.name)
        await babel.write_int_to_writer(writer, self.failure_count)

    @staticmethod
    async def decode(reader):
        name = await babel.read_string_from_reader(reader)
        failure_count = await babel.read_int_from_reader(reader)
        return Job(name,failure_count)

    def increment_failure_count(self):
        self.failure_count += 1

    def __str__(self):
        return self.name + " (failures: " + str(self.failure_count) + ")"
