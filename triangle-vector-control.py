import glfw
from OpenGL.GL import *
import numpy as np

vertices = np.array([
    [-0.5, -0.5],
    [0.5, -0.5],
    [0.0, 0.5]
], dtype=np.float32)

selected_vertex = -1
is_mouse_button_pressed = False


def draw_triangle():
    glBegin(GL_TRIANGLES)
    glColor3f(1.0, 0.0, 0.0)
    for vertex in vertices:
        glVertex2fv(vertex)
    glEnd()


def draw_points():
    glPointSize(10.0)
    glBegin(GL_POINTS)
    glColor3f(0.0, 0.0, 1.0)
    for vertex in vertices:
        glVertex2fv(vertex)
    glEnd()


def mouse_button_callback(window, button, action, mods):
    global selected_vertex, is_mouse_button_pressed
    if button == glfw.MOUSE_BUTTON_LEFT:
        if action == glfw.PRESS:
            xpos, ypos = glfw.get_cursor_pos(window)
            closest_vertex_index = find_closest_vertex(xpos, ypos)
            selected_vertex = closest_vertex_index
            is_mouse_button_pressed = True
        elif action == glfw.RELEASE:
            is_mouse_button_pressed = False


def cursor_position_callback(window, xpos, ypos):
    global selected_vertex
    if is_mouse_button_pressed and selected_vertex != -1:
        vertices[selected_vertex] = [(xpos / 400.0) - 1.0, -(ypos / 300.0) + 1.0]


def find_closest_vertex(xpos, ypos):
    closest_vertex_index = -1
    min_distance = float('inf')
    for i, vertex in enumerate(vertices):
        distance = np.sqrt((xpos - (vertex[0] * 400 + 400))**2 + (ypos - (-vertex[1] * 300 + 300))**2)
        if distance < min_distance:
            min_distance = distance
            closest_vertex_index = i
    return closest_vertex_index


def main():
    if not glfw.init():
        return -1

    window = glfw.create_window(800, 600, "Triangle Control", None, None)
    if not window:
        glfw.terminate()
        return -1

    glfw.make_context_current(window)

    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window, cursor_position_callback)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)

        draw_triangle()
        draw_points()

        glfw.swap_buffers(window)

        glfw.poll_events()

    glfw.terminate()


if __name__ == "__main__":
    main()
