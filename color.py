import cv2
import struct

from tivars.types import TIProgram, TIAppVar
from tivars.models import TI_83PCE

def convertor_Ti(name_input:str):
    VIDEO = name_input

    FICHIER_PROGRAMME = "VIDEO.8xp"
    FICHIER_APPVAR = "VIDEO.8xv"

    LARGEUR = 166
    HAUTEUR = 120

    NB_PIXELS = LARGEUR * HAUTEUR

    MAX_APPVAR = 65535


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

    palette = list(couleurs.values())

    def couleur_proche(r, g, b):

        meilleure_id = 0
        meilleure_distance = float("inf")

        for i, (cr, cg, cb) in enumerate(palette):

            distance = (
                (r - cr) ** 2 +
                (g - cg) ** 2 +
                (b - cb) ** 2
            )

            if distance < meilleure_distance:

                meilleure_distance = distance
                meilleure_id = i

        return meilleure_id

    print("Loading video...")

    video = cv2.VideoCapture(VIDEO)

    frames = []

    numero = 0

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

        for y in range(HAUTEUR):

            for x in range(LARGEUR):

                b, g, r = frame[y, x]

                couleur = couleur_proche(
                    int(r),
                    int(g),
                    int(b)
                )

                image.append(couleur)

        frames.append(image)

        numero += 1

        print(
            f"Frame {numero} completed"
        )


    video.release()


    if len(frames) == 0:

        print("ERROR: no frame found.")

        exit()


    print()
    print("================================")
    print("VIDEO")
    print("================================")
    print("Frames :", len(frames))
    print("Pixels/frame :", NB_PIXELS)
    print("================================")

    def encoder_premiere_frame(frame):

        """
        2 pixels par octet.

        Chaque couleur est comprise entre 0 et 14.
        Elle tient donc sur 4 bits.
        """

        resultat = bytearray()

        for i in range(0, len(frame), 2):

            pixel1 = frame[i]

            if i + 1 < len(frame):
                pixel2 = frame[i + 1]
            else:
                pixel2 = 0

            octet = (
                (pixel1 << 4)
                |
                pixel2
            )

            resultat.append(octet)

        return resultat

    def encoder_changements(ancienne, nouvelle):

        """
        Encode les pixels modifiés.

        Format :

        position : 2 octets
        couleur  : 1 octet

        On utilise ensuite un RLE simple lorsque plusieurs
        pixels consécutifs ont la même couleur.
        """

        resultat = bytearray()

        i = 0

        while i < len(nouvelle):

            if nouvelle[i] == ancienne[i]:

                i += 1
                continue

            couleur = nouvelle[i]

            debut = i
            longueur = 1

            while (
                i + longueur < len(nouvelle)
                and
                nouvelle[i + longueur] == couleur
                and
                nouvelle[i + longueur] != ancienne[i + longueur]
            ):

                longueur += 1

            if longueur == 1:

                resultat.append(0)

                resultat += struct.pack(
                    "<H",
                    debut
                )

                resultat.append(
                    couleur
                )

            else:

                resultat.append(1)

                resultat += struct.pack(
                    "<H",
                    debut
                )

                resultat += struct.pack(
                    "<H",
                    longueur
                )

                resultat.append(
                    couleur
                )

            i += longueur

        return resultat

    print()
    print("Compression...")


    donnees = bytearray()

    donnees += b"VID1"

    donnees += struct.pack(
        "<H",
        LARGEUR
    )

    donnees += struct.pack(
        "<H",
        HAUTEUR
    )

    donnees += struct.pack(
        "<H",
        len(frames)
    )

    premiere = encoder_premiere_frame(
        frames[0]
    )

    donnees += struct.pack(
        "<I",
        len(premiere)
    )

    donnees += premiere


    print(
        "Frame 0 :",
        len(premiere),
        "octets"
    )

    ancienne = frames[0]


    for numero in range(1, len(frames)):

        nouvelle = frames[numero]

        changements = encoder_changements(
            ancienne,
            nouvelle
        )

        donnees += struct.pack(
            "<I",
            len(changements)
        )

        donnees += changements

        print(
            "Frame",
            numero,
            ":",
            len(changements),
            "octets"
        )

        ancienne = nouvelle

    taille = len(donnees)

    print()
    print("================================")
    print("RESULT")
    print("================================")
    print("Size :", taille, "octets")
    print("Size :", round(taille / 1024, 2), "Ko")
    print("================================")

    if taille > MAX_APPVAR:

        print()
        print("ATTENTION !")
        print(
            "The data show",
            taille,
            "octets."
        )

        print(
            "Tivars will probably not be able to",
            "not create a single AppVar."
        )

        print()
        print(
            "Reduce the resolution or",
            "the number of frames."
        )

        exit()

    print()
    print("Creation of VIDEO.8xv...")


    appvar = TIAppVar(
        name="VIDEO",
        data=bytes(donnees)
    )

    appvar.save(
        FICHIER_APPVAR,
        model=TI_83PCE
    )


    print(
        "VIDEO.8xv created !"
    )

    """
    Pour le moment, ce programme sert uniquement
    à vérifier que le .8xp est correctement généré.

    Le lecteur vidéo sera ajouté ensuite.
    """

    code = """
    ClrHome
    ClrDraw
    Disp "VIDEO PLAYER"
    Disp "DONNEES OK"
    Pause
    """

    print()
    print("Creation of VIDEO.8xp...")


    programme = TIProgram(
        code,
        name="VIDEO"
    )

    programme.save(
        FICHIER_PROGRAMME,
        model=TI_83PCE
    )


    print()
    print("================================")
    print("FINISHED")
    print("================================")
    print("Program file :", FICHIER_PROGRAMME)
    print("Data file   :", FICHIER_APPVAR)
    print("================================")
