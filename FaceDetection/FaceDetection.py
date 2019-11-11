from pathlib import Path
import argparse, sys, os

from funcoes import processando_video, processando_imagem

#CRIANDO A APRESENTACAO DO HELP DO PROGRAMA
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

#PASSANDO ARGUMENTOS SUPORTADOS
ap.add_argument("-v", "--path_video", type=str, required=False, help="Caminho de onde esta o vídeo")
ap.add_argument("-i", "--path_image", type=str, required=False, help="Pasta com a imagem")
ap.add_argument("-o", "--output", type=str, required=False, help="Diretorio para onde vai a saida, caso seja passado")
ap.add_argument("-s", "--skip", type=int, default=5, help="Numero de frames que deve pular entre cada aplicação de detecção de face.")
ap.add_argument("-c", "--codec", type=str, default="MJPG", help="codec para a saida do video")
args = vars(ap.parse_args())

#SE NAO TEM CAMINHO DE VIDEO E NEM IMAGEM, SAI DO PROGRAMA
if not args["path_video"] and not args["path_image"]:
    print('Video ou imagem sao nescessarios!')
    sys.exit()

#SE TEM A SAIDA, MAS NAO A PASTA
if args["output"]:
    path = Path(args["output"])
    path.mkdir(parents=True, exist_ok=True)

#SE TEM UM VIDEO
if args["path_video"]:
    i = 0
    #cria uma pasta temporaria para guardar o video
    temp = Path('temp')
    temp.mkdir(parents=True, exist_ok=True)
    pathOutput = os.path.sep.join(['./temp', "temp.avi"])
    #Chamando a funcao para processar o video
                      #caminho do video, #destino temporario  #numero de pulos #codec         #destino permanente
    processando_video(args["path_video"], pathOutput,         args["skip"],    args["codec"], args["output"])

#SE TEM UMA IMAGEM
if args["path_image"]:
    #Chamando a funcao para processar a Imagem
                      #caminho da Imagem   #destino da imagem
    processando_imagem(args["path_image"], args["output"])
