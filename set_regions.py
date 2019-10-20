import os
import numpy as np
import cv2
from matplotlib.patches import Polygon
from matplotlib.widgets import PolygonSelector
from matplotlib.collections import PatchCollection
from shapely.geometry import box
from shapely.geometry import Polygon as shapely_poly
import pickle

points = []
prev_points = []
patches = []
total_points = []
breaker = False
class SelectFromCollection(object):
    def __init__(self, ax):
        self.canvas = ax.figure.canvas

        self.poly = PolygonSelector(ax, self.onselect)
        self.ind = []

    def onselect(self, verts):
        global points
        points = verts
        self.canvas.draw_idle()

    def disconnect(self):
        self.poly.disconnect_events()
        self.canvas.draw_idle()

def break_loop(event):
    global breaker
    if event.key == 'b':
        breaker = True

def onkeypress(event):
    global points, prev_points, total_points
    if event.key == 'n':    
        if points != prev_points and len(points) == 4:        
            patches.append(Polygon(np.array(points)))
            total_points.append(points)
            prev_points = points


if __name__ == '__main__':
    import matplotlib.pyplot as plt

    print("Select points in the figure by enclosing them within a polygon.")
    print("Press the 'esc' key to start a new polygon.")
    print("Try holding the 'shift' key to move all of the vertices.")
    print("Try holding the 'ctrl' key to move a single vertex.")
    
    video_capture = cv2.VideoCapture("parking1.mp4")
    cnt=0
    rgb_image = None
    while video_capture.isOpened():
        success, frame = video_capture.read()
        if not success:
            break
        if cnt == 5:
            rgb_image = frame[:, :, ::-1]
        cnt += 1
    video_capture.release()
    
    
    while True:
        fig, ax = plt.subplots()
        image = rgb_image
        ax.imshow(image)
    
        p = PatchCollection(patches, alpha=0.7)
        p.set_array(10*np.ones(len(patches)))
        ax.add_collection(p)
            
        selector = SelectFromCollection(ax)
        bbox = plt.connect('key_press_event', onkeypress)
        break_event = plt.connect('key_press_event', break_loop)
        plt.show()
        if breaker:
            break
        selector.disconnect()
    
# =============================================================================
#     print(total_points)
# =============================================================================
    if os.path.exists('parking_spaces.p'):
        os.remove('parking_spaces.p')
        
    with open('parking_spaces.p', 'wb') as f:
        pickle.dump(total_points, f, protocol=pickle.HIGHEST_PROTOCOL)
    
# =============================================================================
#     pol1_xy = total_points[0]
#     pol2_xy = total_points[1]
#     polygon1_shape = shapely_poly(pol1_xy)
#     polygon2_shape = shapely_poly(pol2_xy)
#     
#     # Calculate Intersection and union, and tne IOU
#     polygon_intersection = polygon1_shape.intersection(polygon2_shape).area
#     polygon_union = polygon1_shape.union(polygon2_shape).area
#     IOU = polygon_intersection / polygon_union
#     print("IOU is: ", IOU)
# =============================================================================
    
    
    
