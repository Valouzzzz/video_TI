import cv2
import math

VIDEO = "video_144p.mp4"

LARGEUR = 166
HAUTEUR = 120

OFFSET_X = (320 - LARGEUR) // 2
OFFSET_Y = (240 - HAUTEUR) // 2

couleurs = {
    "BLUE":     (0, 0, 255),
    "RED":      (255, 0, 0),
    "BLACK":    (0, 0, 0),
    "MAGENTA":  (255, 0, 255),
    "GREEN":    (0, 128, 0),
    "ORANGE":   (255, 165, 0),
    "BROWN":    (139, 69, 19),
    "NAVY":     (0, 0, 128),
    "LTBLUE":   (173, 216, 230),
    "YELLOW":   (255, 255, 0),
    "WHITE":    (255, 255, 255),
    "LTGRAY":   (211, 211, 211),
    "MEDGRAY":  (128, 128, 128),
    "GRAY":     (96, 96, 96),
    "DARKGRAY": (48, 48, 48)
}


# Chaque couleur possède un numéro
couleur_id = {
    "BLUE": 0,
    "RED": 1,
    "BLACK": 2,
    "MAGENTA": 3,
    "GREEN": 4,
    "ORANGE": 5,
    "BROWN": 6,
    "NAVY": 7,
    "LTBLUE": 8,
    "YELLOW": 9,
    "WHITE": 10,
    "LTGRAY": 11,
    "MEDGRAY": 12,
    "GRAY": 13,
    "DARKGRAY": 14
}

def couleur_proche(r, g, b):

    meilleure_couleur = None
    meilleure_distance = float("inf")

    for nom, (cr, cg, cb) in couleurs.items():

        distance = (
            (r - cr) ** 2 +
            (g - cg) ** 2 +
            (b - cb) ** 2
        )

        if distance < meilleure_distance:
            meilleure_distance = distance
            meilleure_couleur = nom

    return meilleure_couleur

video = cv2.VideoCapture(VIDEO)

frames = []

numero_frame = 0

while True:

    ret, frame = video.read()

    if not ret:
        break

    frame = cv2.resize(
        frame,
        (LARGEUR, HAUTEUR),
        interpolation=cv2.INTER_AREA
    )

    image = []

    for ligne in range(HAUTEUR):

        for colonne in range(LARGEUR):

            bleu, vert, rouge = frame[ligne, colonne]

            couleur = couleur_proche(
                int(rouge),
                int(vert),
                int(bleu)
            )

            image.append(couleur)

    frames.append(image)

    numero_frame += 1

    if numero_frame % 10 == 0:
        print("Frame :", numero_frame)


video.release()

print()
print("Nombre de frames :", len(frames))
print("Pixels par frame :", LARGEUR * HAUTEUR)

changements = []

premiere_image = []

for pixel in range(len(frames[0])):

    couleur = frames[0][pixel]

    position = pixel
    couleur_num = couleur_id[couleur]

    premiere_image.append(
        (position, couleur_num)
    )

changements.append(premiere_image)


for i in range(1, len(frames)):

    frame_changements = []

    ancienne = frames[i - 1]
    nouvelle = frames[i]

    for pixel in range(len(nouvelle)):

        if nouvelle[pixel] != ancienne[pixel]:

            position = pixel
            couleur_num = couleur_id[nouvelle[pixel]]

            frame_changements.append(
                (position, couleur_num)
            )

    changements.append(frame_changements)

    print(
        "Frame",
        i,
        ":",
        len(frame_changements),
        "pixels modifiés"
    )

total_changements = sum(
    len(frame)
    for frame in changements
)

print()
print("Total changements :", total_changements)

print(
    "Moyenne changements/frame :",
    total_changements / len(changements)
)

code = []

code.append("ClrDraw")

for numero_frame, frame in enumerate(changements):

    for debut in range(0, len(frame), 999):

        bloc = frame[debut:debut + 999]

        positions = []

        couleurs_bloc = []

        for position, couleur in bloc:

            positions.append(str(position))
            couleurs_bloc.append(str(couleur))

        code.append(
            "{" + ",".join(positions) + "}→L1"
        )

        code.append(
            "{" + ",".join(couleurs_bloc) + "}→L2"
        )

        code.append(
            f"For(I,1,{len(bloc)})"
        )

        code.append(
            "int(L1(I)/166)→A"
        )

        code.append(
            "L1(I)-166A→B"
        )

        code.append(
            "L2(I)→C"
        )

        code.append(
            "Pxl-On(A+" +
            str(OFFSET_Y) +
            ",B+" +
            str(OFFSET_X) +
            ")"
        )

        code.append("End")

    code.append("Pause .03")


with open("VIDEO.txt", "w", encoding="utf-8") as fichier:

    fichier.write("\n".join(code))


print()
print("================================")
print("Code TI-BASIC généré !")
print("Fichier : VIDEO.txt")
print("================================")
