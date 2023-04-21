from tptk_master.common.road_network import load_rn_shp
from tptk_master.common.trajectory import Trajectory, store_traj_file, parse_traj_file
from tptk_master.common.trajectory import STPoint
from tptk_master.noise_filtering import STFilter, HeuristicFilter
from tptk_master.segmentation import TimeIntervalSegmentation, StayPointSegmentation
from tptk_master.map_matching.hmm.hmm_map_matcher import TIHMMMapMatcher
from tptk_master.common.mbr import MBR
from datetime import datetime
import argparse
import os
from tqdm import tqdm

cleantraj_dir = "./data/trajdata_clean/"
mmtraj_dir = "./data/trajdata_mm/"
rn_dir = "./data/network_latest/"


def mm_tdrive(clean_traj_dir, mm_traj_dir, rn_path):
    rn = load_rn_shp(rn_path, is_directed=False)
    map_matcher = TIHMMMapMatcher(rn)
    for filename in tqdm(os.listdir(clean_traj_dir)):
        clean_trajs = parse_traj_file(os.path.join(clean_traj_dir, filename))
        mm_trajs = [map_matcher.match(clean_traj) for clean_traj in clean_trajs]
        store_traj_file(mm_trajs, os.path.join(mm_traj_dir, filename), traj_type='mm')


if __name__ == "__main__":
    mm_tdrive(cleantraj_dir, mmtraj_dir, rn_dir)
