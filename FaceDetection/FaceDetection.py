from pathlib import Path
import argparse, sys, os

from funcoes import processando_video, processando_imagem

ap = argparse.ArgumentParser(
    prog='Detecção de Face',
     description='''Esse é um programa de detecção de faces, criado com a biblioteca dlib e opencv
     a cores são azul para a detecção com openCV e Vermelho para o Dlib, como
     pode ver mais à frente, você terá a opção de passar video ou imagem para a detecção, além de ter a opção de
     passar uma saida, onde ele irá salvar

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

    processando_video(args["path_video"], pathOutput, args["skip"], args["codec"], args["output"])



if args["path_image"]:
    processando_imagem(args["path_image"], args["output"])
