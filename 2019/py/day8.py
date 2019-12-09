from __future__ import print_function

IMAGE_SIZE = 25*6

def load_image():
    with open('day8.dat') as f:
        image = f.readlines()
        assert len(image) == 1
        image = map(int, image[0].strip())
        assert len(image) % IMAGE_SIZE == 0
    return image

def decode_layers(image):
    for i in range(0, len(image), IMAGE_SIZE):
        yield image[i:i+IMAGE_SIZE]

image = load_image()
layers = list(decode_layers(image))
zeroes = [layer.count(0) for layer in layers]
idx = zeroes.index(min(zeroes))
print(layers[idx].count(1) * layers[idx].count(2))

msg = []
for x in range(IMAGE_SIZE):
    for layer in layers:
        if layer[x] != 2:
            msg.append(layer[x])
            break

msg = u''.join(map(lambda x: u'\u2591' if x==0 else u'\u2588', msg))
for x in range(6):
    print(msg[x*25:(x+1)*25])
