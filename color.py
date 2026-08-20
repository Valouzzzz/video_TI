import cv2
import math

video = cv2.VideoCapture("video_144p.mp4")

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

            bleu, vert, rouge = frame[ligne, colonne]

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

def tri_frames(liste):
    compteur = 0
    liste_final = []
    liste_final.append(liste[0].copy())
    for image in range(1, len(liste)):
        nouvelle_image = []
        for pixel in range(len(liste[image])):
            if liste[image][pixel] == liste[image-1][pixel]:
                nouvelle_image.append("O")
                compteur += 1
            else:
                nouvelle_image.append(liste[image][pixel])
        liste_final.append(nouvelle_image)
    print("nombre de pixels qui ne vont pas être chargés : " + str(compteur))
    return liste_final

frames = tri_frames(frames)
