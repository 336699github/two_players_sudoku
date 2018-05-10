import pygame

GREEN=(0,153,0)
WHITE=(255,255,255)
BLACK=(0,0,0)

class Button:
    def __init__(self,screen):
        self._screen=screen
        self._text="GO!"
        self._font=pygame.font.Font("freesansbold.ttf",20)

        pygame.draw.rect(self._screen, GREEN,(30,20,100,40))
        self._collide=pygame.Surface((100,40))
        #elf.collide=self._collide.convert()
        self._collide.fill(GREEN)
        self._collideRect = self._collide.get_rect()
        self._collideRect = self._collideRect.move(30,20)

        self._textSurf=self._font.render(self._text,True,WHITE)
        self._textRect=self._textSurf.get_rect()
        self._textRect.center=((30+(100/2)),(20+(40/2)))
        self._screen.blit(self._textSurf,self._textRect)

    def check_collide(self,mousepos):
        if len(mousepos) == 2:
            return self._collideRect.collidepoint(mousepos)
        elif len(mousepos) == 4:
            return self._collideRect.colliderect(mousepos)
        else:
            return False
    
    def draw(self):
        pygame.draw.rect(self._screen, GREEN,(30,20,100,40))
        self._screen.blit(self._textSurf,self._textRect)
        pygame.display.flip()

    def add_action_listener(self,controller):
        self._controller=controller


    def go_button_clicked(self):
        
        self._controller.go_button_clicked()