
from pathlib import Path
import numpy as np
import argparse, dlib, cv2, sys, os

def processando_video(video, output, skip):
    vs = cv2.VideoCapture(video)
    read = 0
    processed = 0

    len_folder = len(os.listdir(output))

    while True:
        (ret, frame) = vs.read()

        if not ret:
            break

        read += 1

        if read % skip != 0:
            continue

        path2save = os.path.sep.join([output,
                "{}.png".format(len_folder+processed)])

        save_faces(frame, path2save)
        processed +=1

    vs.release()
    cv2.destroyAllWindows()

#rodar a imagem em 90graus n vezes (times, define o numero de vezes)
def rotate(image, times):
    return np.rot90(image, times)

def save_faces(frame, output, verbose=False):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    detector = dlib.get_frontal_face_detector()
    rects = detector(gray, 0)

    i=1

    #tenta achar o rosto em cada rotacao
    while len(rects) is 0 and i<4:
        gray = rotate(gray, 1)
        frame = rotate(frame, 1)#rotaciona o frame, para poder pegar o rosto na posicao certa depois
        rects = detector(gray, 0)
        i+=1
    face_image = frame.copy()
    for (_, rect) in enumerate(rects):
        l_x = int(rect.tl_corner().x)# - rect.tl_corner().x*0.1)
        t_y = int(rect.tl_corner().y) #- rect.tl_corner().y*0.2)
        r_x = int(rect.br_corner().x) #+ rect.br_corner().x*0.1)
        b_y = int(rect.br_corner().y) #+ rect.br_corner().y*0.2)

        #face_image = frame[t_y:b_y , l_x:r_x, :]
        #cv2.imwrite(output, face_image)

        cv2.rectangle(face_image, (l_x, t_y), (r_x, b_y), (0, 0, 255), 2)

    #cv2.imwrite(output, face_image)
    cv2.imshow('Supernatural',face_image)
    cv2.waitKey(1)

    if verbose:
        print["[INFO] saved {}".format(path)]





ap = argparse.ArgumentParser()
ap.add_argument("-v", "--input_video", type=str, required=False, help="path to input video")
ap.add_argument("-f", "--input_folder", type=str, required=False, help="path to folder imagens")
ap.add_argument("-o", "--output", type=str, required=True, help="path to output directory of cropped faces")
ap.add_argument("-s", "--skip", type=int, default=5, help="# of frames to skip before applying face detection")
args = vars(ap.parse_args())

if not args["input_video"] and not args["input_folder"]:
    print('input_video ou input_folder sao nescessarios!')
    sys.exit()

path = Path(args["output"])
path.mkdir(parents=True, exist_ok=True)

if args["input_video"]:
    processando_video(args["input_video"], args["output"], args["skip"])

if args["input_folder"]:
    processando_imagens(args["input_folder"], args["output"])
