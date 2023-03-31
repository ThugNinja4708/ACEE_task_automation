queue = []
def queueing(task):
    queue.append(task)
    api_call(task)

