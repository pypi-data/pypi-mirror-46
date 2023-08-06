#!/usr/bin/env python3

import pyglet
import glooey

def main():
    window = pyglet.window.Window(visible=False)
    window.set_size(500, 500)

    # Initialize window
    gui = glooey.Gui(window)
    placeholder = glooey.Placeholder()
    gui.add(placeholder)

    placeholder.set_size_hint(490, 490)

    window.set_visible()
    pyglet.app.run()


if __name__ == '__main__':
    main()
