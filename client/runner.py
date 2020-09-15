import subprocess
import shlex
import threading


def print_output(process, identifier):
    while process.poll() is None:
        line = process.stdout.readline()
        if line != b'':
            print(f"[{identifier}]  {line.decode('ascii')}")

    line = process.stdout.read()
    if line != b'':
        print(f"atexit [{identifier}]  {line.decode('ascii')}")
    else:
        print(f"  exit [{identifier}]")


class Runner:

    def __init__(self, command, identifier):
        self.process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        self.printer = threading.Thread(target=print_output, args=(self.process, identifier))
        self.printer.start()

    def done(self) -> bool:
        p = self.process.poll()
        if p is None:
            return False
        else:
            return True

    def failed(self):
        return self.process.returncode != 0


if __name__ == "__main__":
    r = Runner("echo Hello World", 1)
    while not r.done():
        pass

    if r.failed():
        print("Error in runner")
    print("finished")
