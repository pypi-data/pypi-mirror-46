###A basic example of using PythonMusic to play the song Jingle Bells###

import PythonMusic

def example():
    PythonMusic.note('B5', 200, 2)
    PythonMusic.note('B5', 500, 1)

    PythonMusic.wait(100)

    PythonMusic.note('B5', 200, 2)
    PythonMusic.note('B5', 500, 1)

    PythonMusic.wait(300)

    PythonMusic.note('B5', 400, 1)
    PythonMusic.note('D6', 200, 1)
    PythonMusic.note('G5', 200, 1)
    PythonMusic.note('A5', 200, 1)
    PythonMusic.note('B5', 600, 1)

    PythonMusic.wait(600)

    PythonMusic.note('C6', 200, 4)
    PythonMusic.note('C6', 100, 1)
    PythonMusic.note('B5', 200, 3)
    PythonMusic.note('B5', 300, 1)

    PythonMusic.wait(50)

    PythonMusic.note('A5', 300, 1)
    PythonMusic.note('A5', 200, 1)
    PythonMusic.note('B5', 200, 1)
    PythonMusic.note('A5', 400, 1)

    PythonMusic.wait(50)

    PythonMusic.note('E5', 500, 1)
    PythonMusic.note('G5', 800, 1)

if __name__ == "__main__":
    example()
