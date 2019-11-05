
from pathlib import Path
import numpy as np
import argparse, dlib, cv2, sys, os
from datetime import datetime

#Processar Video
def processando_video(video, tempdest, skip):
    vs = cv2.VideoCapture(video) #abrindo video
    (width, height) = int(vs.get(3)), int(vs.get(4)) #pegando largura e altura
    fps = int(vs.get(5)) #pegando numero de fps
    fourcc = cv2.VideoWriter_fourcc(*args["codec"])#pegando codec
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
            faces = acha_face(frame)

        face_image = drawRectangles(frame, faces)
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
        sys.exit()

    pathImage = cv2.imread(imagem)

    faces = acha_face(pathImage)

    face_image = drawRectangles(pathImage, faces)

    cv2.imshow('Resultado',face_image)
    cv2.waitKey(0)

    if output:
        saveImage(face_image, output)

def drawRectangles(imagem, faces):
    face_image = imagem.copy()
    for (_, face) in enumerate(faces):
        l_x = int(face.tl_corner().x)
        t_y = int(face.tl_corner().y)
        r_x = int(face.br_corner().x)
        b_y = int(face.br_corner().y)
        cv2.rectangle(face_image, (l_x, t_y), (r_x, b_y), (0, 0, 255), 2)
    return face_image

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

def saveVideo(video, destino):
    pathVideo= args["path_video"]
    ext = pathVideo.index('.')
    nomeVideo = pathVideo[:ext]
    today = datetime.now()
    diahora = '{}{}{}_{}{}{}'.format(today.day, today.month, today.year, today.hour, today.minute,today.second)
    newLocal = os.path.sep.join([os.getcwd() + '/' + destino, "{}-{}.avi".format(nomeVideo,diahora)])
    try:
        os.rename(video, newLocal)
        print('Video foi salvo com sucesso! Local do arquivo: {}'.format(newLocal))
    except:
        print('Nao foi possivel salvar o video, tente novamente!')

def saveImage(image, destino):
    pathImage = args["path_image"]
    ext = pathImage.index('.')
    nameImage = pathImage[:ext]
    today = datetime.now()
    diahora = '{}{}{}_{}{}{}'.format(today.day, today.month, today.year, today.hour, today.minute,today.second)
    local = os.path.sep.join([os.getcwd() + '/' + destino, "{}-{}.png".format(nameImage,diahora)])
    try:
        cv2.imwrite(local, image)
        print('A imagem foi salvo com sucesso! Local do arquivo: {}'.format(local))
    except:
        print('Nao foi possivel salvar a imagem, tente novamente!')

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

def acha_face(frame, verbose=False):
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

############################################################################
############################################################################
#########-------------Código Principal do Programa-------------#############
############################################################################
############################################################################
ap = argparse.ArgumentParser(
    prog='Detecção de Face',
     description='''Esse é um programa de detecção de faces, criado com a biblioteca dlib, como
     pode ver a frente, você terá a opção de passar video ou imagem para a detecção, alem de se
     passado uma saida ele irá salvar na pasta indicada!

     OBS: Os videos são salvos como .avi e imagem como .png''',
     epilog='''Espero ter lhe ajudado! ^-^''',
     formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

ap.add_argument("-v", "--path_video", type=str, required=False, help="Caminho de onde esta o vídeo")
ap.add_argument("-i", "--path_image", type=str, required=False, help="Pasta com a imagem")
ap.add_argument("-o", "--output", type=str, required=False, help="Diretorio para onde vai a saida, caso seja passado")
ap.add_argument("-s", "--skip", type=int, default=5, help="Numero de frames que deve pular entre cada aplicação de detecção de face.")
ap.add_argument("-c", "--codec", type=str, default="MJPG", help="codec para a saida do video")
args = vars(ap.parse_args())

if not args["path_video"] and not args["path_image"]:
    print('Video ou imagem sao nescessarios!')
    sys.exit()

if args["output"]:
    path = Path(args["output"])
    path.mkdir(parents=True, exist_ok=True)

if args["path_video"]:
    i = 0

    temp = Path('temp')
    temp.mkdir(parents=True, exist_ok=True)
    pathOutput = os.path.sep.join(['./temp', "temp.avi"])

    processando_video(args["path_video"], pathOutput, args["skip"])



if args["path_image"]:
    processando_imagem(args["path_image"], args["output"])
