from PIL import Image
import cv2
import numpy as np

class Detector():
    def __init__(self):
            self.expected_pixels = [(0,0,0), (255,255,255), (30,30,30)]

    def load_image(self, file_path: str):
        self.img = Image.open(file_path)
        width, height = self.img.size

        self.width = width
        self.height = height


    def detect_expected_pixels(self):
        pixel_count  = self.height * self.width
        pixel_data = list(self.img.getdata())

        suspicious_pixels = []
        for i in range(pixel_count):
            if pixel_data[i] not in self.expected_pixels:
                suspicious_pixels.append(pixel_data[i])

        if len(suspicious_pixels) > 5:
            print("Steganography detected in image.")
        else:
            print("Steganography not detected in image.")
    def detect_histogram(self, path:str):

        # Načtěte obrázek
        image = cv2.imread(path)
        image_hist = cv2.calcHist([image], [0], None, [2], [0, 256])
        if len(np.where(image_hist == 0)[1]) > 10:
            print("Steganography detected in image.")
        else:
            print("Steganography not detected in image.")

    def detect_amount_of_one_and_zero(self, path:str):
        self.load_image(path)  # image with secret message
        pixel_data = list(self.img.getdata())

        sum_one = 0
        sum_zero = 0
        pixel_count = self.height * self.width
        for i in range(pixel_count):
            pixel = list(pixel_data[i])
            for k in range(3):
                tmp = pixel[k]
                if tmp==0:
                    sum_zero += 1
                else:
                    sum_one += 1



        # get message bits

        difference = abs(sum_one - sum_zero)
        if difference > 1000:
            print("Steganography detected in image.")
        else:
            print("Steganography not detected in image.")

    def detect4(self, path:str):

        image = Image.open(path)
        binary_data = image.tobytes()
        binary_string = "".join(format(byte, "08b") for byte in binary_data)
        sum_one = 0
        sum_zero = 0
        for bit in binary_string:
            if bit == "0":
                sum_zero += 1
            else:
                sum_one += 1

        difference = abs(sum_one - sum_zero)
        if difference > 1000:
            print("Steganography detected in image.")
        else:
            print("Steganography not detected in image.")
