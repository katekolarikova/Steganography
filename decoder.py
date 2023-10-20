from PIL import Image
from bitstring import BitArray

class Decoder:
    def __init__(self):
        self.width = 0
        self.height = 0
        self.img = None


    def load_image(self, path:str):
        self.img = Image.open(path)
        self.width, self.height = self.img.size

    def bits_array_to_string(self, array_of_bits):

        text = ""

        bit_string = ''.join(map(lambda x: chr(48 + x), array_of_bits))
        bytes = [bit_string[i:i + 8] for i in range(0, len(bit_string), 8)]

        # Převedení každé skupiny bitů na odpovídající znak
        for bit_group in bytes:
            if bit_group == "00000000":
                break
            decimal_value = int(bit_group, 2)  # Převod binární hodnoty na desítkovou
            character = chr(decimal_value)  # Převod desítkové hodnoty na znak
            text += character

        return text

    def decode_header(self, size_of_header, array_of_bits):

        header_bits_array = array_of_bits[:size_of_header]

        num_of_bits = header_bits_array[:32]
        tmp = BitArray(num_of_bits)
        num_of_bits = tmp.uint
        print(num_of_bits)
        file_name_bits = header_bits_array[32:544]
        filename = self.bits_array_to_string(file_name_bits)
        print(filename)
        type_of_info = header_bits_array[544:552]
        tmp = BitArray(type_of_info)
        type_of_info = tmp.uint
        print(type_of_info)
        return num_of_bits, filename, type_of_info

    def decode_text(self, path:str):

        self.load_image(path) # image with secret message
        pixel_data = list(self.img.getdata())

        gained_bits_array = [] # secret message bits
        counter = 0
        size_of_header =+32+64*8+8

        #go through pixels and find secret message bits
        for i in range(self.height):
            pixel = list(pixel_data[i])
            for k in range(3):
                try:
                    tmp = pixel[k] & 1
                    gained_bits_array.append(tmp)
                    counter += 1
                except :
                    break

        #get header info
        num_of_bits, filename, type_of_info = self.decode_header(size_of_header, gained_bits_array)
        # get message bits
        bits_with_message = gained_bits_array[size_of_header:size_of_header+num_of_bits*8]
        # decode message
        decoded_string = self.bits_array_to_string(bits_with_message)

        print("Decoded message:", decoded_string)

    def decode_file(self, path: str):
        # Get the image pixel arrays
        result_message = ""
        self.path = path
        self.load_image()
        pixel_data = list(self.img.getdata())
        text_bits_array = []
        counter = 0

        for i in range(self.height):
            pixel = list(pixel_data[i])
            for k in range(3):
                try:
                    if counter == self.text_bits_array_len:
                        break
                    tmp = pixel[k] & 1
                    text_bits_array.append(tmp)
                    counter += 1
                except:
                    completed = True
                    break

        bit_string = ''.join(map(lambda x: chr(48 + x), text_bits_array))
        decoded_string = ""
        bit_groups = [bit_string[i:i + 8] for i in range(0, len(bit_string), 8)]
        with open("test_result.txt", "wb") as f:
            f.write(bit_groups)
