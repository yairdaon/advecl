import numpy as np

def T_on_boundaries(T):
    ''' 
    calcualte the values of T on the boundaries.
    input:
    T is the value of T in the centers of the cells.
    these range from hx/2 up to x- hx/2

    output:
    TxPlusHalf is (averaged) values of T at vertical 
    boundaries of cells, starting from 0 and up to x
    where x is the endpoint of the x domain

    TyPlusHalf is similar - it is values of horizontal 
    boundaries of cell
    '''

    ny , nx = T.shape

    left      =  T[:,1:nx  ]     # left cells
    right     =  T[:,0:nx-1]     # right cells
    assert left.shape == right.shape

    middle    = (left + right)/2.0 # averaged cells
    leftmost  =  T[:,0] #leftmost boundary
    rightmost =  T[:,nx-1] # rightmost boundary
    
    leftmost  = leftmost.reshape( ( ny , 1) )
    rightmost = rightmost.reshape(( ny , 1) )

    # concatenate
    Tx        = np.concatenate(
        (leftmost,middle,rightmost) , axis=1 )

    

    # similar to above ...
    top        =  T[1:ny   , : ]     # top    cells
    bottom     =  T[0:ny-1 , : ]     # bottom cells
    assert top.shape == bottom.shape
    
    middle     = (top + bottom)/2.0 # averaged cells
    topmost    =  T[0    , :] #topmost boundary
    bottommost =  T[ny-1 , :] # bottom-most boundary
    
    topmost    = topmost.reshape    ( (1, nx) )
    bottommost = bottommost.reshape ( (1, nx) )
    # concatenate
    Ty        = np.concatenate(
        (topmost,middle,bottommost) , axis=0 )
    

    assert Tx.shape == (ny    , nx + 1)
    assert Ty.shape == (ny +1 , nx    )

    return Tx , Ty

    
def F(u, Tx): 
    ''' 
    calculate F = u*T at (x_j + hx/2 , y_k)
    '''
    assert u.shape == Tx.shape , "u.shape == " +str(u.shape) +" != "+ str(Tx.shape) + " == Tx.shape."
    return u * Tx

def G(v, Ty):
    ''' 
    calculate G = V*T at (x_j , y_k + hy/2)
    '''
    assert v.shape == Ty.shape ,"v.shape == " +str(v.shape) +" != "+ str(Ty.shape) + " == Ty.shape." 
    return v * Ty

alpha = .5
beta  = .4
gamma = .3
a1    = .2
a2    = .7
a3    = .1

def RK3( dx, x,  dt){
   
  double *xt;    // "x temporary", to hold x + alpha*v1 or x + beta*v1 + gamma*v2
  xt = dx;       // WARNING: uses the same storage as dx
  
  f( v1, x);                      // stage 1, v1 = dt* f(x)
  for ( int j = 0; j < n; j++){
     v1[j] = dt*v1[j];
     xt[j] = x[j] + alpha*v1[j];  // next point = x + alpha*v1
    }
  
  f( v2, xt);                     // stage 2, v2 = dt*f(x+alpha*v1)
  for ( int j = 0; j < n; j++){
     v2[j] = dt*v2[j];
     xt[j] = x[j] + beta*v1[j] + gamma*v2[j];
    }
  
  f( v3, xt);                     // stage 3, v3 = dt*f(x+beta*v1+gamma*v1)
  for ( int j = 0; j < n; j++){
     v3[j] = dt*v3[j];
    }
  
  for ( int j = 0; j < n; j++){
     dx[j] = a1*v1[j] + a2*v2[j] + a3*v3[j];
    }
  

}
