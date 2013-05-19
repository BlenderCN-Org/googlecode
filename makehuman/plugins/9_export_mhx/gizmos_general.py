#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makeinfo.human.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Thomas Larsson

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makeinfo.human.org/node/318)

**Coding Standards:**  See http://www.makeinfo.human.org/node/165

Abstract
--------

Gizmos used by mhx and rigify rig
"""

def asString():
    return(

"""
# ----------------------------- MESH --------------------- # 

Mesh GZM_Jaw GZM_Jaw 
  Verts
    v 0.529 0.764 -0.325 ;
    v 0.666 0.259 -0.067 ;
    v 0.584 0.677 0.169 ;
    v 0.023 1.154 0.097 ;
    v -0.615 0.713 0.203 ;
    v -0.697 0.295 -0.033 ;
    v -0.482 0.764 -0.325 ;
    v 0.023 1.048 -0.439 ;
  end Verts
  Edges
    e 4 5 ;
    e 5 6 ;
    e 6 7 ;
    e 0 7 ;
    e 0 1 ;
    e 1 2 ;
    e 2 3 ;
    e 3 4 ;
  end Edges
end Mesh

Object GZM_Jaw MESH GZM_Jaw
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
    Modifier Subsurf SUBSURF
      levels 2 ;
      render_levels 2 ;
      subdivision_type 'CATMULL_CLARK' ;
      use_subsurf_uv True ;
    end Modifier
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_Head GZM_Head 
 Verts
    v -0.714 -0.056 -0.552 ;
    v -0.000 0.131 -1.040 ;
    v 0.714 -0.056 -0.552 ;
    v 0.886 0.028 -0.007 ;
    v 0.877 0.701 0.737 ;
    v -0.000 1.780 1.056 ;
    v -0.877 0.701 0.737 ;
    v -0.886 0.028 -0.007 ;
  end Verts
  Edges
    e 4 5 ;
    e 5 6 ;
    e 6 7 ;
    e 0 7 ;
    e 0 1 ;
    e 1 2 ;
    e 2 3 ;
    e 3 4 ;
  end Edges
end Mesh

Object GZM_Head MESH GZM_Head
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
    Modifier Subsurf SUBSURF
      levels 2 ;
      render_levels 2 ;
      subdivision_type 'CATMULL_CLARK' ;
      use_subsurf_uv True ;
    end Modifier
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_Shoulder GZM_Shoulder 
  Verts
    v 0.036 1.000 -0.036 ;
    v 0.080 0.000 -0.080 ;
    v -0.080 0.000 -0.080 ;
    v -0.036 1.000 -0.036 ;
    v 0.036 1.000 0.036 ;
    v 0.080 -0.000 0.080 ;
    v -0.080 0.000 0.080 ;
    v -0.036 1.000 0.036 ;
  end Verts
  Edges
    e 1 2 ;
    e 0 1 ;
    e 0 3 ;
    e 2 3 ;
    e 4 5 ;
    e 5 6 ;
    e 6 7 ;
    e 4 7 ;
    e 1 5 ;
    e 0 4 ;
    e 2 6 ;
    e 3 7 ;
  end Edges
end Mesh

Object GZM_Shoulder MESH GZM_Shoulder
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_Hand GZM_Hand 
  Verts
    v 0.296403 0.132076 0.444902 ;
    v 0.296403 1.14172 0.402842 ;
    v -0.296403 1.14172 0.402842 ;
    v -0.296403 0.132076 0.444902 ;
    v 0.296403 0.132076 -0.529527 ;
    v 0.296403 1.14172 -0.614674 ;
    v -0.296403 1.14172 -0.614674 ;
    v -0.296403 0.132076 -0.529527 ;
  end Verts
  Faces
    f 0 1 2 3 ;
    f 4 7 6 5 ;
    f 0 4 5 1 ;
    f 1 5 6 2 ;
    f 2 6 7 3 ;
    f 4 0 3 7 ;
  end Faces
end Mesh

Object GZM_Hand MESH GZM_Hand
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_Neck GZM_Neck 
  Verts
    v -0.563 0.492 -0.466 ;
    v 0.000 0.132 -0.806 ;
    v 0.563 0.492 -0.466 ;
    v 0.797 0.812 0.247 ;
    v 0.563 0.479 0.987 ;
    v 0.000 0.212 1.310 ;
    v -0.563 0.479 0.987 ;
    v -0.797 0.812 0.247 ;
  end Verts
  Edges
    e 4 5 ;
    e 5 6 ;
    e 6 7 ;
    e 0 7 ;
    e 0 1 ;
    e 1 2 ;
    e 2 3 ;
    e 3 4 ;
  end Edges
end Mesh

Object GZM_Neck MESH GZM_Neck
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
    Modifier Subsurf SUBSURF
      levels 2 ;
      render_levels 2 ;
      subdivision_type 'CATMULL_CLARK' ;
      use_subsurf_uv True ;
    end Modifier
  parent Refer Object CustomShapes ;
end Object


# ----------------------------- MESH --------------------- # 

Mesh GZM_Master GZM_Master 
  Verts
    v 3.00451 3.95367 -2.4557e-07 ;
    v 4.24903 0.949164 0 ;
    v 3.00451 -2.05536 0 ;
    v -2.03413e-07 -3.29987 2.4557e-07 ;
    v -3.00451 -2.05536 0 ;
    v -4.24903 0.949164 0 ;
    v -3.00451 3.95367 -2.4557e-07 ;
    v -1.11512e-06 5.19819 0 ;
    v -2.03413e-07 -3.831 0 ;
    v 0.531128 -3.29987 2.4557e-07 ;
    v -0.531128 -3.29987 2.4557e-07 ;
    v 0.531128 -3.29987 2.4557e-07 ;
    v -0.531128 -3.29987 2.4557e-07 ;
    v -2.03415e-07 -3.831 0 ;
    v -2.03415e-07 -3.831 0 ;
    v 0.531128 -3.29987 2.4557e-07 ;
    v -0.531128 -3.29987 2.4557e-07 ;
  end Verts
  Edges
    e 0 1 ;
    e 1 2 ;
    e 2 3 ;
    e 3 4 ;
    e 4 5 ;
    e 5 6 ;
    e 6 7 ;
    e 0 7 ;
    e 9 11 ;
    e 10 12 ;
    e 8 13 ;
    e 8 14 ;
    e 11 14 ;
    e 9 15 ;
    e 12 15 ;
    e 10 16 ;
    e 13 16 ;
  end Edges
end Mesh

Object GZM_Master MESH GZM_Master
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
    Modifier Subsurf SUBSURF
      levels 2 ;
      render_levels 2 ;
      subdivision_type 'CATMULL_CLARK' ;
      use_subsurf_uv True ;
    end Modifier
  parent Refer Object CustomShapes ;
end Object 

# ----------------------------- MESH --------------------- # 

Mesh GZM_Gaze GZM_Gaze 
  Verts
    v -0.000 0 -0.126 ;
    v -0.048 0 -0.117 ;
    v -0.089 0 -0.089 ;
    v -0.117 0 -0.048 ;
    v -0.126 0 0.000 ;
    v -0.117 0 0.048 ;
    v -0.089 0 0.089 ;
    v -0.048 0 0.117 ;
    v -0.000 0 0.126 ;
    v 0.048 0 0.117 ;
    v 0.089 0 0.089 ;
    v 0.117 0 0.048 ;
    v 0.126 0 -0.000 ;
    v 0.117 0 -0.048 ;
    v 0.089 0 -0.089 ;
    v 0.048 0 -0.117 ;
    v -0.000 0 -0.142 ;
    v -0.116 0 -0.132 ;
    v -0.214 0 -0.082 ;
    v -0.279 0 -0.033 ;
    v -0.302 0 0.000 ;
    v -0.279 0 0.033 ;
    v -0.214 0 0.082 ;
    v -0.116 0 0.132 ;
    v -0.000 0 0.142 ;
    v 0.116 0 0.132 ;
    v 0.214 0 0.082 ;
    v 0.279 0 0.033 ;
    v 0.302 0 -0.000 ;
    v 0.279 0 -0.033 ;
    v 0.214 0 -0.082 ;
    v 0.116 0 -0.132 ;
  end Verts
  Edges
    e 1 0 ;
    e 2 1 ;
    e 3 2 ;
    e 4 3 ;
    e 5 4 ;
    e 6 5 ;
    e 7 6 ;
    e 8 7 ;
    e 9 8 ;
    e 10 9 ;
    e 11 10 ;
    e 12 11 ;
    e 13 12 ;
    e 14 13 ;
    e 15 14 ;
    e 15 0 ;
    e 17 16 ;
    e 18 17 ;
    e 19 18 ;
    e 20 19 ;
    e 21 20 ;
    e 22 21 ;
    e 23 22 ;
    e 24 23 ;
    e 25 24 ;
    e 26 25 ;
    e 27 26 ;
    e 28 27 ;
    e 29 28 ;
    e 30 29 ;
    e 31 30 ;
    e 31 16 ;
  end Edges
end Mesh

Object GZM_Gaze MESH GZM_Gaze
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_Crown GZM_Crown 
  Verts
    v -0.000 1.200 -2.000 ;
    v 0.390 1.200 -1.962 ;
    v 0.765 0.800 -1.848 ;
    v 1.111 0.800 -1.663 ;
    v 1.414 1.200 -1.414 ;
    v 1.663 1.200 -1.111 ;
    v 1.848 0.800 -0.765 ;
    v 1.962 0.800 -0.390 ;
    v 2.000 1.200 0.000 ;
    v 1.962 1.200 0.390 ;
    v 1.848 0.800 0.765 ;
    v 1.663 0.800 1.111 ;
    v 1.414 1.200 1.414 ;
    v 1.111 1.200 1.663 ;
    v 0.765 0.800 1.848 ;
    v 0.390 0.800 1.962 ;
    v -0.000 1.200 2.000 ;
    v -0.390 1.200 1.962 ;
    v -0.765 0.800 1.848 ;
    v -1.111 0.800 1.663 ;
    v -1.414 1.200 1.414 ;
    v -1.663 1.200 1.111 ;
    v -1.848 0.800 0.765 ;
    v -1.962 0.800 0.390 ;
    v -2.000 1.200 -0.000 ;
    v -1.962 1.200 -0.390 ;
    v -1.848 0.800 -0.765 ;
    v -1.663 0.800 -1.111 ;
    v -1.414 1.200 -1.414 ;
    v -1.111 1.200 -1.663 ;
    v -0.765 0.800 -1.848 ;
    v -0.390 0.800 -1.962 ;
  end Verts
  Edges
    e 0 1 ;
    e 1 2 ;
    e 2 3 ;
    e 3 4 ;
    e 4 5 ;
    e 5 6 ;
    e 6 7 ;
    e 7 8 ;
    e 8 9 ;
    e 9 10 ;
    e 10 11 ;
    e 11 12 ;
    e 12 13 ;
    e 13 14 ;
    e 14 15 ;
    e 15 16 ;
    e 16 17 ;
    e 17 18 ;
    e 18 19 ;
    e 19 20 ;
    e 20 21 ;
    e 21 22 ;
    e 22 23 ;
    e 23 24 ;
    e 24 25 ;
    e 25 26 ;
    e 26 27 ;
    e 27 28 ;
    e 28 29 ;
    e 29 30 ;
    e 30 31 ;
    e 0 31 ;
  end Edges
end Mesh

Object GZM_Crown MESH GZM_Crown
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_Foot GZM_Foot 
  Verts
    v 0.253 0.014 0.224 ;
    v 0.253 0.834 0.347 ;
    v -0.291 0.833 0.348 ;
    v -0.290 0.014 0.224 ;
    v 0.253 0.324 -0.514 ;
    v 0.252 1.040 -0.099 ;
    v -0.291 1.040 -0.099 ;
    v -0.291 0.324 -0.513 ;
  end Verts
  Faces
    f 0 1 2 3 ;
    f 4 7 6 5 ;
    f 0 4 5 1 ;
    f 1 5 6 2 ;
    f 2 6 7 3 ;
    f 4 0 3 7 ;
  end Faces
end Mesh

Object GZM_Foot MESH GZM_Foot
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_Toe_L GZM_Toe_L
  Verts
    v -0.573 -0.005 -0.195 ;
    v -0.526 1.258 -0.151 ;
    v 0.392 1.256 -0.157 ;
    v 0.346 -0.001 -0.198 ;
    v -0.467 0.067 0.596 ;
    v -0.462 1.301 0.322 ;
    v 0.457 1.287 0.322 ;
    v 0.452 0.066 0.598 ;
  end Verts
  Faces
    f 0 1 2 3 ;
    f 4 7 6 5 ;
    f 0 4 5 1 ;
    f 1 5 6 2 ;
    f 2 6 7 3 ;
    f 4 0 3 7 ;
  end Faces
end Mesh

Object GZM_Toe_L MESH GZM_Toe_L
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_Toe_R GZM_Toe_R
  Verts
    v -0.367 -0.000 -0.192 ;
    v -0.418 1.255 -0.163 ;
    v 0.502 1.253 -0.164 ;
    v 0.553 0.010 -0.204 ;
    v -0.462 0.063 0.593 ;
    v -0.477 1.282 0.303 ;
    v 0.443 1.292 0.312 ;
    v 0.457 0.060 0.593 ;
  end Verts
  Faces
    f 0 1 2 3 ;
    f 4 7 6 5 ;
    f 0 4 5 1 ;
    f 1 5 6 2 ;
    f 2 6 7 3 ;
    f 4 0 3 7 ;
  end Faces
end Mesh

Object GZM_Toe_R MESH GZM_Toe_R
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_Circle_FK_Hip GZM_Circle_FK_Hip 
  Verts
    v 0.907 0.323 0.980 ;
    v 1.282 0.323 0.073 ;
    v 0.907 0.323 -0.833 ;
    v -0.000 0.323 -1.209 ;
    v -0.907 0.323 -0.833 ;
    v -1.282 0.323 0.073 ;
    v -0.907 0.323 0.980 ;
    v -0.000 0.323 1.356 ;
    v -0.000 0.323 1.454 ;
    v -0.379 0.323 1.297 ;
    v 0.379 0.323 1.297 ;
    v 0.013 0.323 1.449 ;
    v 0.366 0.323 1.303 ;
    v -0.013 0.323 1.449 ;
    v -0.366 0.323 1.303 ;
    v -0.363 0.323 1.297 ;
    v 0.363 0.323 1.297 ;
    v 1.239 0.323 1.260 ;
    v 1.239 0.323 -1.217 ;
    v -1.239 0.323 -1.217 ;
    v -1.239 0.323 1.260 ;
    v 1.239 0.323 -1.176 ;
    v 1.239 0.323 1.219 ;
    v -1.239 0.323 1.219 ;
    v -1.239 0.323 -1.176 ;
    v 1.197 0.323 -1.217 ;
    v -1.197 0.323 -1.217 ;
    v 1.197 0.323 1.260 ;
    v -1.197 0.323 1.260 ;
    v -0.000 0.323 1.297 ;
  end Verts
  Faces
    f 9 14 15 ;
    f 10 16 12 ;
    f 8 11 13 ;
    f 11 29 13 ;
    f 13 29 15 14 ;
    f 11 12 16 29 ;
  end Faces
end Mesh

Object GZM_Circle_FK_Hip MESH GZM_Circle_FK_Hip
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
    Modifier Subsurf SUBSURF
      levels 2 ;
    end Modifier
  hide False ;
  hide_select False ;
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_Ball GZM_Ball 
  Verts
    v 0.283 2.255 -5.008 ;
    v 0.283 1.741 -5.246 ;
    v 0 1.635 -5.295 ;
    v -0.283 1.741 -5.246 ;
    v -0.283 2.255 -5.008 ;
    v 0 2.361 -4.959 ;
    v 0 2.374 -5.265 ;
    v 0 2.166 -5.490 ;
    v 0 1.860 -5.503 ;
    v 0 1.622 -4.989 ;
    v 0 2.136 -4.751 ;
    v -0.283 1.879 -4.870 ;
    v 0 1.830 -4.764 ;
    v 0.283 1.879 -4.870 ;
    v 0.400 1.998 -5.127 ;
    v 0.283 2.117 -5.384 ;
    v -0.283 2.117 -5.384 ;
    v -0.400 1.998 -5.127 ;
    v 0 0.500 0 ;
    v 0 0.500 0 ;
    v 0 0.500 0 ;
    v 0 0.500 0 ;
    v 0 0.500 0 ;
    v 0.020 1.783 -4.618 ;
    v 0.020 1.797 -4.602 ;
    v 0.020 1.818 -4.601 ;
    v 0.040 1.801 -4.609 ;
  end Verts
  Edges
    e 1 2 ;
    e 2 3 ;
    e 5 10 ;
    e 5 6 ;
    e 6 7 ;
    e 7 8 ;
    e 11 12 ;
    e 12 13 ;
    e 13 14 ;
    e 14 15 ;
    e 16 17 ;
    e 11 17 ;
    e 7 16 ;
    e 7 15 ;
    e 10 12 ;
    e 9 12 ;
    e 2 9 ;
    e 2 8 ;
    e 0 5 ;
    e 4 5 ;
    e 4 17 ;
    e 3 17 ;
    e 1 14 ;
    e 0 14 ;
    e 12 18 ;
    e 20 22 ;
    e 20 21 ;
    e 19 20 ;
    e 9 23 ;
    e 22 23 ;
    e 12 24 ;
    e 20 24 ;
    e 10 25 ;
    e 21 25 ;
    e 13 26 ;
    e 19 26 ;
  end Edges
end Mesh

Object GZM_Ball MESH GZM_Ball
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
    Modifier Subsurf SUBSURF
      levels 2 ;
    end Modifier
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_IKBall GZM_IKBall 
  Verts
    v 0.0848528 0.0848528 5.96046e-08 ;
    v -1.86068e-09 -0.12 5.96046e-08 ;
    v -0.0848528 0.0848528 5.96046e-08 ;
    v 1.9537e-09 -1.03039e-09 -0.12 ;
    v -1.9537e-09 -0.0848528 -0.0848528 ;
    v -5.19885e-09 0.0848528 0.0848529 ;
    v -6.11328e-09 1.08103e-08 0.12 ;
    v -0.12 -5.50651e-09 5.96046e-08 ;
    v -0.0848528 -1.26591e-08 -0.0848528 ;
    v 0.0848528 -1.26591e-08 -0.0848528 ;
    v 0.12 -5.50651e-09 5.96046e-08 ;
    v 0.0848528 1.64605e-09 0.0848529 ;
    v -0.0848528 1.64605e-09 0.0848529 ;
    v -1.23514e-08 -0.0848528 0.0848529 ;
    v -1.9537e-09 0.0848528 -0.0848528 ;
    v -1.97353e-10 0.12 5.96046e-08 ;
    v -0.0848528 -0.0848528 5.96046e-08 ;
    v 0.0848528 -0.0848528 5.96046e-08 ;
  end Verts
  Edges
    e 3 4 ;
    e 5 6 ;
    e 1 4 ;
    e 2 7 ;
    e 17 10 ;
    e 9 10 ;
    e 11 10 ;
    e 14 15 ;
    e 17 1 ;
    e 16 1 ;
    e 15 5 ;
    e 14 3 ;
    e 6 12 ;
    e 6 11 ;
    e 7 8 ;
    e 7 12 ;
    e 3 8 ;
    e 3 9 ;
    e 6 13 ;
    e 1 13 ;
    e 15 0 ;
    e 15 2 ;
    e 16 7 ;
    e 0 10 ;
  end Edges
end Mesh

Object GZM_IKBall MESH GZM_IKBall
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
    Modifier Subsurf SUBSURF
      levels 2 ;
    end Modifier
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_Eyes GZM_Eyes 
  Verts
    v 0.74286 -0.54515 5.96046e-08 ;
    v 1.17834 3.03283e-08 -3.90061e-09 ;
    v 0.74286 0.54515 -5.96046e-08 ;
    v -7.72164e-08 0.280699 -5.96046e-08 ;
    v -0.74286 0.54515 -5.96046e-08 ;
    v -1.17834 3.03283e-08 -3.90061e-09 ;
    v -0.74286 -0.54515 5.96046e-08 ;
    v -2.13531e-07 -0.280699 5.96046e-08 ;
    v 1.09994 -0.272575 2.98023e-08 ;
    v 1.09994 0.272575 -5.96046e-08 ;
    v 0.305346 0.386941 -8.9407e-08 ;
    v -0.305346 0.386941 -8.9407e-08 ;
    v -1.09994 0.272575 -5.96046e-08 ;
    v -1.09994 -0.272575 2.98023e-08 ;
    v -0.305345 -0.386941 5.96046e-08 ;
    v 0.305345 -0.386941 5.96046e-08 ;
  end Verts
  Edges
    e 0 8 ;
    e 1 8 ;
    e 1 9 ;
    e 2 9 ;
    e 2 10 ;
    e 3 10 ;
    e 3 11 ;
    e 4 11 ;
    e 4 12 ;
    e 5 12 ;
    e 5 13 ;
    e 6 13 ;
    e 6 14 ;
    e 7 14 ;
    e 0 15 ;
    e 7 15 ;
  end Edges
end Mesh

Object GZM_Eyes MESH GZM_Eyes
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
    Modifier Subsurf SUBSURF
      levels 2 ;
    end Modifier
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_CircleSpine GZM_CircleSpine 
  Verts
    v 1.096 0.317 -0.194 ;
    v 1.096 0.165 0.702 ;
    v 0.454 0.012 1.325 ;
    v -0.454 0.039 1.332 ;
    v -1.096 0.139 0.696 ;
    v -1.096 0.344 -0.188 ;
    v -0.454 0.443 -0.824 ;
    v 0.454 0.470 -0.817 ;
    v 0.161 -0.024 1.509 ;
    v -0.161 -0.024 1.509 ;
    v 0.000 -0.056 1.667 ;
    v 0.000 -0.056 1.667 ;
    v 0.080 -0.040 1.588 ;
    v 0.161 -0.024 1.509 ;
    v 0.000 -0.024 1.509 ;
    v -0.161 -0.024 1.509 ;
    v -0.080 -0.040 1.588 ;
    v 0.841 0.420 -0.567 ;
    v 1.190 0.228 0.250 ;
    v 0.841 0.089 1.082 ;
    v 0.000 -0.006 1.417 ;
    v -0.841 0.089 1.082 ;
    v -1.190 0.228 0.250 ;
    v -0.841 0.420 -0.567 ;
    v 0.000 0.461 -0.916 ;
    v 0.000 -0.056 1.667 ;
    v 0.161 -0.024 1.509 ;
    v -0.161 -0.024 1.509 ;
    v 0.141 -0.028 1.529 ;
    v -0.121 -0.024 1.509 ;
    v -0.020 -0.052 1.647 ;
    v 0.020 -0.052 1.647 ;
    v 0.121 -0.024 1.509 ;
    v -0.141 -0.028 1.529 ;
  end Verts
  Edges
    e 0 17 ;
    e 0 18 ;
    e 1 18 ;
    e 1 19 ;
    e 2 19 ;
    e 2 20 ;
    e 3 20 ;
    e 3 21 ;
    e 4 21 ;
    e 4 22 ;
    e 5 22 ;
    e 5 23 ;
    e 6 23 ;
    e 6 24 ;
    e 7 17 ;
    e 7 24 ;
    e 8 26 ;
    e 8 28 ;
    e 9 27 ;
    e 9 29 ;
    e 10 25 ;
    e 10 30 ;
    e 11 25 ;
    e 11 31 ;
    e 12 28 ;
    e 12 31 ;
    e 13 26 ;
    e 13 32 ;
    e 14 29 ;
    e 14 32 ;
    e 15 27 ;
    e 15 33 ;
    e 16 30 ;
    e 16 33 ;
  end Edges
end Mesh

Object GZM_CircleSpine MESH GZM_CircleSpine
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_CircleChest GZM_CircleChest 
  Verts
    v 0.900 0.106 -0.049 ;
    v 0.900 0.346 0.652 ;
    v 0.373 0.573 1.134 ;
    v -0.373 0.540 1.142 ;
    v -0.900 0.379 0.644 ;
    v -0.900 0.073 -0.041 ;
    v -0.373 -0.088 -0.539 ;
    v 0.373 -0.120 -0.531 ;
    v 0.396 0.597 1.230 ;
    v -0.396 0.597 1.230 ;
    v 0.000 0.741 1.596 ;
    v 0.000 0.741 1.596 ;
    v 0.198 0.669 1.413 ;
    v 0.396 0.597 1.230 ;
    v 0.000 0.597 1.230 ;
    v -0.396 0.597 1.230 ;
    v -0.198 0.669 1.413 ;
    v 0.691 -0.044 -0.337 ;
    v 0.977 0.242 0.298 ;
    v 0.691 0.463 0.948 ;
    v 0.000 0.601 1.206 ;
    v -0.691 0.463 0.948 ;
    v -0.977 0.242 0.298 ;
    v -0.691 -0.044 -0.337 ;
    v 0.000 -0.116 -0.611 ;
    v 0.000 0.741 1.596 ;
    v 0.396 0.597 1.230 ;
    v -0.396 0.597 1.230 ;
    v 0.348 0.615 1.275 ;
    v -0.297 0.597 1.230 ;
    v -0.048 0.723 1.551 ;
    v 0.048 0.723 1.551 ;
    v 0.297 0.597 1.230 ;
    v -0.348 0.615 1.275 ;
  end Verts
  Edges
    e 0 17 ;
    e 0 18 ;
    e 1 18 ;
    e 1 19 ;
    e 2 19 ;
    e 2 20 ;
    e 3 20 ;
    e 3 21 ;
    e 4 21 ;
    e 4 22 ;
    e 5 22 ;
    e 5 23 ;
    e 6 23 ;
    e 6 24 ;
    e 7 17 ;
    e 7 24 ;
    e 8 26 ;
    e 8 28 ;
    e 9 27 ;
    e 9 29 ;
    e 10 25 ;
    e 10 30 ;
    e 11 25 ;
    e 11 31 ;
    e 12 28 ;
    e 12 31 ;
    e 13 26 ;
    e 13 32 ;
    e 14 29 ;
    e 14 32 ;
    e 15 27 ;
    e 15 33 ;
    e 16 30 ;
    e 16 33 ;
  end Edges
end Mesh

Object GZM_CircleChest MESH GZM_CircleChest
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_CircleHips GZM_CircleHips
  Verts
    v -1.935 0.989 0.919 ;
    v -1.935 0.929 -0.249 ;
    v -0.802 0.989 -1.076 ;
    v 0.802 0.929 -1.076 ;
    v 1.935 0.989 -0.249 ;
    v 1.935 0.989 0.919 ;
    v 0.802 0.929 1.744 ;
    v -0.802 0.929 1.744 ;
    v -0.855 0.989 -1.229 ;
    v 0.855 0.989 -1.229 ;
    v -0.000 0.989 -1.847 ;
    v -0.000 0.989 -1.847 ;
    v -0.426 0.989 -1.538 ;
    v -0.855 0.989 -1.229 ;
    v -0.000 0.989 -1.229 ;
    v 0.855 0.989 -1.229 ;
    v 0.426 0.989 -1.538 ;
    v -1.486 0.929 1.417 ;
    v -2.102 0.989 0.335 ;
    v -1.486 0.929 -0.748 ;
    v 0.000 0.989 -1.196 ;
    v 1.486 0.929 -0.748 ;
    v 2.102 0.989 0.335 ;
    v 1.486 0.929 1.417 ;
    v 0.000 0.989 1.866 ;
    v -0.000 0.989 -1.847 ;
    v -0.855 0.989 -1.229 ;
    v 0.855 0.989 -1.229 ;
    v -0.747 0.989 -1.307 ;
    v 0.642 0.989 -1.229 ;
    v 0.108 0.989 -1.769 ;
    v -0.108 0.989 -1.769 ;
    v -0.642 0.989 -1.229 ;
    v 0.747 0.989 -1.307 ;
  end Verts
  Edges
    e 0 17 ;
    e 0 18 ;
    e 1 18 ;
    e 1 19 ;
    e 2 19 ;
    e 2 20 ;
    e 3 20 ;
    e 3 21 ;
    e 4 21 ;
    e 4 22 ;
    e 5 22 ;
    e 5 23 ;
    e 6 23 ;
    e 6 24 ;
    e 7 17 ;
    e 7 24 ;
    e 8 26 ;
    e 8 28 ;
    e 9 27 ;
    e 9 29 ;
    e 10 25 ;
    e 10 30 ;
    e 11 25 ;
    e 11 31 ;
    e 12 28 ;
    e 12 31 ;
    e 13 26 ;
    e 13 32 ;
    e 14 29 ;
    e 14 32 ;
    e 15 27 ;
    e 15 33 ;
    e 16 30 ;
    e 16 33 ;
  end Edges
end Mesh

Object GZM_CircleHips MESH GZM_CircleHips
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_CircleInvChest GZM_CircleInvChest 
  Verts
    v -0.899 0.910 0.091 ;
    v -0.899 0.611 -0.587 ;
    v -0.372 0.449 -1.095 ;
    v 0.373 0.420 -1.078 ;
    v 0.900 0.640 -0.604 ;
    v 0.900 0.881 0.107 ;
    v 0.372 1.101 0.582 ;
    v -0.373 1.071 0.598 ;
    v -0.396 0.424 -1.177 ;
    v 0.396 0.424 -1.177 ;
    v -0.000 0.283 -1.543 ;
    v -0.000 0.283 -1.543 ;
    v -0.198 0.352 -1.360 ;
    v -0.396 0.424 -1.177 ;
    v -0.000 0.424 -1.177 ;
    v 0.396 0.424 -1.177 ;
    v 0.198 0.352 -1.360 ;
    v -0.691 0.996 0.404 ;
    v -0.977 0.775 -0.257 ;
    v -0.690 0.496 -0.884 ;
    v 0.000 0.421 -1.167 ;
    v 0.691 0.496 -0.884 ;
    v 0.977 0.775 -0.257 ;
    v 0.690 0.996 0.404 ;
    v -0.000 1.129 0.654 ;
    v -0.000 0.283 -1.543 ;
    v -0.396 0.424 -1.177 ;
    v 0.396 0.424 -1.177 ;
    v -0.345 0.406 -1.222 ;
    v 0.297 0.424 -1.177 ;
    v 0.051 0.301 -1.498 ;
    v -0.048 0.301 -1.498 ;
    v -0.297 0.424 -1.177 ;
    v 0.348 0.406 -1.222 ;
  end Verts
  Edges
    e 0 17 ;
    e 0 18 ;
    e 1 18 ;
    e 1 19 ;
    e 2 19 ;
    e 2 20 ;
    e 3 20 ;
    e 3 21 ;
    e 4 21 ;
    e 4 22 ;
    e 5 22 ;
    e 5 23 ;
    e 6 23 ;
    e 6 24 ;
    e 7 17 ;
    e 7 24 ;
    e 8 26 ;
    e 8 28 ;
    e 9 27 ;
    e 9 29 ;
    e 10 25 ;
    e 10 30 ;
    e 11 25 ;
    e 11 31 ;
    e 12 28 ;
    e 12 31 ;
    e 13 26 ;
    e 13 32 ;
    e 14 29 ;
    e 14 32 ;
    e 15 27 ;
    e 15 33 ;
    e 16 30 ;
    e 16 33 ;
  end Edges
end Mesh

Object GZM_CircleInvChest MESH GZM_CircleInvChest
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
  parent Refer Object CustomShapes ;
end Object


# ----------------------------- MESH --------------------- # 

Mesh GZM_CircleInvSpine GZM_CircleInvSpine 
  Verts
    v -1.096 0.721 0.160 ;
    v -1.096 0.871 -0.737 ;
    v -0.454 0.930 -1.376 ;
    v 0.454 0.958 -1.373 ;
    v 1.096 0.843 -0.740 ;
    v 1.096 0.748 0.162 ;
    v 0.454 0.633 0.796 ;
    v -0.454 0.661 0.798 ;
    v -0.483 0.942 -1.456 ;
    v 0.483 0.942 -1.456 ;
    v -0.000 1.005 -1.933 ;
    v -0.000 1.005 -1.933 ;
    v -0.240 0.975 -1.693 ;
    v -0.483 0.942 -1.456 ;
    v -0.000 0.942 -1.456 ;
    v 0.483 0.942 -1.456 ;
    v 0.243 0.975 -1.693 ;
    v -0.842 0.695 0.546 ;
    v -1.190 0.782 -0.290 ;
    v -0.841 0.923 -1.121 ;
    v 0.000 0.943 -1.469 ;
    v 0.841 0.923 -1.121 ;
    v 1.190 0.782 -0.290 ;
    v 0.841 0.695 0.546 ;
    v -0.000 0.621 0.889 ;
    v -0.000 1.005 -1.933 ;
    v -0.483 0.942 -1.456 ;
    v 0.483 0.942 -1.456 ;
    v -0.423 0.951 -1.516 ;
    v 0.363 0.942 -1.456 ;
    v 0.060 0.999 -1.873 ;
    v -0.060 0.999 -1.873 ;
    v -0.363 0.942 -1.456 ;
    v 0.423 0.951 -1.516 ;
  end Verts
  Edges
    e 0 17 ;
    e 0 18 ;
    e 1 18 ;
    e 1 19 ;
    e 2 19 ;
    e 2 20 ;
    e 3 20 ;
    e 3 21 ;
    e 4 21 ;
    e 4 22 ;
    e 5 22 ;
    e 5 23 ;
    e 6 23 ;
    e 6 24 ;
    e 7 17 ;
    e 7 24 ;
    e 8 26 ;
    e 8 28 ;
    e 9 27 ;
    e 9 29 ;
    e 10 25 ;
    e 10 30 ;
    e 11 25 ;
    e 11 31 ;
    e 12 28 ;
    e 12 31 ;
    e 13 26 ;
    e 13 32 ;
    e 14 29 ;
    e 14 32 ;
    e 15 27 ;
    e 15 33 ;
    e 16 30 ;
    e 16 33 ;
  end Edges
end Mesh

Object GZM_CircleInvSpine MESH GZM_CircleInvSpine
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
  parent Refer Object CustomShapes ;
end Object

# ----------------------------- MESH --------------------- # 

Mesh GZM_IK_Hips GZM_IK_Hips
  Verts
    v 0 0.942 0.888 ;
    v 0 -0.848 1.515 ;
    v 0 1.079 1.515 ;
    v 0 0.115 2.479 ;
    v 0 -0.206 1.515 ;
    v 0 0.436 1.515 ;
    v 0 1.062 1.532 ;
    v 0 0.132 2.462 ;
    v 0 -0.832 1.532 ;
    v 0 0.099 2.462 ;
    v 0 -0.826 1.515 ;
    v 0 -0.228 1.515 ;
    v 0 1.057 1.515 ;
    v 0 0.457 1.515 ;
    v 0 0.436 1.499 ;
    v 0 -0.206 1.499 ;
    v 0 0.436 1.121 ;
    v 0 -0.206 1.121 ;
    v 0 0.436 1.138 ;
    v 0 -0.206 1.138 ;
    v 0 0.450 1.111 ;
    v 0 -0.220 1.111 ;
    v 0 0.449 -1.111 ;
    v 0 -0.222 -1.111 ;
    v 0 0.434 -1.138 ;
    v 0 -0.209 -1.138 ;
    v 0 0.434 -1.121 ;
    v 0 -0.209 -1.121 ;
    v 0 0.434 -1.499 ;
    v 0 -0.209 -1.499 ;
    v 0 -0.229 -1.515 ;
    v 0 -0.828 -1.515 ;
    v 0 0.454 -1.515 ;
    v 0 1.054 -1.515 ;
    v 0 0.129 -2.462 ;
    v 0 1.059 -1.532 ;
    v 0 0.097 -2.462 ;
    v 0 -0.834 -1.532 ;
    v 0 -0.209 -1.515 ;
    v 0 0.434 -1.515 ;
    v 0 0.113 -2.479 ;
    v 0 -0.850 -1.515 ;
    v 0 1.075 -1.515 ;
    v 0 0.942 -0.888 ;
    v 0 -0.774 0.888 ;
    v 0 -0.774 -0.888 ;
    v 0 1.370 0 ;
    v 0 1.137 -0.550 ;
    v 0 1.138 0.549 ;
    v 0 -0.969 0.549 ;
    v 0 -0.969 -0.550 ;
    v 0 -1.201 0 ;
  end Verts
 Edges
    e 2 6 ;
    e 6 7 ;
    e 3 7 ;
    e 1 8 ;
    e 8 9 ;
    e 3 9 ;
    e 1 10 ;
    e 10 11 ;
    e 4 11 ;
    e 2 12 ;
    e 12 13 ;
    e 5 13 ;
    e 5 14 ;
    e 4 15 ;
    e 14 18 ;
    e 16 18 ;
    e 15 19 ;
    e 17 19 ;
    e 0 20 ;
    e 16 20 ;
    e 17 21 ;
    e 22 26 ;
    e 23 27 ;
    e 24 26 ;
    e 24 28 ;
    e 25 27 ;
    e 25 29 ;
    e 28 39 ;
    e 29 38 ;
    e 30 38 ;
    e 30 31 ;
    e 31 41 ;
    e 32 39 ;
    e 32 33 ;
    e 33 42 ;
    e 34 40 ;
    e 34 35 ;
    e 35 42 ;
    e 36 40 ;
    e 36 37 ;
    e 37 41 ;
    e 23 45 ;
    e 22 43 ;
    e 21 44 ;
    e 46 48 ;
    e 46 47 ;
    e 0 48 ;
    e 43 47 ;
    e 50 51 ;
    e 49 51 ;
    e 44 49 ;
    e 45 50 ;
  end Edges
end Mesh

Object GZM_IK_Hips MESH GZM_IK_Hips
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
    Modifier Subsurf SUBSURF
      levels 2 ;
    end Modifier
  parent Refer Object CustomShapes ;
end Object


# ----------------------------- MESH --------------------- # 

Mesh GZM_Circle01 GZM_Circle01 
  Verts
    v 0.070 0.500 -0.070 ;
    v 0.099 0.500 0.000 ;
    v 0.070 0.500 0.070 ;
    v 0.000 0.500 0.099 ;
    v -0.070 0.500 0.070 ;
    v -0.099 0.500 0.000 ;
    v -0.070 0.500 -0.070 ;
    v 0.000 0.500 -0.099 ;
    v 0.000 0.500 0.166 ;
    v 0.061 0.500 0.100 ;
    v -0.061 0.500 0.100 ;
    v 0.061 0.500 0.100 ;
    v -0.061 0.500 0.100 ;
    v 0.000 0.500 0.166 ;
    v 0.000 0.500 0.166 ;
    v 0.061 0.500 0.100 ;
    v -0.061 0.500 0.100 ;
  end Verts
  Edges
	e 0 1 ;
	e 1 2 ;
	e 2 3 ;
	e 3 4 ;
	e 4 5 ;
	e 5 6 ;
	e 6 7 ;
	e 0 7 ;
	e 9 11 ;
	e 10 12 ;
	e 8 13 ;
	e 8 14 ;
	e 11 14 ;
	e 9 15 ;
	e 12 15 ;
	e 10 16 ;
	e 13 16 ;
  end Edges
end Mesh

Object GZM_Circle01 MESH GZM_Circle01
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
	Modifier Subsurf SUBSURF
	  levels 2 ;
	end Modifier
  parent Refer Object CustomShapes ;
end Object


# ----------------------------- MESH --------------------- # 

Mesh GZM_Circle025 GZM_Circle025 
  Verts
    v 0.178 0.500 -0.178 ;
    v 0.252 0.500 0.000 ;
    v 0.178 0.500 0.179 ;
    v 0.000 0.500 0.252 ;
    v -0.178 0.500 0.179 ;
    v -0.252 0.500 0.000 ;
    v -0.178 0.500 -0.178 ;
    v 0.000 0.500 -0.252 ;
    v 0.000 0.500 0.420 ;
    v 0.164 0.500 0.256 ;
    v -0.164 0.500 0.256 ;
    v 0.164 0.500 0.256 ;
    v -0.164 0.500 0.256 ;
    v 0.000 0.500 0.420 ;
    v 0.000 0.500 0.420 ;
    v 0.164 0.500 0.256 ;
    v -0.164 0.500 0.256 ;
  end Verts
  Edges
	e 0 1 ;
	e 1 2 ;
	e 2 3 ;
	e 3 4 ;
	e 4 5 ;
	e 5 6 ;
	e 6 7 ;
	e 0 7 ;
	e 9 11 ;
	e 10 12 ;
	e 8 13 ;
	e 8 14 ;
	e 11 14 ;
	e 9 15 ;
	e 12 15 ;
	e 10 16 ;
	e 13 16 ;
  end Edges
end Mesh

Object GZM_Circle025 MESH GZM_Circle025
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
	Modifier Subsurf SUBSURF
	  levels 2 ;
	end Modifier
  parent Refer Object CustomShapes ;
end Object


# ----------------------------- MESH --------------------- # 

Mesh GZM_Circle05 GZM_Circle05 
  Verts
    v 0.369 0.500 -0.368 ;
    v 0.521 0.500 0.000 ;
    v 0.369 0.500 0.369 ;
    v 0.000 0.500 0.522 ;
    v -0.369 0.500 0.369 ;
    v -0.521 0.500 0.000 ;
    v -0.369 0.500 -0.368 ;
    v 0.000 0.500 -0.521 ;
    v 0.000 0.500 0.846 ;
    v 0.320 0.500 0.526 ;
    v -0.320 0.500 0.526 ;
    v 0.320 0.500 0.526 ;
    v -0.320 0.500 0.526 ;
    v 0.000 0.500 0.846 ;
    v 0.000 0.500 0.846 ;
    v 0.320 0.500 0.526 ;
    v -0.320 0.500 0.526 ;
  end Verts
  Edges
	e 0 1 ;
	e 1 2 ;
	e 2 3 ;
	e 3 4 ;
	e 4 5 ;
	e 5 6 ;
	e 6 7 ;
	e 0 7 ;
	e 9 11 ;
	e 10 12 ;
	e 8 13 ;
	e 8 14 ;
	e 11 14 ;
	e 9 15 ;
	e 12 15 ;
	e 10 16 ;
	e 13 16 ;
  end Edges
end Mesh

Object GZM_Circle05 MESH GZM_Circle05
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
	Modifier Subsurf SUBSURF
	  levels 2 ;
	end Modifier
  parent Refer Object CustomShapes ;
end Object


# ----------------------------- MESH --------------------- # 

Mesh GZM_Circle10 GZM_Circle10 
  Verts
    v 0.707 0.500 -0.705 ;
    v 1.000 0.500 0.001 ;
    v 0.707 0.500 0.708 ;
    v 0.000 0.500 1.001 ;
    v -0.707 0.500 0.708 ;
    v -1.000 0.500 0.001 ;
    v -0.707 0.500 -0.705 ;
    v 0.000 0.500 -0.999 ;
    v 0.000 0.500 1.595 ;
    v 0.591 0.500 1.004 ;
    v -0.591 0.500 1.004 ;
    v 0.591 0.500 1.004 ;
    v -0.591 0.500 1.004 ;
    v 0.000 0.500 1.595 ;
    v 0.000 0.500 1.595 ;
    v 0.591 0.500 1.004 ;
    v -0.591 0.500 1.004 ;
  end Verts
  Edges
	e 0 1 ;
	e 1 2 ;
	e 2 3 ;
	e 3 4 ;
	e 4 5 ;
	e 5 6 ;
	e 6 7 ;
	e 0 7 ;
	e 9 11 ;
	e 10 12 ;
	e 8 13 ;
	e 8 14 ;
	e 11 14 ;
	e 9 15 ;
	e 12 15 ;
	e 10 16 ;
	e 13 16 ;
  end Edges
end Mesh

Object GZM_Circle10 MESH GZM_Circle10
  layers Array 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1  ;
	Modifier Subsurf SUBSURF
	  levels 2 ;
	end Modifier
  parent Refer Object CustomShapes ;
end Object

""")
