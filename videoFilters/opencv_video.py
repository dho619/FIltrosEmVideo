import cv2, imutils

cap = cv2.VideoCapture('video.avi') # Lendo o video e guardando na variavel cap
i = 0
for i in range(180):#Rodar 180 frames
    ret, frame = cap.read() #Pegando a imagem(frame) atual, o ret e o retorno se conseguiu ou nao ler
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #transformando imagem para tom de Cinza
    cv2.imshow('Tons de Cinza',gray) #exibindo a imagem em tom de cinza

    '''cv2.waitKey(30) vai esperar pelo menos 30milisegundos antes de continuar
       0xFF == ord('q') se a tecla apertada foi 'q'
       Isso faz com que todo frame aguarde pelo menos 30milisegundos e se apertar q sai do while
    '''
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break


#Para frente irei comentar apenas o que nao foi comentado acima
for i in range(180):
    ret, frame = cap.read()
    resized = cv2.resize(frame, (200, 200))  #usa o opencv para redimencionar o video no tamanho passado
    cv2.imshow('Redimensionar Fixo',resized)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

for i in range(150):
    ret, frame = cap.read()
    Senku = frame[120:220, 200:300]#recorta uma parte da imagem, que nada mais e do que uma matriz de pixels
    cv2.imshow('Senku',Senku)      #do pixel 120 ao 220 na vertical e do 200 ao 300 na horizontal
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

for i in range(150):
    ret, frame = cap.read()
    (h, w, d) = frame.shape # pegando as dimensoes do frame linhas(height), colunas(width) e dimensoes
    r = 300.0 / w #pegando a proporcao de 300 para a largura anterior
    dim = (300, int(h * r)) #cria uma tupla com 300 na primeira posicao e a antiga altura vezes a proporcao na segunda
    resized = cv2.resize(frame, dim) # usa novamente o opencv para redimencionar
    cv2.imshow('Redimensionar por proporcao',resized)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

for i in range(150):
    ret, frame = cap.read()
    resized = imutils.resize(frame, width=500) #usa o imutils para redimencionar
    cv2.imshow('Redimensionar do Imutils',resized)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

graus=45 #grau de rotacao no inicio
for i in range(150):
    ret, frame = cap.read()
    (h, w, d) = frame.shape #Pegando as coordenadas, altura(h), largura(w) e dimensoes(d)
    center = (w // 2, h // 2) #Pegando o centro da imagem
    M = cv2.getRotationMatrix2D(center, graus, 1.0) #Constroi a matriz de rotacao de acordo com o ponto passado, nesse caso o centro
    rotated = cv2.warpAffine(frame, M, (w, h)) # roda a imagem usando a matriz adiquirida acima
    cv2.imshow('Rotacao do OpenCV',rotated)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    graus += 1 #incrementa o grau de rotacao da imagem

graus = 90 #grau de rotacao no inicio
for i in range(150):
    ret, frame = cap.read()
    rotated = imutils.rotate(frame, graus) #Rotaciona em 90graus usando o imutils
    cv2.imshow('Rotacao do Imutils',rotated)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    graus -= 1 #incrementa o grau de rotacao da imagem

graus = -45 #  grau de rotacao no inicio
for i in range(150):
    ret, frame = cap.read()
    rotated = imutils.rotate_bound(frame, graus)# rotaciona usando o imutils com a funcao rotate_bound
    cv2.imshow('Imutils Bound Rotation',rotated)# que nao deixa perder parte da imagem na rotacao
    if cv2.waitKey(30) & 0xFF == ord('q'):      # (normalmente corta as bordas em rotacoes normais)
        break
    graus += 1

for i in range(150):
    ret, frame = cap.read()
    blurred = cv2.GaussianBlur(frame, (11, 11), 0) #Faz com que a imagem fique borrada, utilizado
    cv2.imshow('Borrado',blurred)               # para reduzir ruidos de alta frequencia
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

for i in range(150):
    ret, frame = cap.read()
    output = frame.copy()
    cv2.rectangle(output, (180, 260), (200, 160), (0, 0, 255), 2) # desenha um retangulo usando as coordenadas passadas
    cv2.imshow('Retangulo',output)                                # sendo os parametros passados: imagem vertice 1,
    if cv2.waitKey(30) & 0xFF == ord('q'):                        # vertice oposto, cor e espessura
        break

for i in range(150):
    ret, frame = cap.read()
    output = frame.copy()
    cv2.circle(output, (300, 150), 20, (255, 0, 0), -1) # desenha um circulo com os parametros: imagem,
    cv2.imshow('Circulo',output)                        # centro, raio, cor e espessura(negativo, preenche o circulo todo)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

for i in range(150):
    ret, frame = cap.read()
    output = frame.copy()
    cv2.line(output, (60, 20), (400, 200), (0, 0, 255), 5)# desenha uma linha com os parametros: imagem
    cv2.imshow('Linha',output)                            # coordenada de inicio, coordenada de fim,
    if cv2.waitKey(30) & 0xFF == ord('q'):                # cor e espessura
        break

while(cap.isOpened()):
    ret, frame = cap.read()
    if (not ret):# se nao leu nada, fecha (se nao leu, provavelmente, acabou o video)
        break
    output = frame.copy()                               # escreve o texto passado, sendo os parametros:
    cv2.putText(output, "OpenCV + Dr Stone!!!", (10, 25), # imagem, texto, coordenada de inicio do texto,
    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)  # font, escala, cor e espessura
    cv2.imshow('Texto',output)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release() #fecha o video
cv2.destroyAllWindows() #destroi todas as janelas abertas



print('||End Application!')
