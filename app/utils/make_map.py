from PIL import Image, ImageFilter, ImageDraw, ImageChops, ImageColor, ImageFont
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from scipy import interpolate
import numpy as np
from numpy import random



BASE_MAP_PATH    = "resources/horror.png"

all_stations = {
    "Questionaire"  : (  35,  40),
    "Map"           : ( 100,  70),
    "Embodiment"    : ( 245,  35),
    "Garage"        : ( 250, 175),
    "Memorial"      : (  85, 125),
    "Drum"          : ( 255, 105),
    "Reading Room"  : ( 115,  85),
    "Antifa Kitchen": ( 115,  85),
    "Playstation"   : ( 115,  85),
    "Fountain"      : ( 115,  85)
}
colors = [
    "#6c1985",
    "#a84085",
    "#d0728e",
    "#eba7a7",
    "#ffddd2",
    "#ffdab2",
    "#ffdf89",
    "#ffeb59",
    "#fffc17"
]
rgb_cols = [ ImageColor.getrgb(c) for c in colors]
fnt = ImageFont.truetype("resources/OpenSans-SemiBold.ttf", 24)

def draw_map(stations, file_path):

    stations = { s: all_stations[s] for s in stations }

    img = Image.open(BASE_MAP_PATH).convert("RGB")


    scale = 200 / img.width 

    background = img.resize((int(img.width * scale), int(img.height * scale)))
    mask = background.copy()

    c = background.info['dpi'][0] / 25.4
    coords = [ (int(x * c  * scale), int(y * c  * scale)) for x, y in stations.values()]
    
    mask = mask.convert('L').filter(ImageFilter.GaussianBlur(3.5))
    mask = mask.point(lambda x: 0 if x< 250 else 255, '1')

    matrix = np.asarray(mask)

    grid = Grid(matrix=matrix)
    finder = AStarFinder(diagonal_movement=DiagonalMovement.always)

    paths = []
    for pntA, pntB in zip(coords[0:-1], coords[1:] ):
        start = grid.node(pntA[0], pntA[1])
        end   = grid.node(pntB[0], pntB[1])
        
        path, runs = finder.find_path(start, end, grid)
        print('operations:', runs, 'path length:', len(path))
        paths.append(path)
        grid.cleanup()

    smooth_paths = []
    for path in paths:
        np_path = np.asarray(path) / scale
 
        # #create spline function
        f, u = interpolate.splprep([np_path[:,0], np_path[:,1]], s=2000)
        # #create interpolated lists of points
        xint, yint = interpolate.splev(np.linspace(0, 1, 60), f)
        smooth_path = [ (x, y) for x, y in zip(xint.tolist(), yint.tolist()) ]
        smooth_paths.append(smooth_path)




    path_img = Image.new("RGB", img.size, (255, 255, 255))
    path_img_draw = ImageDraw.Draw(path_img)
    for i, path in enumerate(smooth_paths):
        path_img_draw.line(path, fill=rgb_cols[i], width=10, joint='curve')

    for i, (name, coord) in enumerate(zip(stations.keys(), coords)):
        r = 15
        box = (
            (coord[0] / scale ) - r,
            (coord[1] / scale ) - r,
            (coord[0] / scale ) + r,
            (coord[1] / scale ) + r
        )
        path_img_draw.ellipse(box, fill = rgb_cols[i], outline=(255,255,255), width=6)
        
        path_img_draw.text( (box[0] + 35, box[1] - 15), name, fill=(0,0,0), stroke_fill = (255, 255, 255), stroke_width = 2, font=fnt)
        


    path_img = path_img.filter(ImageFilter.GaussianBlur(0.5))

    img = ImageChops.darker(img, path_img)
    # mask = mask.resize((img.width, img.height)).convert("RGB").filter(ImageFilter.GaussianBlur(15))
    # img = Image.blend(mask, img, 0.5)
    #img.show()

    img.save(file_path)


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