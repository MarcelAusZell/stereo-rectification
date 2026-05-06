import numpy as np

def skew_matrix_from_vector(t):
  tx, ty, tz = t.ravel()
  
  return np.array([
    [0, -tz, ty],
    [tz, 0, -tx],
    [-ty, tx, 0],
  ])
  

def compute_fundamental_matrix(K1,K2,R1,R2,T1,T2):
  """
  Input:
  P1 = K1[R1 | T1]
  P2 = K2[R2 | T2]
      
  X = R1 * X1 + T1
  X = R2 * X2 + T2
  
  
  If left 
  Derivation:
  X2 = R2^T * (X - T2)
     = R2^T * (R1 * X1 + T1 - T2)
     = R2^T * R1 * X1 + R2^T * (T1 - T2)
     = R * X1 + T
  Therefore:
      R = R2^T * R1
      T = R2^T * (T1 - T2)
  """
  R = R2.T @ R1
  T = R2.T @ (T1 - T2)

  E = skew_matrix_from_vector(T) @ R
  F = np.linalg.inv(K2).T @ E @ np.linalg.inv(K1)

  return F / np.linalg.norm(F)
  
def rectification_homography(K, R_rect, P):
    return P[:3, :3] @ R_rect @ np.linalg.inv(K)