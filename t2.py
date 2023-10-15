import cv2
import numpy as np

class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0
    def __eq__(self, __value: object) -> bool:
        return self.position == __value.position
    def __add__(self, __value: object):
        new_x = self.position[0] + __value.position[0]
        new_y = self.position[1] + __value.position[1]
        return Node((new_x, new_y),self) #自动继承结点


def astar(puzzel_map, start, end):
    open_list = []
    closed_list = []
    start_node = Node(start)
    end_node = Node(end)

    open_list.append(start_node)
    while open_list:
        current_node = min(open_list, key=lambda node: node.f)
        open_list.remove(current_node)
        closed_list.append(current_node)
        #log
        print(current_node.position, current_node.g, current_node.h, current_node.f)

        if current_node == end_node:
            path = []
            while current_node: #回溯路径
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1] #返回倒序
        
        #寻找四周节点
        dirctions = [Node((0, -1)), Node((0, 1)), Node((-1, 0)), Node((1, 0))]
        for dir_pos in dirctions:
            neighbor_node = current_node + dir_pos
            #边际条件1：边界
            if neighbor_node.position[0] > 14 or neighbor_node.position[0] < 0 or neighbor_node.position[1] > 14 or neighbor_node.position[1] < 0:
                continue
            #边际条件2：障碍
            if puzzel_map[neighbor_node.position[0]][neighbor_node.position[1]] == 1:
                continue
            #计算f值
            neighbor_node.g = current_node.g + 1
            neighbor_node.h = abs(neighbor_node.position[0] - end_node.position[0]) + abs(neighbor_node.position[1] - end_node.position[1])
            neighbor_node.f = neighbor_node.g + neighbor_node.h
            #检查并更新开放列表
            for open_node in open_list:
                if neighbor_node.position == open_node.position:
                    if neighbor_node.g > open_node.g:
                        continue
                    else:
                        open_list.remove(open_node)
            #检查并更新关闭列表
            for closed_node in closed_list:
                if neighbor_node.position == closed_node.position:
                    if neighbor_node.g > closed_node.g:
                        continue
                    else:
                        closed_list.remove(closed_node)
            open_list.append(neighbor_node)
    return None
            


def read_puzzel(image):
    '''
    读取迷宫地图
    0:空地
    1:墙
    '''
    puzzel_map = np.zeros((15,15),dtype=np.uint8) 
    h, w = image.shape[:2]
    h_step = h/15
    w_step = w/15
    for i in range(15):
        for j in range(15):
            color = image[round(i*h_step+0.5*h_step), round(j*w_step+0.5*w_step)]
            if np.linalg.norm(color-[0,0,0]) < 20:
                puzzel_map[i][j] = 1
            elif np.linalg.norm(color-[232,162,0]) < 20:
                start_node = (i, j)
            elif np.linalg.norm(color-[0,0,255]) < 20:
                end_node = (i, j)
    return puzzel_map, start_node, end_node

def draw_path(image, path):
    h, w = image.shape[:2]
    h_step = h/15
    w_step = w/15
    for node in path:
        circle_center = round(node[1]*h_step+0.5*h_step), round(node[0]*w_step+0.5*w_step)
        cv2.drawMarker(image,circle_center,(0,255,0),markerType=cv2.MARKER_STAR,markerSize=40)
    cv2.imshow("Image",image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == '__main__':
    # 读取图片
    image = cv2.imread('question_set/T2.png')
    maze, start_node, end_node = read_puzzel(image)
    print(maze, start_node, end_node)

    path = astar(maze, start_node, end_node)

    draw_path(image, path)


