
import numpy as np
import cv2

class DeteccionBosque():

    def obtener_img_capas(self):
        rojo = np.uint8(np.ones((480,640,3))*(0,0,255))
        azul = np.uint8(np.ones((480,640,3))*(255,0,0))
        return rojo, azul

    def obtener_variacion(self, img_actual, img_anterior):
        rojo, azul = self.obtener_img_capas()
        img_actual = self.normalizar_imagen(img_actual)
        img_anterior = self.normalizar_imagen(img_anterior)
        bin_act = self.pre_procesamiento(img_actual)
        bin_ant = self.pre_procesamiento(img_anterior)
        resultado = self.obtener_resultado(img_actual, bin_act, bin_ant, rojo, azul)
        #self.obtener_porcentaje_variacion(resultado)
        resultado = cv2.resize(resultado, (610, 430))
        cv2.imwrite("images/imgresultado.PNG", resultado)
        porcentaje_ganancia = self.calcularPorcentaje(bin_ant, bin_act)
        porcentaje_perdida = self.calcularPorcentaje(bin_act, bin_ant)
        return porcentaje_ganancia, porcentaje_perdida

    def normalizar_imagen(self, img):
        img = cv2.resize(img, (640, 480))
        r, g, b = cv2.split(img)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        cl_r = clahe.apply(r)
        cl_g = clahe.apply(g)
        cl_b = clahe.apply(b)
        return cv2.merge((cl_r, cl_g, cl_b))

    def obtener_resultado(self, img_actual, bin_act, bin_ant, rojo, azul):
        res = bin_act - bin_ant
        res1 = bin_ant - bin_act
        res = cv2.bitwise_not(bin_ant, rojo, mask=res)
        res = cv2.bitwise_and(rojo, rojo, mask=res)
        res1 = cv2.bitwise_and(azul, azul, mask=res1)
        juntar = cv2.add(res, res1)
        return cv2.add(img_actual, juntar)

    def pre_procesamiento(self, img):
        img = cv2.resize(img, (640, 480))
        r, g, b = cv2.split(img)
        _, img_binaria = cv2.threshold(b, 35, 255, cv2.THRESH_BINARY)
        img_binaria = cv2.dilate(img_binaria, (10, 10))
        return img_binaria

    def obtener_porcentaje_variacion(self, img_res):
        img_res = cv2.cvtColor(img_res, cv2.COLOR_BGR2HSV)
        mascara_rosa = cv2.inRange(img_res, (150,70,100), (220,270,300))
        contours, _ = cv2.findContours(mascara_rosa, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        areas = 0
        for c in contours:
            areas += cv2.contourArea(c)
        mascara_rosa = cv2.inRange(img_res, (50, 127, 0), (127, 255, 255))
        contours, _ = cv2.findContours(mascara_rosa, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        areas = 0
        for c in contours:
            areas += cv2.contourArea(c)

    def obtener_rango_colores(self, img, rango_inferior, rango_superior):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    def calcularPorcentaje(self, imagen1, imagen2):
        img1 = cv2.resize(imagen1, (64, 64))
        img2 = cv2.resize(imagen2, (64, 64))
        diferencia = img1 - img2
        px1 = self.contarPixeles(img1)
        px2 = self.contarPixeles(diferencia)
        porcentaje = px2 * 100 / px1
        return porcentaje

    def contarPixeles(self, imagen1):
        contador = 0
        red = cv2.resize(imagen1, (64, 64))
        matriz = np.array(red)
        altura, anchura = matriz.shape[:2]
        for i in range(0, altura - 1, 1):
            for j in range(0, anchura - 1, 1):
                v = matriz[i][j]
                if (v == 255):
                    contador = contador + 1
        # print contador
        return contador


'''
img1 = cv2.imread("/media/carlitos/16GB/hackathon/Images/img1.PNG")
img2 = cv2.imread("/media/carlitos/16GB/hackathon/Images/img2.PNG")
db = DeteccionBosque()
db.obtener_variacion(img1, img2)
'''
k = cv2.waitKey(0)
if k == 27:
    cv2.destroyAllWindows()
