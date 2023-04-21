import networkx as nx
from osgeo import ogr
from math import sin, cos, sqrt, atan2, radians
from tptk_master.common.spatial_func import distance, SPoint
from tptk_master.common.road_network import load_rn_shp

rn_dir = "./data/network_latest/"
traj_dir = './data/trajdata_mm/'
trajpath_dir = './data/trajdata_path/'
g = nx.read_shp(rn_dir, simplify=True, strict=False)
point_dict = {}  # 轨迹点=>边id

# 获得两个相邻轨迹点之间的路径
def get_path(last_node, now_node):
    eid_last_node = point_dict[last_node] # 获得两个轨迹点对应的边的id
    eid_now_node = point_dict[now_node]

    tmp_g = nx.read_shp(rn_dir, simplify=True, strict=False)
    for u, v, data in g.edges(data=True):
        if (data['eid'] == eid_last_node):
            # {lat,lng}
            point_u = SPoint(u[1], u[0])
            point_v = SPoint(v[1], v[0])
            point_last = SPoint(last_node[1], last_node[0])
            dis1 = distance(point_u, point_last)
            dis2 = distance(point_v, point_last)
            tmp_g.add_edge(u, last_node, attr_dict={'length': dis1})
            tmp_g.add_edge(last_node, u, attr_dict={'length': dis1})
            tmp_g.add_edge(last_node, v, attr_dict={'length': dis2})
            tmp_g.add_edge(v, last_node, attr_dict={'length': dis2})
        if (data['eid'] == eid_now_node):
            point_u = SPoint(u[1], u[0])
            point_v = SPoint(v[1], v[0])
            point_now = SPoint(last_node[1], now_node[0])
            dis1 = distance(point_u, point_now)
            dis2 = distance(point_v, point_now)
            tmp_g.add_edge(u, now_node, attr_dict={'length': dis1})
            tmp_g.add_edge(now_node, v, attr_dict={'length': dis2})
            tmp_g.add_edge(now_node, u, attr_dict={'length': dis1})
            tmp_g.add_edge(v, now_node, attr_dict={'length': dis2})
    path = []
    try:
        path = nx.shortest_path(tmp_g, source=last_node, target=now_node, weight='length')
    except nx.NetworkXNoPath:
        tmp1 = (now_node[0], now_node[1])
        tmp2 = (last_node[0], last_node[1])
        path.append(tmp2)
        path.append(tmp1)
    return path[1:]


def solve(traj_id):
    filename = traj_dir + str(traj_id) + '.txt'
    row_traj_list = []  # 原始的轨迹点列表
    res_traj_list = []  # 加入了路径的轨迹点列表
    # 获得轨迹id对应的轨迹 存在轨迹列表row_traj_list中
    with open(filename, 'r') as f:
        for line in f.readlines():
            attrs = line.rstrip().split(',')
            if attrs[0] == '#':
                pass
            else:
                if attrs[3] == 'None':
                    pass
                else:
                    eid = int(attrs[3])
                    proj_lat = float(attrs[4])
                    proj_lng = float(attrs[5])
                    row_traj_list.append((proj_lng, proj_lat))
                    point_dict[(proj_lng, proj_lat)] = eid
    f.close()


    last_node = row_traj_list[0]
    res_traj_list.append(last_node)
    # 利用get_path函数每次处理两个相邻的轨迹点 last_node now_node，获得路径
    for i in range(1, len(row_traj_list)):
        last_node = row_traj_list[i - 1]
        now_node = row_traj_list[i]
        ans = get_path(last_node, now_node)
        res_traj_list.extend(ans)
    return res_traj_list


if __name__ == '__main__':
    for u, v, data in g.edges(data=True):
        geom_line = ogr.CreateGeometryFromWkb(data['Wkb'])
        coords = []
        for i in range(geom_line.GetPointCount()):
            geom_pt = geom_line.GetPoint(i)
            coords.append(SPoint(geom_pt[1], geom_pt[0]))
        data['coords'] = coords
        data['length'] = sum([distance(coords[i], coords[i + 1]) for i in range(len(coords) - 1)])

    for i in range(0, 21877):
        print("solve trajid:",i)
        filename = trajpath_dir + str(i) +'.txt'
        ans = solve(i)
        with open(filename,'w') as f:
            for tmp in ans:
                f.write('{}\n'.format(tmp))

    # traj_id = 0
    # ans = solve(traj_id)
    # filename = trajpath_dir + str(traj_id) + '.txt'
    # with open(filename, 'w') as f:
    #     for tmp in ans:
    #         f.write('{}\n'.format(tmp))
