import cv2
import numpy as np


def calcularPorcentaje(imagen1, imagen2):
    img1 = cv2.resize(imagen1,(64,64))
    img2 = cv2.resize(imagen2,(64,64))
    diferencia = img1 - img2
    px1 = contarPixeles(img1)
    print px1
    px2 = contarPixeles(diferencia)
    print px2
    porcentaje = px2*100/px1
    return porcentaje

def contarPixeles(imagen1):
    contador = 0
    red = cv2.resize(imagen1,(64,64))
    matriz = np.array(red)
    altura, anchura = matriz.shape[:2]
    for i in range(0 , altura-1,1):
        for j in range(0, anchura-1, 1):
            v = matriz[i][j]
            if(v == 255):
                contador = contador + 1
    #print contador
    return contador

img1 = cv2.imread('/home/carlitos/evelin/Images/img1.PNG')
img2 = cv2.imread('/home/carlitos/evelin/Images/img2.PNG')
img1 = cv2.resize(img1, (640, 480))
img2 = cv2.resize(img2, (640, 480))
cv2.imshow("img1", img1)
cv2.imshow("img2", img2)
res = img1 - img2

# usar metodo de convolucion
r1, g1, b1 = cv2.split(img1)
r2, g2, b2 = cv2.split(img2)

_, binary1 = cv2.threshold(b1, 35, 255, cv2.THRESH_BINARY)         #actual
binary1 = cv2.dilate(binary1, (10,10))
cv2.imshow("binary 1", binary1)
_, binary2 = cv2.threshold(b2, 35,255, cv2.THRESH_BINARY)
binary2 = cv2.dilate(binary2, (10,10))

porcentajePerdida = calcularPorcentaje(binary1,binary2) #anterior , actual
porcentajeGanancia = calcularPorcentaje(binary2,binary1) # actual, anterior
print ("El Porcentaje de perdida es: " + str(porcentajePerdida)+"%")
print ("El porcentaje de ganancia es: " + str(porcentajeGanancia)+"%")

cv2.imshow("binary 2", binary2)
area_verde_actual = 0
area_incrementada = 0
area_disminuida = 0
for i in range(0, 480, 1):
    for j in range(0, 640, 1):
        # Disminucion de areas verdes // Resaltado con color rojo
        if binary2[i][j] == 0:
            area_verde_actual +=1
        if binary2[i][j] == 0 and binary1[i][j]==255:
            img1[i][j] = (0, 0, 255)
            area_disminuida += 1
        # Aumento de areas verdes // color azul
        elif binary2[i][j] == 255 and binary1[i][j] == 0:
            img1[i][j] = (255, 0, 0)
            area_incrementada += 1

cv2.imshow("res", img1)

k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()

