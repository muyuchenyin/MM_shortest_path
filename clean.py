# a tutorial example based on T-Drive dataset
from tptk_master.common.road_network import load_rn_shp
from tptk_master.common.trajectory import Trajectory, store_traj_file, parse_traj_file
from tptk_master.common.trajectory import STPoint
from tptk_master.noise_filtering import STFilter, HeuristicFilter
from tptk_master.segmentation import TimeIntervalSegmentation, StayPointSegmentation
from tptk_master.map_matching.hmm.hmm_map_matcher import TIHMMMapMatcher
from tptk_master.common.mbr import MBR
from datetime import datetime
import os
from tqdm import tqdm
import argparse
from tptk_master.statistics import statistics


def parse_tdrive(filename, tdrive_root_dir):
    oid = filename.replace('.txt', '')
    with open(os.path.join(tdrive_root_dir, filename), 'r') as f:
        pt_list = []
        for line in f.readlines():
            attrs = line.strip('\n').split(',')
            lat = float(attrs[3])
            lng = float(attrs[2])
            time = datetime.strptime(attrs[1], '%Y-%m-%d %H:%M:%S')
            pt_list.append(STPoint(lat, lng, time))
    if len(pt_list) > 1:
        return Trajectory(oid, 0, pt_list)
    else:
        return None


def do_clean(raw_traj, filters, segmentations):
    clean_traj = raw_traj
    for filter in filters:
        clean_traj = filter.filter(clean_traj)
        if clean_traj is None:
            return []
    clean_traj_list = [clean_traj]
    for seg in segmentations:
        tmp_clean_traj_list = []
        for clean_traj in clean_traj_list:
            segment_trajs = seg.segment(clean_traj)
            tmp_clean_traj_list.extend(segment_trajs)
        clean_traj_list = tmp_clean_traj_list
    return clean_traj_list


def clean_tdrive(tdrive_root_dir, clean_traj_dir):
    start_time = datetime(2008, 2, 2)
    end_time = datetime(2008, 2, 9)
    mbr = MBR(31.204398, 121.465479, 31.24151, 121.51698)
    st_filter = STFilter(mbr, start_time, end_time)
    heuristic_filter = HeuristicFilter(max_speed=35)
    filters = [st_filter, heuristic_filter]
    ti_seg = TimeIntervalSegmentation(max_time_interval_min=6)
    sp_seg = StayPointSegmentation(dist_thresh_meter=100, max_stay_time_min=15)
    segs = [ti_seg, sp_seg]
    for filename in tqdm(os.listdir(tdrive_root_dir)):
        raw_traj = parse_tdrive(filename, tdrive_root_dir)
        if raw_traj is None:
            continue
        clean_trajs = do_clean(raw_traj, filters, segs)
        if len(clean_trajs) > 0:
            store_traj_file(clean_trajs, os.path.join(clean_traj_dir, filename))

if __name__ == '__main__':
    root_dir = './data/trajdata_row'
    clean_dir = './data/trajdata_clean'
    clean_tdrive(root_dir, clean_dir)
