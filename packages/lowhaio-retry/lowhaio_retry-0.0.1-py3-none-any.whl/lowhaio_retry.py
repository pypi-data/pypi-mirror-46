import asyncio


def retry(request, exception_intervals=()):

    async def _retry(*args, **kwargs):
        exception_iterators = dict(
            (klass, iter(intervals))
            for klass, intervals in exception_intervals
        )
        exceptions = tuple(exception_iterators.keys())

        while True:
            try:
                return await request(*args, **kwargs)
            except exceptions as exception:
                iterator = None
                for klass, iterator in exception_iterators.items():
                    if isinstance(exception, klass):
                        break
                try:
                    interval = next(iterator)
                except StopIteration:
                    raise exception from exception.__cause__

            await asyncio.sleep(interval)

    return _retry
