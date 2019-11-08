from pathlib import Path
import numpy as np
import dlib, cv2, os
from datetime import datetime
from sys import exit

#Processar Video
def processando_video(video, tempdest, skip, codec):
    vs = cv2.VideoCapture(video) #abrindo video
    (width, height) = int(vs.get(3)), int(vs.get(4)) #pegando largura e altura
    fps = int(vs.get(5)) #pegando numero de fps
    fourcc = cv2.VideoWriter_fourcc(*codec)#pegando codec
    new_video = cv2.VideoWriter(tempdest, fourcc, fps, (width, height), True) #criando novo arquivo de video com largura, altura e fps do original
    read = 0

    print('Processando video, isso pode demorar um pouco, aguarde por favor...')
    #Detectando os rostos na imagens
    while True:
        (sucess, frame) = vs.read()
        if not sucess:#se nao conseguiu ler
            break
        read += 1
        if read == 1 or read % skip == 0:#o numero de pulos antes de fazer outra deteccao
            faces = acha_face_Dlib(frame)
            faces2 = acha_face_OpenCV(frame)

        face_image = drawRectangles(frame, faces, faces2)
        new_video.write(face_image)

    vs.release()
    new_video.release()
    print('')
    input('Indentificacao de faces concluida! Aperte enter para exibir o resultado: ')

    showVideo(tempdest)

    if args["output"]:
        print('Salvando Video...')
        saveVideo(tempdest, args["output"])

    removeTemp()

#Processar Imagem
def processando_imagem(imagem, output):
    if not os.path.isfile(imagem):
        print('Nao foi possivel ler a Imagem "{}", por favor, tente novamente!'.format(path_image))
        exit()

    pathImage = cv2.imread(imagem)

    faces = acha_face_Dlib(pathImage)
    faces2 = acha_face_OpenCV(pathImage)

    face_image = drawRectangles(pathImage, faces, faces2)

    cv2.imshow('Resultado',face_image)
    cv2.waitKey(0)

    if output:
        saveImage(face_image, output, imagem)

#Desenhar os retangulos
def drawRectangles(imagem, faces, faces2):
    face_image = imagem.copy()
    for (_, face) in enumerate(faces):
        l_x = int(face.tl_corner().x)
        t_y = int(face.tl_corner().y)
        r_x = int(face.br_corner().x)
        b_y = int(face.br_corner().y)
        cv2.rectangle(face_image, (l_x, t_y), (r_x, b_y), (0, 0, 255), 2)

    for (x, y, w, h) in faces2:
        cv2.rectangle(face_image, (x, y), (x+w, y+h), (255, 0, 0), 2)

    return face_image

#exibir video
def showVideo(output):
    vs = cv2.VideoCapture(output)
    vs.set(1, 0)
    while True:
        (sucess, frame) = vs.read()

        if not sucess:#se nao conseguiu ler
            break
        cv2.imshow('Exibicao do Resultado',frame)
        if cv2.waitKey(30) & 0xFF == ord('q'):
            break

    cv2.destroyAllWindows()

#salvar video
def saveVideo(video, destino):
    pathVideo= args["path_video"]
    ext = pathImage.rfind('.') #posicao do ultimo ponto, que e a extencao do arquivo
    barra = pathImage.rfind('/') + 1 #posicao da ultima barra
    nomeVideo = pathVideo[barra:ext] #nome do video
    today = datetime.now()
    diahora = '{}{}{}_{}{}{}'.format(today.day, today.month, today.year, today.hour, today.minute,today.second)
    newLocal = os.path.sep.join([os.getcwd() + '/' + destino, "{}-{}.avi".format(nomeVideo,diahora)])
    try:
        os.rename(video, newLocal)
        print('Video foi salvo com sucesso! Local do arquivo: {}'.format(newLocal))
    except:
        print('Nao foi possivel salvar o video, tente novamente!')

#salvar imagem
def saveImage(image, destino, pathImage):
    ext = pathImage.rfind('.') #posicao do ultimo ponto, que e a extencao do arquivo
    barra = pathImage.rfind('/') + 1 #posicao da ultima barra
    if barra == -1:#caso nao ache barra, barra recebe a posicao 0
        barra = 0
    nameImage = pathImage[barra:ext] #pega so o nome da imagem

    today = datetime.now()
    diahora = '{}{}{}_{}{}{}'.format(today.day, today.month, today.year, today.hour, today.minute,today.second)
    #NAO TA FUNCIONANDO OS IFS A FRENTE
    if destino[0] == '.':#tirar . do comeco
        destino = destino[1:]
    if destino[0] == '/': #tirar / do comeco
        destino = destino[1:]
    local = os.path.sep.join([os.getcwd() + '/' + destino, "{}-{}.png".format(nameImage,diahora)])
    try:
        cv2.imwrite(local, image)
        print('A imagem foi salvo com sucesso! Local do arquivo: {}'.format(local))
    except:
        print('Nao foi possivel salvar a imagem, tente novamente!')

#remover pasta temporaria
def removeTemp():
    try:
        path ="./temp"
        dir = os.listdir(path)
        for file in dir:
            os.unlink('./temp/{}'.format(file))
        os.rmdir(path)
    except:
        print("Nao foi possivel remover a pasta temp!")

#rodar a imagem em 90graus n vezes (times, define o numero de vezes)
def rotate(image, times=1):
    return np.rot90(image, times)

#achar face com o Dlib
def acha_face_Dlib(frame, verbose=False):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detector = dlib.get_frontal_face_detector()
    rects = detector(gray, 0)#tenta achar o rosto da forma que esta
    i=1

    #tenta achar o rosto em outras rotacoes
    while len(rects) is 0 and i<4:
        gray = rotate(gray, 1)
        frame = rotate(frame, 1)#rotaciona o frame, para poder pegar o rosto na posicao certa depois
        rects = detector(gray, 0)
        i+=1

    return rects

#achar face com o OpenCV
def acha_face_OpenCV(frame, verbose=False):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cascPath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascPath)

    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    return faces
