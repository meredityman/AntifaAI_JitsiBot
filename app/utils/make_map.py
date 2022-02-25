from PIL import Image, ImageFilter, ImageDraw, ImageOps, ImageColor, ImageFont
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from scipy import interpolate
import numpy as np
from numpy import random



BASE_MAP_PATH    = "resources/horror-base.png"
MASK_MAP_PATH    = "resources/horror-mask.png"

all_stations = {
    "Questionaire"  : (1038,  630),
    "Embodiment"    : ( 794,  633),
    "Garage"        : ( 776,  325),
    "Memorial"      : ( 890,  180),
    "Playstation"   : ( 600,  500),
    "Fountain"      : ( 484,  364),  
    "Map"           : ( 285,  456),
    "Drum"          : ( 480,  182),
    "Inflatable"    : ( 407,   63)
}



colors = [
    "#6c1985cc",
    "#a84085cc",
    "#d0728ecc",
    "#eba7a7cc",
    "#ffddd2cc",
    "#ffdab2cc",
    "#ffdf89cc",
    "#ffeb59cc",
    "#fffc17cc"
]
rgb_cols = [ ImageColor.getrgb(c) for c in colors]
fnt = ImageFont.truetype("resources/OpenSans-SemiBold.ttf", 16)

def draw_map(stations, file_path):

    stations = { s: all_stations[s] for s in stations }

    base = Image.open(BASE_MAP_PATH).convert("RGB")
    mask = Image.open(MASK_MAP_PATH).convert("L")

    scale = 200 / mask.width 

    mask = mask.resize((int(mask.width * scale), int(mask.height * scale)))


    coords = [ (int(x   * scale), int(y   * scale)) for x, y in stations.values()]
    
    mask = mask.convert('L').filter(ImageFilter.GaussianBlur(3.5))
    mask = ImageOps.invert(mask)



    matrix = np.asarray(mask)
    print(matrix)
    grid = Grid(matrix=matrix)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

    print(grid)

    paths = []
    for pntA, pntB in zip(coords[0:-1], coords[1:] ):
        print(pntA, pntB)
        start = grid.node(pntA[0], pntA[1])
        end   = grid.node(pntB[0], pntB[1])
        
        path, runs = finder.find_path(start, end, grid)
        print('operations:', runs, 'path length:', len(path))
        paths.append(path)
        grid.cleanup()

    smooth_paths = []
    for path in paths:
        np_path = np.asarray(path) / scale
        try:
            # #create spline function
            f, u = interpolate.splprep([np_path[:,0], np_path[:,1]], s=1000)
            # #create interpolated lists of points
            xint, yint = interpolate.splev(np.linspace(0, 1, 40), f)
            smooth_path = [ (x, y) for x, y in zip(xint.tolist(), yint.tolist()) ]
            smooth_paths.append(smooth_path)
        except:
            smooth_paths.append([])


    path_img = base.copy()
    path_img_draw = ImageDraw.Draw(path_img)
    for i, path in enumerate(smooth_paths):
        if path:
            path_img_draw.line(path, fill=rgb_cols[i], width=6, joint='curve')

    for i, (name, coord) in enumerate(zip(stations.keys(), coords)):
        r = 10
        box = (
            (coord[0] / scale ) - r,
            (coord[1] / scale ) - r,
            (coord[0] / scale ) + r,
            (coord[1] / scale ) + r
        )
        path_img_draw.ellipse(box, fill = rgb_cols[i], outline=(255,255,255), width=2)
        

        text = f"{i:02d} | {name}"
        path_img_draw.text( (box[0] + 35, box[1] - 15), text, fill=(0,0,0), stroke_fill = (255, 255, 255), stroke_width = 2, font=fnt)
        
    background = Image.new('RGB', (1280, 720), (255, 255, 255))
    bg_w, bg_h = background.size
    img_w, img_h = background.size
    offset = ((bg_w - img_w) // 2, (bg_h - img_h) // 2)
    background.paste(path_img, offset)
    path_img = path_img.filter(ImageFilter.GaussianBlur(0.5))

    # img = ImageChops.darker(img, path_img)
    # # mask = mask.resize((img.width, img.height)).convert("RGB").filter(ImageFilter.GaussianBlur(15))
    # # img = Image.blend(mask, img, 0.5)
    # #img.show()
    ath_img = background
    path_img.save(file_path, quality=95)


def get_tests(stations):
    num = 3
    samples = 20


    qs = stations[0]
    stns = stations[1:]

    output = [ ]
    for _ in range(samples):
        random.shuffle(stns)

        out = stns[:num]
        out.insert(0, qs)

        output.append(out)

    return output


def test():

    samples = get_tests(list(all_stations.keys()))

    for i, sample in enumerate(samples):
        print(sample)
        draw_map(sample, f"output/sample_maps/map_{i}.jpg")

# if __name__ == "__main__":
#     test()