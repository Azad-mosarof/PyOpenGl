import pygame as pg
import numpy as np
from OpenGL.GL import *
import ctypes
from OpenGL.GL.shaders import compileProgram, compileShader

vertext_file_path = "/home/azadm/Desktop/openGl/venv/pyOpenGl/shaders/vertext.txt"
fragment_file_path = "/home/azadm/Desktop/openGl/venv/pyOpenGl/shaders/fragment.txt"
image_path_1 = "/home/azadm/Desktop/openGl/venv/pyOpenGl/assests/wood.jpeg"
image_path_2 = "/home/azadm/Desktop/openGl/venv/pyOpenGl/assests/cat.png"

class App:

    def __init__(self):
        pg.init()
        pg.display.set_mode((600, 400), pg.OPENGL | pg.DOUBLEBUF)
        self.clock = pg.time.Clock()
        glClearColor(0.1, 0.2, 0.2, 3)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        self.shader = self.createShader(vertext_file_path, fragment_file_path)
        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)
        self.triangle = Triangle()
        self.wood_texture = Material(image_path_1)
        self.mainLoop()

    def createShader(self, vertexFilePath, fragmentFilePath):
        with open(vertexFilePath, 'r') as f:
            vertex_src = f.readlines()

        with open(fragmentFilePath, 'r') as f:
            fragment_src = f.readlines()

        shader = compileProgram(
            compileShader(vertex_src, GL_VERTEX_SHADER),
            compileShader(fragment_src, GL_FRAGMENT_SHADER)
        )

        return shader

    def mainLoop(self):
        running = True
        while(running):
            #check events
            for event in pg.event.get():
                if(event.type == pg.QUIT):
                    running = False
            #refresh screen
            glClear(GL_COLOR_BUFFER_BIT)  

            glUseProgram(self.shader)
            self.wood_texture.use()
            glBindVertexArray(self.triangle.vao)
            glDrawArrays(GL_TRIANGLES, 0, self.triangle.vertex_count)

            """glDrawArrays functions take the argument draw mode, starting position
            and number of points"""

            pg.display.flip()

            #timing
            self.clock.tick(60)
        self.quit()

    def quit(self):
        self.triangle.destroy()
        self.wood_texture.destroy()
        glDeleteProgram(self.shader)
        pg.quit()

class Triangle:

    def __init__(self):
        #x, y, z, r, g, b, s, t
        self.vertices = (
            -0.5, -0.5, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0,
            0.5, -0.5, 0.0, 0.0, 1.0, 0.0, 1.0, 1.0,
            0.0, 0.5, 0.0, 0.0, 0.0, 1.0, 0.5, 0.0
        )

        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.vertex_count = 3

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        """
        vertex array object is the best way to represent the
        vertex data.
        """

        self.vbo = glGenBuffers(1)  #it will create one open opengl buffer object. buffer is the basic storage container
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo) #bind that buffer 
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        """
        glBufferData used to shift the buffer data to
        the graphics card. We tell openGl where we want to store 
        the data, how many bytes we are sending through, then the data
        and then we are telling the opengl how to use the data
        """

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(12))
        glEnableVertexAttribArray(2)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, 32, ctypes.c_void_p(24))

        """
        Here we first enabled the attributes. Attributes 0 is for the 
        position x, y, z and the attribute 1 is for the rgb color channels.
        each attribute have total 3 points and data types is float. GL_FALSE
        means it openGL does not need any extra work to normalize the data.
        next argument is the stride that how many steps it need to jump to go 
        to the next vertices. each verices have 6 number, so 6*4 = 24. Next
        argument is the offset that where the is the starting point of the data.
        the starting position of for the first vertex is 0 and the starting
        position for the first color point is 3*4 = 12(after the 3 vertex).

        Here we actually allocate some memory in the graphics card.So after
        compleating the task we should clear the memory.
        """

    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))

    """In order to draw anything first we need to make shaders.We need
    Two shaders, one is vertex shader and another one is fragment shader.
    The vertex shader runs for per vertex, responsible to set the position
    and make transformation.Then the shape is assembled and break down
    into fragments or pixels.The fragment shader run ones per pixels
    and it is responsible for calculating the color that pixel should
    take."""

class CubeMesh:

    def __init__(self):
        #x, y, z, r, g, b, s, t
        self.vertices = (
            -0.5, -0.5, 0.0, 0.0, 1.0,
            0.5, -0.5, 0.0, 1.0, 1.0,
            0.0, 0.5, 0.0, 0.5, 0.0
        )

        self.vertices = np.array(self.vertices, dtype=np.float32)
        self.vertex_count = 3

        self.vao = glGenVertexArrays(1)
        glBindVertexArray(self.vao)

        self.vbo = glGenBuffers(1)  #it will create one open opengl buffer object. buffer is the basic storage container
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo) #bind that buffer 
        glBufferData(GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices, GL_STATIC_DRAW)

        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(0))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 20, ctypes.c_void_p(12))


    def destroy(self):
        glDeleteVertexArrays(1, (self.vao,))
        glDeleteBuffers(1, (self.vbo,))



class Cube:

    def __init__(self, position, eulers):
        self.position = np.array(position)
        self.eulers = np.array(eulers)

class Material:

    def __init__(self, filePath):

        self.texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        """Texture co-ordinate in opengl are address in S, T co-ordinate pair
        S=0 means left side of the texture, s=1 means right side of the texture,
        T=0 means top of the texture and T=1 means bottom of the texture"""

        """The first line, glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST), sets the texture filtering mode 
        when the texture is scaled down. The GL_TEXTURE_MIN_FILTER parameter specifies that we want to set the filtering mode 
        for when the texture is minified, i.e. when it is displayed at a smaller size than its original resolution. The GL_NEAREST 
        parameter specifies the filtering mode, which in this case is nearest-neighbor filtering. Nearest-neighbor filtering 
        selects the texel (texture pixel) closest to the pixel being rendered, resulting in a blocky appearance but with less blur.

        The second line, glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR), sets the texture filtering mode when the 
        texture is scaled up. The GL_TEXTURE_MAG_FILTER parameter specifies that we want to set the filtering mode for when the 
        texture is magnified, i.e. when it is displayed at a larger size than its original resolution. The GL_LINEAR parameter 
        specifies the filtering mode, which in this case is linear filtering. Linear filtering takes the average of surrounding 
        texels to produce a smooth appearance, which is better suited for larger texture scales."""

        image = pg.image.load(filePath).convert_alpha()
        image_width, image_height = image.get_rect().size
        image_data = pg.image.tostring(image, "RGBA") #opengl does not understand the pygame image data.that's we convert the image data into string
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, image_width, image_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, image_data)
        glGenerateMipmap(GL_TEXTURE_2D)

    def use(self):
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.texture)

    def destroy(self):
        glDeleteTextures(1, (self.texture,))



if __name__ == "__main__":
    myApp = App()
        
