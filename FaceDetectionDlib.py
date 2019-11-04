
from pathlib import Path
import numpy as np
import argparse, dlib, cv2, sys, os

#Processar Video
def processando_video(video, output, skip):
    vs = cv2.VideoCapture(video)
    (width, height) = int(vs.get(3)), int(vs.get(4))
    fps = int(vs.get(5))
    fourcc = cv2.VideoWriter_fourcc(*args["codec"])
    new_video = cv2.VideoWriter(output, fourcc, fps, (width, height), True)
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

        face_image = frame.copy()
        for (_, face) in enumerate(faces):
            l_x = int(face.tl_corner().x)
            t_y = int(face.tl_corner().y)
            r_x = int(face.br_corner().x)
            b_y = int(face.br_corner().y)

            cv2.rectangle(face_image, (l_x, t_y), (r_x, b_y), (0, 0, 255), 2)

        new_video.write(face_image)

    vs.release()
    new_video.release()
    input('De enter para continuar...')

    vs = cv2.VideoCapture(output)
    vs.set(1, 0)
    while True:
        (sucess, frame) = vs.read()

        if not sucess:#se nao conseguiu ler
            break
        cv2.imshow('Exibicao do Resultado',frame)
        cv2.waitKey(30)

    cv2.destroyAllWindows()



#Processar Imagem
def processando_imagem(imagem, output):
    if not os.path.isfile(imagem):
        print('Nao foi possivel ler a Imagem "{}", por favor, tente novamente!'.format(path_image))
        sys.exit()

    acha_face(cv2.imread(imagem))
    if output:
        print('Aqui vai salvar a imagem: {}'.format(output))

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
     pode ver a frente, você terá a opção de passar video ou imagem para a detecção!''',
     epilog='''Espero ter lhe ajudado! ^-^''',
     formatter_class=argparse.ArgumentDefaultsHelpFormatter
)

ap.add_argument("-v", "--path_video", type=str, required=False, help="Caminho de onde esta o vídeo")
ap.add_argument("-i", "--path_imagem", type=str, required=False, help="Pasta com a imagem")
ap.add_argument("-o", "--output", type=str, required=False, help="Diretorio para onde vai a saida, caso seja passado")
ap.add_argument("-s", "--skip", type=int, default=5, help="Numero de frames que deve pular entre cada aplicação de detecção de face.")
ap.add_argument("-c", "--codec", type=str, default="MJPG", help="codec para a saida do video")
args = vars(ap.parse_args())

if not args["path_video"] and not args["path_imagem"]:
    print('Video ou imagem sao nescessarios!')
    sys.exit()

if args["output"]:
    path = Path(args["output"])
    path.mkdir(parents=True, exist_ok=True)

if args["path_video"]:
    i = 0
    saida = '_' + args["path_video"]
    processando_video(args["path_video"], saida[:-4]+'.avi', args["skip"])



if args["path_imagem"]:
    processando_imagem(args["path_imagem"], args["output"])
