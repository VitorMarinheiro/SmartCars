import pygame


class Car(pygame.sprite.Sprite):

    def __init__(self, janela, *groups):
        super().__init__(*groups)

        self.janela = janela
        self.image = pygame.image.load("assets/_56.png")
        self.rect = self.image.get_rect()
        self.height = 50
        self.width = 22
        self.rect.x = 635 - self.width // 2
        self.rect.y = 340 - self.height // 2
        self.ticks = 0
        self.vel = 0
        self.pts = 0
        self.play = True
        self.angle = 0

    def update(self, *args):
        if self.play:
            self.pts += 1

    def anim(self):
        self.ticks = (self.ticks + 1) % 4  # Vai fazer isso 6x depois voltar para 0

    def rotate(self, angle):
        self.angle += angle

    def draw(self):
        print('x')
        if self.play:
            print('a')
            img_copy = pygame.transform.rotate(self.image, self.angle)
            self.janela.blit(img_copy, (
                self.rect.centerx - int(img_copy.get_width() / 2), self.rect.centery - int(img_copy.get_height() / 2)))
            self.anim()
        else:
            print('b')
            self.janela.blit(self.image, (self.rect.x, self.rect.y))