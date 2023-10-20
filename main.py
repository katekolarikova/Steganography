from decoder import Decoder
from encoder import Encoder

if __name__ == '__main__':

    encoder = Encoder()
    decoder = Decoder()
    encoder.encode_text("hello world", "sec_pic.png")
    decoder.decode_text("cover-secret.png")
