# 构件规则（合成图纸的文字索引）
所有构件是轴对齐封闭长方体，标签不得省略。箱体参数顺序x,y,z,dx,dy,dz，单位mm。
Hall柱H_COL_ix_iy：ix=0..6，iy=0..4，(6000ix,5000iy,0,400,400,12000)。
Hall楼板H_SLAB_level：level=0..2，z=6000level，(0,0,z,36400,20400,250)。
每层楼板上的X梁H_BEAMX_level_ix_iy：ix=0..5,iy=0..4，(6000ix+400,5000iy,z+250,5600,400,500)。
Y梁H_BEAMY_level_ix_iy：ix=0..6,iy=0..3，(6000ix,5000iy+400,z+250,400,4600,500)。
H_NORTH_WALL：(0,20400,0,36400,250,12500)。
H_GLASS_ix：ix=0..11，(3000ix,0,500,2950,80,5500)。
Tower楼板T_SLAB_level：level=0..6，(42000,0,4000level,12400,10400,250)。
Tower柱T_COL_level_ix_iy：level=0..5,ix=0..2,iy=0..2，(42000+6000ix,5000iy,4000level+250,400,400,3750)。
Tower核心筒T_CORE_level：level=0..5，(46200,4000,4000level+250,4000,3000,3750)。
图纸和本索引共同构成权威尺寸。实体误差<=1mm；保留对象ID便于协调复核，OBJ使用o声明。
