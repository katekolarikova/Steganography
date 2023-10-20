import sys

import numpy as np
import PIL.Image as Image

# hlavicka - pocet bitu, zacatek prvniho, nazev souboru, offset

class Encoder:
    def __init__(self):
        self.width = 0
        self.height = 0

    def create_header(self, num_of_bits:int, file_name:str, type_of_info:str):
        # size_of_header = 32+64*8+8
        encoded_num_of_bits = num_of_bits.to_bytes(4, byteorder='big')
        encoded_file_name = file_name.encode('utf-8')+ bytes(64 - len(file_name))
        encoded_type_of_info = type_of_info.to_bytes(1, byteorder='big')

        header = encoded_num_of_bits + encoded_file_name + encoded_type_of_info

        return header

    def load_image(self, path:str):
        self.path = path
        self.img = Image.open(self.path)
        self.width, self.height = self.img.size

    def modify_bit(self, original_number: int,
                   bit_value: int) -> int:
        return (original_number & ~1) | bit_value

    def encode_text(self, message:str, path:str):

        self.load_image(path)

        # check if message is too long
        encoding_capacity = self.height*self.width * 3
        message_bits_len = sys.getsizeof(message) * 8
        if message_bits_len > encoding_capacity:
            raise ValueError("Message is too long to encode")

        header = self.create_header(len(message), path, 0)

        text_bytes = message.encode('utf-8') # convert message to bytes
        pixel_data = list(self.img.getdata()) # get pixels from image

        header_bits_array = [int(bit) for byte in header for bit in format(byte, '08b')] # convert header to bits
        text_bits_array = [int(bit) for byte in text_bytes for bit in format(byte, '08b')] # convert message to bits
        bits_to_write = header_bits_array + text_bits_array # merge header and message bits

        current_text_bit = 0

        # chaneg LSB of each pixel
        for i in range(self.height):
            pixel = list(pixel_data[i]) # for each pixel
            for k in range(3): #RGB
                try:
                    x = bits_to_write[current_text_bit]
                    current_text_bit += 1
                except IndexError:
                        break
                pixel[k] = self.modify_bit(pixel[k], x) # modify LSB
                pixel_data[i] = tuple(pixel)

        new_image = Image.new(self.img.mode, self.img.size)

        #save image
        new_image.putdata(pixel_data)
        new_image.save("cover-secret.png")



    def encode_file(self, path:str):
        with open(path, "rb") as f:
            data = f.read()
            data_size = len(data) * 8

            encoding_capacity = self.height * self.width * 3
            if data_size > encoding_capacity:
                raise ValueError("Message is too long to encode")

            text_bits_array = [int(bit) for byte in data for bit in format(byte, '08b')]
            # for byte in data:
            #     binary_byte = f'{byte:08b}'

            pixel_data = list(self.img.getdata())
            new_image = Image.new(self.img.mode, self.img.size)
            current_text_bit = 0
            self.text_bits_array_len = len(text_bits_array)

            for i in range(self.height):
                pixel = list(pixel_data[i])
                for k in range(3):
                    try:
                        x = text_bits_array[current_text_bit]
                        current_text_bit += 1

                    except IndexError:
                        completed = True
                        break
                    pixel[k] = self.modify_bit(pixel[k], x)
                    pixel_data[i] = tuple(pixel)

            new_image.putdata(pixel_data)
            new_image.save("cover-secret.png")



