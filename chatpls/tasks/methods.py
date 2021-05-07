import logging
import multiprocessing
import threading

threads = []
processes = []


def add_process(name, function, *args):
    process = multiprocessing.Process(target=function, args=args)
    processes.append(process)
    process.start()
    return process


def add_thread(name, function, *args):
    thread = threading.Thread(target=function, args=args, daemon=True)
    threads.append(thread)
    thread.start()
    return thread


class process_function:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args):
        return add_process("Unnamed", self.function, *args)


class thread_function:
    def __init__(self, function):
        self.function = function

    def __call__(self, *args):
        return add_thread("Unnamed", self.function, *args)
