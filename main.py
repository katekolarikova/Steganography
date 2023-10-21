from decoder import Decoder
from detector import Detector
from encoder import Encoder

if __name__ == '__main__':

    encoder = Encoder()
    decoder = Decoder()
    detector = Detector()

    encoder.encode_text("hello world", "test2.jpg")

    result = detector.detect4("cover-secret.png")
    result = detector.detect4("test2.jpg")

    # encoder.encode_text("hello world", "sec_pic.png")
    # decoder.decode_text("cover-secret.png")


