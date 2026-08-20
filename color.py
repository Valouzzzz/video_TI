import cv2
import math

video = cv2.VideoCapture("video_144p.mp4")

# Couleurs de référence en RGB
couleurs = {
    "BLUE":    (0, 0, 255),
    "RED":     (255, 0, 0),
    "BLACK":   (0, 0, 0),
    "MAGENTA": (255, 0, 255),
    "GREEN":   (0, 128, 0),
    "ORANGE":  (255, 165, 0),
    "BROWN":   (139, 69, 19),
    "NAVY":    (0, 0, 128),
    "LTBLUE":  (173, 216, 230),
    "YELLOW":  (255, 255, 0),
    "WHITE":   (255, 255, 255),
    "LTGRAY":  (211, 211, 211),
    "MEDGRAY": (128, 128, 128),
    "GRAY":    (96, 96, 96),
    "DARKGRAY":(48, 48, 48)
}


# Trouve la couleur la plus proche
def couleur_proche(r, g, b):

    meilleure_couleur = None
    meilleure_distance = float("inf")

    for nom, (cr, cg, cb) in couleurs.items():

        distance = math.sqrt(
            (r - cr) ** 2 +
            (g - cg) ** 2 +
            (b - cb) ** 2
        )

        if distance < meilleure_distance:
            meilleure_distance = distance
            meilleure_couleur = nom

    return meilleure_couleur


frames = []

while True:

    ret, frame = video.read()

    if not ret:
        break

    image = []

    for ligne in range(120):
        for colonne in range(166):

            # OpenCV donne BGR
            bleu, vert, rouge = frame[ligne, colonne]

            # Conversion en RGB
            couleur = couleur_proche(
                int(rouge),
                int(vert),
                int(bleu)
            )

            image.append(couleur)

    frames.append(image)


video.release()


print("Nombre d'images :", len(frames))
print("Nombre de pixels par image :", len(frames[0]))
print("Premier pixel :", frames[0][0])
print("Dernier pixel :", frames[0][-1])

