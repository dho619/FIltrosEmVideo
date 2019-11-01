
from pathlib import Path
import numpy as np
import argparse, dlib, cv2, sys, os

#Processar Video
def processando_video(video, output, skip):
    vs = cv2.VideoCapture(video)
    read = 0
    processed = 0

    #len_folder = len(os.listdir(output))

    while True:
        (sucess, frame) = vs.read()

        if not sucess:#se nao conseguiu ler
            break

        read += 1

        if read != 0 and read % skip != 0:#o numero de pulos antes de fazer outra deteccao
            continue

        pathSave = "VideoNew.png"#os.path.sep.join([output,"VideoNew.png"])

        show_result(frame, pathSave)
        processed +=1

    vs.release()
    cv2.destroyAllWindows()

#Processar Imagem
def processando_imagem(imagem, output):
    if not os.path.isfile(imagem):
        print('Nao foi possivel ler a Imagem "{}", por favor, tente novamente!'.format(path_image))
        sys.exit()

    pathSave = 'ImagemFace.png'#os.path.sep.join([output,"ImagemFace.png"])

    show_result(cv2.imread(imagem), pathSave)

#rodar a imagem em 90graus n vezes (times, define o numero de vezes)
def rotate(image, times=1):
    return np.rot90(image, times)

def show_result(frame, output, verbose=False):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detector = dlib.get_frontal_face_detector()
    rects = detector(gray, 0)#tenta achar o rosto da forma que esta

    i=1
    '''
    #tenta achar o rosto em outras rotacoes
    while len(rects) is 0 and i<4:
        gray = rotate(gray, 1)
        frame = rotate(frame, 1)#rotaciona o frame, para poder pegar o rosto na posicao certa depois
        rects = detector(gray, 0)
        i+=1
    '''
    face_image = frame.copy()
    for (_, rect) in enumerate(rects):
        l_x = int(rect.tl_corner().x)
        t_y = int(rect.tl_corner().y)
        r_x = int(rect.br_corner().x)
        b_y = int(rect.br_corner().y)

        #face_image = frame[t_y:b_y , l_x:r_x, :]
        cv2.rectangle(face_image, (l_x, t_y), (r_x, b_y), (0, 0, 255), 2)

    #cv2.imwrite(output, face_image)
    cv2.imshow('Exibicao do Resultado',face_image)
    cv2.waitKey(1)

    if verbose:
        print["[INFO] saved {}".format(path)]

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
args = vars(ap.parse_args())

if not args["path_video"] and not args["path_imagem"]:
    print('Video ou imagem sao nescessarios!')
    sys.exit()

if args["output"]:
    path = Path(args["output"])
    path.mkdir(parents=True, exist_ok=True)

if args["path_video"]:
    processando_video(args["path_video"], args["output"], args["skip"])

if args["path_imagem"]:
    processando_imagem(args["path_imagem"], args["output"])
