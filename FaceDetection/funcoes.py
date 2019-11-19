from pathlib import Path
import numpy as np
import dlib, cv2, os
from datetime import datetime
from sys import exit

#Processar se for Video
def processando_video(video, tempdest, skip, codec, output):
    if not os.path.isfile(video):#ve se o video existe
        print('Nao foi possivel ler a Imagem "{}", por favor, tente novamente!'.format(path_image))
        exit()#se nao sai do codigo
    vs = cv2.VideoCapture(video) #abrindo video
    (width, height) = int(vs.get(3)), int(vs.get(4)) #pegando largura e altura
    fps = int(vs.get(5)) #pegando numero de fps
    fourcc = cv2.VideoWriter_fourcc(*codec)#pegando codec
    new_video = cv2.VideoWriter(tempdest, fourcc, fps, (width, height), True) #criando novo arquivo de video com largura, altura e fps do original
    read = 0 # para controle, caso precise parar antes de terminar (em testes)

    print('Processando video, isso pode demorar um pouco, aguarde por favor...')
    #Detectando os rostos na imagens
    while True:
        (sucess, frame) = vs.read() #frame recebe o frame atual e sucess recebe true ou false, se leu ou nao
        if not sucess:#se nao conseguiu ler
            break     #para o codigo(normalmente, acaabou o video)
        read += 1 #adiciona que leu mais um

        if read == 1 or read % skip == 0:#o numero de pulos antes de fazer outra deteccao, passado por parametro
            faces = acha_face_Dlib(frame) #acha face com Dlib
            faces2 = acha_face_OpenCV(frame) #acha face com openCV

        face_image = drawRectangles(frame, faces, faces2) ##desenha os rosto na imagem
        new_video.write(face_image) #vai salvando os frame no arquivo temporario

    vs.release() #fecha o video
    new_video.release() #fecha o video criado temporariamente
    print('')
    input('Indentificacao de faces concluida! Aperte enter para exibir o resultado: ')

    showVideo(tempdest) # exibir o video, que esta na pasta temporaria

    if output: #se foi passado uma saida
        print('Salvando Video...')
        saveVideo(tempdest, output, video) #salva o video

    removeTemp()#remove a pasta temp e tudo que esta dentro dela

#Processar se for Imagem
def processando_imagem(imagem, output=''):
    if not os.path.isfile(imagem): #ve se a imagem existe
        print('Nao foi possivel ler a Imagem "{}", por favor, tente novamente!'.format(path_image))
        exit()#se nao sai do codigo

    NovaImagem = cv2.imread(imagem) #le a imagem

    faces = acha_face_Dlib(NovaImagem) #acha as faces com dlib
    faces2 = acha_face_OpenCV(NovaImagem)#acha as faces com openCV

    face_image = drawRectangles(NovaImagem, faces, faces2) #desenha os rostos

    cv2.imshow('Resultado',face_image) #exibe a imagem resultado
    cv2.waitKey(0) #apertar  alguma tecla para continuar

    if output: #se passou um caminho de saida
        saveImage(face_image, output, imagem) #salva a imagem nesse caminho

#Desenhar os retangulos
def drawRectangles(imagem, faces, faces2):
    face_image = imagem.copy() #faz uma copia da imagem
    for (_, face) in enumerate(faces): #passa cada rosto acha pelo dlib
        l_x = int(face.tl_corner().x) #e pega suas posicoes
        t_y = int(face.tl_corner().y)
        r_x = int(face.br_corner().x)
        b_y = int(face.br_corner().y)
        cv2.rectangle(face_image, (l_x, t_y), (r_x, b_y), (0, 0, 255), 2)#desenha o retangulo red

    for (x, y, w, h) in faces2:#passa cada rosto achado no openCV
        cv2.rectangle(face_image, (x, y), (x+w, y+h), (255, 0, 0), 2)# desenha o retangulo azul

    return face_image #retorna a imagem com os rostos destacados, que foram encontrados pelo openCV e Dlib

#exibir video
def showVideo(output):
    vs = cv2.VideoCapture(output)#lendo video
    vs.set(1, 0) #seta o indice 1 (CV_CAP_PROP_POS_FRAMES) para 0, ou seja, vai voltar o indice do video para 0
    while True:#loop infinito(ou ate achar um break), o mesmo que usar cv2.isOpened()
        (sucess, frame) = vs.read() #le o frame atual, frame recebe o frame atual e sucess se consegiu ou nao ler

        if not sucess:#se nao conseguiu ler, stop video (se entrar aki, e pq acabou video)
            break
        cv2.imshow('Exibicao do Resultado',frame)#Exibe o resultado
        if cv2.waitKey(30) & 0xFF == ord('q'):#aguarda pelo menos 30milisegundos por
            break                             #frame e se apertar q, ele sai da while (para de exibir o video)

    vs.release()#fecha o video
    cv2.destroyAllWindows()#destroi todas janelas abertas do video

#salvar video
def saveVideo(antigoCaminho, destino, video):
    pathVideo = video #copia do caminho do video
    ext = pathVideo.rfind('.') #posicao do ultimo ponto, que e a extencao do arquivo
    barra = pathVideo.rfind('/') + 1 #posicao da ultima barra
    if barra == -1:#caso nao ache barra, barra recebe a posicao 0
        barra = 0
    nomeVideo = pathVideo[barra:ext] #sobra apenas o nome do video
    today = datetime.now() #pega a data e hora atual para criar um novo nome unico
    diahora = '{}{}{}_{}{}{}'.format(today.day, today.month, today.year, today.hour, today.minute,today.second) #formata a data e hora
    newDestino = destino# Faz um copia do destino
    if newDestino[0] == '.':#tirar . do comeco
        newDestino = newDestino[1:]
    if newDestino[0] == '/': #tirar / do comeco
        newDestino = newDestino[1:]
                                #caminho absoluto  #novo destino #nome do Video
    newLocal = os.path.sep.join([os.getcwd() +     newDestino, "{}-{}.avi".format(nomeVideo,diahora)])
    try:
        os.rename(antigoCaminho, newLocal)#copia o arquivo da temp para o novo destino
        print('Video foi salvo com sucesso! Local do arquivo: {}'.format(newLocal))
    except:#caso de erro
        print('Nao foi possivel salvar o video, tente novamente!')

#salvar imagem
def saveImage(image, destino, pathImage):
    ext = pathImage.rfind('.') #posicao do ultimo ponto, que e a extencao do arquivo
    barra = pathImage.rfind('/') + 1 #posicao da ultima barra
    if barra == -1:#caso nao ache barra, barra recebe a posicao 0
        barra = 0
    nameImage = pathImage[barra:ext] #pega so o nome da imagem

    today = datetime.now() #pega data e hora atual para criar um novo nome unico
    diahora = '{}{}{}_{}{}{}'.format(today.day, today.month, today.year, today.hour, today.minute,today.second) #formata data e hora

    newDestino = destino# Faz um copia do destino
    if newDestino[0] == '.':#tirar . do comeco
        newDestino = newDestino[1:]
    if newDestino[0] == '/': #tirar / do comeco
        newDestino = newDestino[1:]
                             #caminho absoluto  #novo destino #nome do Video
    local = os.path.sep.join([os.getcwd() +     newDestino,   "{}-{}.png".format(nameImage,diahora)])
    try:
        cv2.imwrite(local, image)#salva a imagem no local passado
        print('A imagem foi salvo com sucesso! Local do arquivo: {}'.format(local))
    except:#caso de erro
        print('Nao foi possivel salvar a imagem, tente novamente!')

#remover a pasta temporaria
def removeTemp():
    try:
        path ="./temp" #pega o caminho da pasta temporaria
        dir = os.listdir(path) #pega todos arquivos que tem dentro dela
        for file in dir: #passa por cada arquivo
            os.unlink('./temp/{}'.format(file))#apaga o arquivo
        os.rmdir(path)#apaga pasta temp
    except:#caso de erro
        print("Nao foi possivel remover a pasta temp!")

#rodar a imagem em 90graus n vezes (times, define o numero de vezes)
def rotate(image, times=1):
    return np.rot90(image, times)#roda a imagem

#achar face com o Dlib
def acha_face_Dlib(frame, verbose=False):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#transforma a imagem em cinza
    detector = dlib.get_frontal_face_detector() #criando um objeto do face_detector
    rects = detector(gray, 0)#tenta achar o rosto da forma que esta
    i=1

    #tenta achar o rosto em outras rotacoes, caso nao achou na anterior
    while len(rects) is 0 and i<4:
        gray = rotate(gray, 1) #rotaciona a imagem
        frame = rotate(frame, 1)#rotaciona o frame, para poder pegar o rosto na posicao certa depois
        rects = detector(gray, 0)#tenta achar o rosto
        i+=1

    return rects #retorna os rostos achados

#achar face com o OpenCV
def acha_face_OpenCV(frame, verbose=False):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #transforma a imagem em cinza

    cascPath = "haarcascade_frontalface_default.xml" #pega o caminho do haarcascade (pegado ja pronto na net)
    faceCascade = cv2.CascadeClassifier(cascPath) #carrega o haarcascade (nescessario para encontrar a face)

    faces = faceCascade.detectMultiScale( #tenta detectar o rosto com alguns parametros
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.CASCADE_SCALE_IMAGE
    )

    return faces #retorna os rostos achados
