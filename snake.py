import itertools, time, random
from curtsies import FullscreenWindow, Input, FSArray
from curtsies.fmtfuncs import red, bold, green, on_blue, yellow, on_red, blue

MAX_FPS = 10
time_per_frame = 1. / MAX_FPS

class FrameCounter(object):
    def __init__(self):
        self.render_times = []
        self.dt = .5
    def frame(self):
        self.render_times.append(time.time())
    def fps(self):
        now = time.time()
        while self.render_times and self.render_times[0] < now - self.dt:
            self.render_times.pop(0)
        return len(self.render_times) / max(self.dt, now - self.render_times[0] if self.render_times else self.dt)

class SnakeGame(object):
    def __init__(self, width, height):
        self.snake_segments = [(10, 10), (10, 11), (10, 12)]
        self.width = width
        self.height = height
        self.direction = (1, 0)
    def render(self, isDead):
        if not isDead:
            a = FSArray(self.height, self.width)
            for seg in self.snake_segments:
                a[seg[0],seg[1]] = blue('X')
            return a
        else:
            a = self.deathSequence()
            return a

    def move(self):
        self.snake_segments.insert(0, (self.snake_segments[0][0] + self.direction[0],
                                      (self.snake_segments[0][1] + self.direction[1])))
    def deathSequence(self):
        a = FSArray(self.height, self.width)
        a[10,10] = red('X')
        a[10,14] = red('X')
        a[12, 10] = red('_')
        a[12, 11] = red('_')
        a[12, 12] = red('_')
        a[12, 13] = red('_')
        a[12, 14] = red('_')
        return a

def main():
    counter = FrameCounter()
    with FullscreenWindow() as window:
        print('Press escape to exit')
        game = SnakeGame(window.height, window.width)
        with Input() as input_generator:
            c = None
            for framenum in itertools.count(0):
                t0 = time.time()
                while True:
                    t = time.time()
                    temp_c = input_generator.send(max(0, t - (t0 + time_per_frame)))
                    if temp_c is not None:
                        c = temp_c
                    if c is None:
                        pass
                    elif c == '<ESC>':
                        return

                    c = None
                    if time_per_frame < t - t0:
                        break

                fps = 'FPS: %.1f' % counter.fps()
                a = game.render(isDead = False) # insert death boolean
                a[0:1, 0:len(fps)] = [fps]

                game.move()
                window.render_to_terminal(a)
                counter.frame()

if __name__ == '__main__':
    main()
