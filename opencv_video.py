import cv2, time, imutils

cap = cv2.VideoCapture('video.avi')
i = 0
while(cap.isOpened()):
    if(i==180):
        break
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Tons de Cinza',gray)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    i+=1

filtro = 'Redimensionar Fixo'
while(cap.isOpened()):
    if(i==360):
        break
    ret, frame = cap.read()
    resized = cv2.resize(frame, (200, 200))
    cv2.imshow(filtro,resized)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    i+=1

while(cap.isOpened()):
    if(i==510):
        break
    ret, frame = cap.read()
    Senku = frame[120:220, 200:300]
    cv2.imshow('Senku',Senku)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    i+=1

while(cap.isOpened()):
    if(i==660):
        break
    ret, frame = cap.read()
    (h, w, d) = frame.shape
    r = 300.0 / w
    dim = (300, int(h * r))
    resized = cv2.resize(frame, dim)
    cv2.imshow('Redimensionar por proporcao',resized)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    i+=1

while(cap.isOpened()):
    if(i==810):
        break
    ret, frame = cap.read()
    resized = imutils.resize(frame, width=500)
    cv2.imshow('Redimensionar do Imutils',resized)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    i+=1

while(cap.isOpened()):
    if(i==960):
        break
    ret, frame = cap.read()
    (h, w, d) = frame.shape
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, 45, 1.0)
    rotated = cv2.warpAffine(frame, M, (w, h))
    cv2.imshow('Rotacao do OpenCV',rotated)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    i+=1

while(cap.isOpened()):
    if(i==1110):
        break
    ret, frame = cap.read()
    rotated = imutils.rotate(frame, 90)
    cv2.imshow('Rotacao do Imutils',rotated)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    i+=1

while(cap.isOpened()):
    if(i==1260):
        break
    ret, frame = cap.read()
    rotated = imutils.rotate_bound(frame, -45)
    cv2.imshow('Imutils Bound Rotation',rotated)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    i+=1

while(cap.isOpened()):
    if(i==1410):
        break
    ret, frame = cap.read()
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    cv2.imshow('Borrado',blurred)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    i+=1

while(cap.isOpened()):
    if(i==1560):
        break
    ret, frame = cap.read()
    output = frame.copy()
    cv2.rectangle(output, (180, 260), (200, 160), (0, 0, 255), 2)
    cv2.imshow('Retangulo',output)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    i+=1

while(cap.isOpened()):
    if(i==1710):
        break
    ret, frame = cap.read()
    output = frame.copy()
    cv2.circle(output, (300, 150), 20, (255, 0, 0), -1)
    cv2.imshow('Circulo',output)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    i+=1

while(cap.isOpened()):
    if(i==1870):
        break
    ret, frame = cap.read()
    output = frame.copy()
    cv2.line(output, (60, 20), (400, 200), (0, 0, 255), 5)
    cv2.imshow('Linha',output)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break
    i+=1

while(cap.isOpened()):

    ret, frame = cap.read()
    if (not ret):#se nao leu nada, fecha
        break
    output = frame.copy()
    cv2.putText(output, "OpenCV + Dr Stone!!!", (10, 25),
    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow('Texto',output)
    if cv2.waitKey(30) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()



print('||End Application!')
