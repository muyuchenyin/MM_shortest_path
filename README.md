# 连续点的轨迹

## target

输出两个连续点之间的路径

## data

**路网范围**

> 'min_lat': 31.204398,
> 'min_lng': 121.465479,
> 'max_lat': 31.24151,
> 'max_lng': 121.51698,

**train_traj.json**

+ 整条轨迹ID：
+ + 轨迹点ID
  + 轨迹点坐标



## 步骤

+ 利用[osm2rn](https://github.com/sjruan/osm2rn)提取路网

+ > python osm_clip.py --input_path china-latest.osm.pbf --output_path region.osm.pbf --min_lat 31.204398 --min_lng 121.465479 --max_lat 31.24151 --max_lng 121.51698
  >
  > python osm_to_rn.py --input_path region.osm.pbf --output_path Shanghai

+ 处理轨迹数据

+ > python load trajdata.py
  >
  > python clean.py

+ 利用HMM进行地图匹配

+ > python get_mmtrajdata.py

+ 求连续点之间的路径

+ > python getpath.py



## 思路

