import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from PIL import Image

def Cubo():
    im = Image.open("cat.jpg")
    width, height, img_data = im.width, im.height, im.tobytes("raw", "RGBA", 0, -1)


    #Funções que habilitam as funcionalidades do OpenGL
    glEnable(GL_DEPTH_TEST) #Noção de profundidade
    glEnable(GL_TEXTURE_2D) #Executa a texturização bidimensional

    #cria nome para textura
    Texture = glGenTextures(1)
    
    #Criação de uma textura nomeada e associada ao destino dela
    glBindTexture(GL_TEXTURE_2D, Texture)

    #especifica uma imagem de textura bidimensional
    #parametros(destino, level*nivel de detelhe*, cor, largura, altura, largura da borda, formato dos dados, tipo, imagem)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    #Filtros de textura
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    #Inicio da criação do cubo com sua textura
    glBegin ( GL_QUADS )

    #face posterior
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)

    #face inferior
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, -1.0, -1.0)
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)

    #face direita
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)
    glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)

    #face esquerda
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0, -1.0)
    glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)

    #face superior
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0, -1.0)
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0,  1.0,  1.0)
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0,  1.0,  1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0, -1.0)

    #face frontal
    glTexCoord2f(0.0, 0.0); glVertex3f(-1.0, -1.0,  1.0)
    glTexCoord2f(1.0, 0.0); glVertex3f( 1.0, -1.0,  1.0)
    glTexCoord2f(1.0, 1.0); glVertex3f( 1.0,  1.0,  1.0)
    glTexCoord2f(0.0, 1.0); glVertex3f(-1.0,  1.0,  1.0)

    glEnd()

# variáveis de controle de estado
rotating = False      # controle de rotação
translating = False   # controle de translação
scaling_x = False  # controle de escalonamento no eixo X
scaling_y = False  # controle de escalonamento no eixo Y
scaling_z = False  # controle de escalonamento no eixo Z
trans_x = 0           # translação no eixo X
trans_y = 0           # translação no eixo Y
trans_z = -5          # translação no eixo Z (inicialmente para afastar o cubo da câmera)
scale_x = 1.0  # fator de escalonamento no eixo X
scale_y = 1.0  # fator de escalonamento no eixo Y
scale_z = 1.0       # fator de escalonamento no eixo Z
rotation_angle_x = 0  # angulo de rotação em torno do eixo X
rotation_angle_y = 0  # angulo de rotação em torno do eixo Y
rotation_angle_z = 0  # angulo de rotação em torno do eixo Z

def main():
    global rotating, translating, scaling_x, scaling_y, scaling_z, trans_x, trans_y, trans_z, scale_x, scale_y, scale_z, rotation_angle_x, rotation_angle_y, rotation_angle_z
    pygame.init()
    display = (800, 600)
    pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    rotating = not rotating  # alterna o estado de rotação
                if event.key == pygame.K_t:
                    translating = not translating  # alterna o estado de translação
                if event.key == pygame.K_x:
                        scaling_x = not scaling_x  # alterna o estado de escalonamento no eixo X
                        if scaling_x:
                            scaling_y = False
                            scaling_z = False
                if event.key == pygame.K_y:
                    scaling_y = not scaling_y  # alterna o estado de escalonamento no eixo Y
                    if scaling_y:
                        scaling_x = False
                        scaling_z = False
                if event.key == pygame.K_z:
                    scaling_z = not scaling_z  # alterna o estado de escalonamento no eixo Z
                    if scaling_z:
                        scaling_x = False
                        scaling_y = False

        keys = pygame.key.get_pressed()
        
        if scaling_x:
            if keys[pygame.K_w]:
                scale_x += 0.1  # aumenta o escalonamento no eixo X
            if keys[pygame.K_s]:
                scale_x = max(0.1, scale_x - 0.1)  # diminui o escalonamento no eixo X sem permitir valores negativos

        if scaling_y:
            if keys[pygame.K_w]:
                scale_y += 0.1  # aumenta o escalonamento no eixo Y
            if keys[pygame.K_s]:
                scale_y = max(0.1, scale_y - 0.1)  # diminui o escalonamento no eixo Y sem permitir valores negativos

        if scaling_z:
            if keys[pygame.K_w]:
                scale_z += 0.1  # aumenta o escalonamento no eixo Z
            if keys[pygame.K_s]:
                scale_z = max(0.1, scale_z - 0.1)  # diminui o escalonamento no eixo Z sem permitir valores negativos

        if translating:
            if keys[pygame.K_UP]:
                trans_y += 0.1  # move o cubo para cima
            if keys[pygame.K_DOWN]:
                trans_y -= 0.1  # move o cubo para baixo
            if keys[pygame.K_LEFT]:
                trans_x -= 0.1  # move o cubo para a esquerda
            if keys[pygame.K_RIGHT]:
                trans_x += 0.1  # move o cubo para a direita
            if keys[pygame.K_KP_PLUS]:
                trans_z += 0.1  # move o cubo para frente
            if keys[pygame.K_KP_MINUS]:
                trans_z -= 0.1  # move o cubo para trás

        if rotating:
            rotation_angle_x += 1  # incrementa o ângulo de rotação em torno do eixo X
            rotation_angle_y += 1  # incrementa o ângulo de rotação em torno do eixo Y
            rotation_angle_z += 1  # incrementa o ângulo de rotação em torno do eixo Z
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        # define a perspectiva da câmera
        gluPerspective(45, (display[0] / display[1]), 0.1, 50.0)
        glTranslatef(trans_x, trans_y, trans_z)  # aplica a translação
        glScalef(scale_x, scale_y, scale_z)  # aplica o escalonamento
        glRotatef(rotation_angle_x, 1, 0, 0)  # aplica a rotação em torno do eixo X
        glRotatef(rotation_angle_y, 0, 1, 0)  # aplica a rotação em torno do eixo Y
        glRotatef(rotation_angle_z, 0, 0, 1)  # aplica a rotação em torno do eixo Z
        Cubo()
        pygame.display.flip()
        pygame.time.wait(10)

main()
