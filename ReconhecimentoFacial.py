import cv2, sys

# Obter imagem fornecida pelo usuário
imagePath = sys.argv[1]
cascPath = "haarcascade_frontalface_default.xml"

# Crie a cascata haar
faceCascade = cv2.CascadeClassifier(cascPath)

# Lendo a imagem
image = cv2.imread(imagePath)
#transformando em cinza a imagem
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Detecta rostos na imagem
faces = faceCascade.detectMultiScale(
    gray,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags = cv2.CASCADE_SCALE_IMAGE
)

print("Encontrado {0} faces!".format(len(faces)))

# Desenhando um retângulo ao redor das faces
for (x, y, w, h) in faces:
    cv2.rectangle(image, (x, y), (x+w, y+h), (0, 255, 0), 2)

cv2.imshow("Faces found", image)
cv2.waitKey(0)
