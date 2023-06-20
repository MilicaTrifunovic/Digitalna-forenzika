import cv2, math
import random
import os
from algorithm import *
from functions import _int_to_bin, _bin_to_int

#Encode image size in first frame
def encode_img_size(img_size):
    w, h = img_size
    path = frame_location + r"\frame1.png"
    frame1 = Image.open(path)
    frame1_map = frame1.load()
    w_bin = f'{w:012b}'
    h_bin = f'{h:012b}'
    fr, fg, fb = _int_to_bin(frame1_map[0, 0])
    f1r, f1g, f1b = _int_to_bin(frame1_map[0, 1])
    frame1_map[0, 0] = _bin_to_int((fr[:4] + w_bin[:4], fg[:4] + w_bin[4:8], fb[:4] + w_bin[8:]))
    frame1_map[0, 1] = _bin_to_int((f1r[:4] + h_bin[:4], f1g[:4] + h_bin[4:8], f1b[:4] + h_bin[8:]))
    frame1.save(path)


def decode_img_size():
    path = frame_location + r"\frame1.png"
    frame1 = Image.open(path)
    frame1_map = frame1.load()
    fr, fg, fb = _int_to_bin(frame1_map[0, 0])
    f1r, f1g, f1b = _int_to_bin(frame1_map[0, 1])
    w = fr[4:] + fg[4:] + fb[4:]
    h = f1r[4:] + f1g[4:] + f1b[4:]
    w_res = int(w, 2)
    h_res = int(h, 2)

    return w_res, h_res


def encode(start_frame, end_frame, img_name, frame_loc):
    total_frame = end_frame - start_frame
    filedata = Image.open(img_name)
    encode_img_size(filedata.size)
    datapoints = math.floor(filedata.size[1] / total_frame) # Data distribution per frame
    rest = filedata.size[1] - datapoints * (total_frame - 1)
    counter = start_frame
    frame_num = 0
    print("Encoding...")
    for i in range(0, filedata.size[1], datapoints):
        if frame_num == total_frame - 1:
            datapoints = rest
        numbering = frame_loc + r"\frame" + str(counter) + ".png"
        encode_img = filedata.crop((0, i, filedata.size[0], i+datapoints)) # left, top, right, bottom
        #encode_img.save(os.getcwd() + r"\encode_img_part" + str(counter) + ".jpg")

        kt = KnightTour(numbering)
        new_img = kt.stego_encode((0, 0), encode_img)
        kt.print_list()
        new_img.save(numbering) # Save as new frame

        counter += 1
        frame_num += 1
    print("Complete encode!\n")


def decode(start_frame, end_frame, frame_loc):
    cover_img_w, cover_img_h = decode_img_size()
    total_frame = end_frame - start_frame
    datapoints = math.floor(cover_img_h / total_frame) # Data distribution per frame
    size = datapoints
    rest = cover_img_h - datapoints*(total_frame-1)
    counter = start_frame
    final_img = Image.new("RGB", (cover_img_w, cover_img_h))
    print("Decoding...")
    for frame_num in range(total_frame):
        if(frame_num == total_frame - 1):
            datapoints = rest
        numbering = frame_loc + r"\frame" + str(counter) + ".png"
        kt = KnightTour(numbering)
        new_image = kt.stego_decode((0, 0), datapoints, cover_img_w)
        kt.print_list()
        final_img.paste(new_image, (0, frame_num*size))
        counter += 1
    final_img.save(os.getcwd() + r"\final_image.png")
    print("Complete decode!\n")


if __name__ == '__main__':
    img_location = input("Input image to hide (inc. extension): ")
    img = Image.open(img_location)
    video_location = input("Input video (inc. extension): ")
    cap = cv2.VideoCapture(video_location)
    fps = cap.get(cv2.CAP_PROP_FPS)
    count = 1

    frame_location = os.getcwd() + r"\frames"
    os.mkdir(frame_location)

    while cap.isOpened():
        ret, frame = cap.read()
        if ret:
            cv2.imwrite('frames/frame{:d}.png'.format(count), frame)
            count += 1
        else:
            break

    print("Please enter start and end frame where data will be hidden at")
    frame_start = int(input("Input start frame: "))
    frame_end = int(input("Input end frame: "))

    #Random frames selection
    # frame_start = random.randint(1, math.ceil(count/2))
    # if count-frame_start < img.size[1]:
    #     end = count
    # else:
    #     end = img.size[1]
    # frame_end = random.randint(frame_start, end)
    # print(frame_start)
    # print(frame_end)

    encode(frame_start, frame_end, img_location, frame_location)
    decode(frame_start, frame_end, frame_location)

    img = cv2.imread("frames/frame1.png")
    height, width, layers = img.shape
    size = (width, height)

    out = cv2.VideoWriter('final_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), fps, size)

    for i in range(1, count):
        filename = 'frames/frame' + str(i) + '.png'
        img = cv2.imread(filename)
        out.write(img)

    out.release()

