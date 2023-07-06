from modules.colors import color as c
from time import sleep
from threading import Thread
import time


class Loader:

    def __init__(self, message, finished_message='', color='&a'):
        self.running: bool = False
        self.characters: str = "|/–\\"
        self.message: str = message
        self.finished_message: str = finished_message
        self.thread: Thread = None
        self.killed = None
        self.char: str = None
        self.log = True
        self.custom_color = color
        self.new_line = False
        self.start_time = None
        self.suspended = False
        self.first_suspend = True
        self.suspended_validate = False

    def print(self, message, new_line=False, color='&a'):
        final_message = c(f"&7[ {color}> &7] &7{message}", False)
        final_message = '\n' + final_message if new_line else final_message
        print("\033[F\033[K" + final_message + "\n")
        print("\033[F\033[K" + c(f"&7[ &a{self.char} &7] " + self.message))
        return self

    def loading(self):
        try:
            print("\033[F\033[K\n")

            char_index = 0

            sleep(0.1)
            while self.running:
                self.char = self.characters[char_index]
                if self.suspended and self.first_suspend:
                    print("\033[F\033[F" + (" " * 100))
                    self.first_suspend = False
                    self.suspended_validate = True
                if not self.suspended:
                    print("\033[F\033[K" + c(f"&7[ {self.custom_color}{self.char} &7] " + self.message))
                char_index += 1
                if char_index == len(self.characters):
                    char_index = 0
                sleep(0.2)

            run_time = round(time.time() - self.start_time, 2)

            if self.log:
                if self.new_line:
                    print('\n')
                message = "\033[F\033[K" + c(
                    f"&7[ {self.custom_color}> &7] {self.custom_color}" + self.finished_message) + "\n"
                message = self.message.replace('%time%', str(run_time))
                print(self.message)
            else:
                print("\033[F\033[K")
            self.killed = True
        except KeyboardInterrupt as e:
            print("\033[F\033[K")
            self.killed = True
            exit()

    def infos(self, message):
        self.message = message
        return self

    def suspend(self, message=False, color='&9'):

        if message:
            print('\033[F' + 100 * ' ')
            print('\033[F' + c(f"&7[ {color}> &7] {color}{message}"))

        self.suspended_validate = False
        self.first_suspend = True
        self.suspended = True
        while not self.suspended_validate:
            sleep(0.1)
        return self

    def resume(self):
        self.suspended = False
        sleep(0.1)

    def start(self, new_line=False):
        if new_line != False:
            print('')
        self.start_time = time.time()
        self.running = True
        self.killed = False
        # self.thread: Thread = Thread(target=self.loading, args=(self.message,))
        self.thread: Thread = Thread(target=self.loading, daemon=True)
        self.thread.start()
        return self

    def stop(self, log=True, custom_message=False, custom_color=False, new_line=False):
        self.log = log
        if new_line != False:
            self.new_line = True
        if custom_message != False:
            self.finished_message = custom_message
        if custom_color != False:
            self.custom_color = custom_color
        self.running = False
        while not self.killed:
            sleep(0.1)
        self.thread = None
