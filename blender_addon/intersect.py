import math
from . import d2 

def distance(x,y):
    """
    Simple distance function.
    """
    return (x[0]-y[0])**2 +  (x[1]-y[1])**2

def point_in_poly(x: int, y: int, poly: list[tuple]) -> bool:
    """
    Search if a point is part of a polygone made of a list of points.
    """
    inside = False
    n = len(poly)
    j = n - 1
    for i in range(n):
        xi, yi = poly[i]
        xj, yj = poly[j]
        if ((yi > y) != (yj > y)) and \
           (x < (xj - xi) * (y - yi) / (yj - yi + 1e-9) + xi):
            inside = not inside
        j = i
    return inside

def apply_box_blur(img: list, width:int, height:int, radius: int = 1) -> list:
    """
    Add a blur effect to an image in gey nuance, the parameter radius determine the window effect : 
    1 = 3x3, 2 = 5x5 ...
    """

    output = [0] * width * height

    for y in range(height):
        for x in range(width):
            total = 0
            count = 0
            for dy in range(-radius, radius + 1):
                for dx in range(-radius, radius + 1):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < width and 0 <= ny < height:
                        total += img[nx + (height - 1 - ny) * width]
                        count += 1
            average = total // count
            output[x + (height - 1 - y) * width] = average

    return output

def contour_detection(threshold:float, width : int, height : int, pixels : list, ignore_zones: list[list[tuple]], blur_radius=5) -> list: 
    """ 
    return the contour of the image by applying it a high pass filter.
    """

    blurred = pixels #apply_box_blur(pixels, width,height, blur_radius)
    edges = [0] * width * height

    # Simple Detection : difference between close pixels.
    for y in range(1, height - 1):
        for x in range(1, width - 1):

            # Verify if (x,y) is part of the ignored area
            ignore = any(point_in_poly(x, y, zone) for zone in ignore_zones)
            if ignore:
                continue

            # Approximate gradient (Sobel simplified)
            gx = abs(blurred[(height-1-y)*width+x+1] - blurred[(height-1-y)*width+x-1])
            gy = abs(blurred[(height-1-(y+1))*width+x] - blurred[(height-1-(y-1))*width+x])
            gradient = gx + gy

            # Threshold for the contouring
            edges[x + (height-y) * width] = 255 if gradient > threshold else 0
    return edges

def intersect(width : int, height : int, img : list, stroke : list, ignore_zones: list[list[tuple]], accuracy:float, init_rib_size:float,rib_step:float) -> list:
    """
    Process to create the ribs from the stroke.
    """

    #Create the image of the contour
    pixels = contour_detection(accuracy,width, height, img, ignore_zones) 

    #initialisation paramaters
    SqrtA = d2.getSqrtA(stroke)
    ribs = []
    alpha = rib_step
    correction = init_rib_size

    

    for i in range(0, len(stroke) - 1):

        #Init of the two first points close to stroke point for determining the left and right point of the rib
        p1 = stroke[i]
        p2 = stroke[i + 1]
        middle = ((p1[0] + p2[0]) / 2.0, (p1[1] + p2[1]) / 2.0)

        dx = p2[0] - middle[0]
        dy = middle[1] - p2[1]

        # Right
        rx = dx * math.cos(math.pi/2) + dy * math.sin(math.pi/2)
        ry = dx * math.sin(math.pi/2) - dy * math.cos(math.pi/2)
        right_ext = (rx * correction + middle[0], ry * correction + middle[1])

        # Left
        lx = dx * math.cos(-math.pi/2) + dy * math.sin(-math.pi/2)
        ly = dx * math.sin(-math.pi/2) - dy * math.cos(-math.pi/2)
        left_ext = (lx * correction + middle[0], ly * correction + middle[1])

        #Out of bounds indicator 
        r = 0 
        l = 0 

        # Walk right
        while True:
            grad = d2.d2grad(right_ext, stroke, SqrtA)
            right_ext = (right_ext[0] + grad[0] * alpha,right_ext[1] + grad[1] * alpha) 
            pix = (int(right_ext[0]),int(right_ext[1]))

            if not (0 <= pix[0] < width and 0 <= pix[1] < height):
                r = 1
                break

            if pixels[pix[0] + width* (height-1-pix[1])] == 255:
                break

        # Walk left
        while True:
            grad = d2.d2grad(left_ext, stroke, SqrtA)
            left_ext = (left_ext[0] + grad[0] * alpha, left_ext[1] + grad[1] * alpha)
            pix = (int(left_ext[0]),int(left_ext[1]))

            if not (0 <= pix[0] < width and 0 <= pix[1] < height):
                ("Out of bounds (left)")
                l = 1
                break

            if pixels[pix[0]+ width* (height-1-pix[1])] == 255:
                break
        
        if l==0 and r==0 :
            ans_x : tuple = (int(right_ext[0]),int(right_ext[1]))
            ans_y : tuple = (int(left_ext[0]),int(left_ext[1]))
            ans : tuple = (ans_x, ans_y)
            ribs.append(ans)
    
    #d2.opt
    #imizeRibs(ribs)
    return ribs
