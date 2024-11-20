import numpy as np
import os


def bbox_to_rle(x_min, y_min, w, h, height, width):
    mask = np.zeros((height, width), dtype=np.uint8)
    for x,y,wid,hei in zip(x_min, y_min, w,h):
        mask[y:(hei+y), x:(wid+x)] = 1
    
    rle = mask_to_rle(np.flipud(mask))
    if len(rle) == 0:
        print("no rle found")
    return rle


def mask_to_rle(mask):

    pixels = mask.T.flatten()  # Flatten the mask
    rle = []
    last_pixel = 0
    run_length = 0
    
    for i, pixel in enumerate(pixels):
        if pixel == last_pixel:
            run_length += 1
        else:
            if last_pixel == 1:
                rle.append(run_length)
            elif last_pixel == 0:
                rle.append(i + 1)
            run_length = 1
            last_pixel = pixel
    
    # Append the last run
    if last_pixel == 1:
        rle.append(run_length)

    
    return rle


def rel2abs(x_min, y_min, width, height, src_width, src_height):
    center_x_abs = x_min * src_width
    center_y_abs = y_min * src_height

    width_abs = width * src_width
    height_abs = height * src_height
    if height_abs < 0:
        print("n")
    return (center_x_abs, width_abs, center_y_abs, height_abs)


def make_rle_str(start_str, results):
    x=[]
    y=[]
    h=[]
    w=[]
    for g in results:
        abs_x, abs_w, abs_y, abs_h = map(int, rel2abs(g[0], g[1], g[2], g[3], 525, 350))
        x.append(abs_x)
        y.append(abs_y)
        w.append(abs_w)
        h.append(abs_h)
    rle = bbox_to_rle(x, y, w, h, 350, 525)

    rle_str = ""
    for i in rle:
        rle_str+=f" {i}"
    start_str += rle_str[1:]

    return start_str


def main():
    with open("results.csv", "w") as outfile:
        outfile.write("Image_Label,EncodedPixels\n")
        for fname in os.listdir():
            if fname.split(".")[-1] != "txt":
                continue

            name = fname.split(".")[0]

            sugar_results = []
            gravel_results = []
            flower_results = []
            fish_results = []
            with open(fname) as infile:
                for line in infile:
                    cls ,x_min,y_min, x_max, y_max = map(float, line.split())
                    if y_max-y_min <0:
                        print("Invalid")
                    if cls == 2:
                        gravel_results.append((x_min, y_min,x_max-x_min, y_max-y_min))
                    elif cls == 0:
                        fish_results.append((x_min, y_min,x_max-x_min, y_max-y_min))
                    elif cls == 1:
                        flower_results.append((x_min, y_min,x_max-x_min, y_max-y_min))
                    elif cls == 3:
                        sugar_results.append((x_min, y_min,x_max-x_min, y_max-y_min))

            if len(gravel_results):
                outfile.write(make_rle_str(f"{name}.jpg_Gravel, ", gravel_results) + "\n")

            if len(flower_results):
                outfile.write(make_rle_str(f"{name}.jpg_Flower, ", flower_results) + "\n")
            if len(sugar_results):
                outfile.write(make_rle_str(f"{name}.jpg_Sugar, ", sugar_results) + "\n")
            if len(fish_results):
                outfile.write(make_rle_str(f"{name}.jpg_Fish, ", fish_results) + "\n")

if __name__ == "__main__":
    main()





