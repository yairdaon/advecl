import numpy as np

  

def T_on_boundaries(T):
    ''' 
    calcualte the values of T on the boundaries.
    input:
    T is the value of T in the centers of the cells.
    these range from hx/2 up to x- hx/2

    output:
    vertT is values of T at vertical 
    boundaries of cells, starting from 0 and up to x
    where x is the endpoint of the x domain

    horzT is similar - it is values of horizontal 
    boundaries of cell

    vertT has shape (  nyCenters    ,  nxCenters + 1  )
    horzT has shape (  nyCenters+1  ,  nxCenters      )
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
    vertT        = np.concatenate(
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
    horzT        = np.concatenate(
        (topmost,middle,bottommost) , axis=0 )
    

    assert vertT.shape == (ny    , nx + 1)
    assert horzT.shape == (ny +1 , nx    )

    return vertT , horzT


def f(T, uVertBound, vHorzBound,  hx, hy):


    vertT , horzT = T_on_boundaries(T)
    assert uVertBound.shape == vertT.shape , ("uVertBound.shape == " +str(uVertBound.shape)
                                              +" != "+ str(vertT.shape) + " == vertT.shape.")
    assert vHorzBound.shape == horzT.shape , ("vHorzBound.shape == " +str(vHorzBound.shape)
                                              +" != "+ str(horzT.shape) + " == horzT.shape.") 
    
    # define F
    F  = uVertBound * vertT  
    
    # calculate the differences of F
    dF = F[:,1:] - F[:,0:-1]
    assert dF.shape == T.shape

    # define G
    G  = vHorzBound * horzT
    
    # calculate the differences of G
    dG = G[1:,:] - G[0: -1,:]
    assert dG.shape == T.shape

    # find the value of f and return it
    rt = -(dF*hy + dG*hx)/(hx*hy)   
    return rt

def RK3( T, u, v, hx,hy, ht):
    '''
    do a third order RK time step
    T is values of T at centers of cells
    u is values of u flows on vertiaccl boundaries
    v is values of v flows on horizontal boundaries
    hx is step size in x direction
    hy is step size in y direction
    ht is time step
    '''

    alpha = .5
    beta  = .4
    gamma = .3
    a1    = .2
    a2    = .7
    a3    = .1
    
    v1 = f( T, u, v, hx, hy )*ht              # stage 1, v1 = dt* f(x)       
    
    Ttmp = T + alpha*v1
    v2 = f( Ttmp, u, v, hx, hy )*ht                 # stage 2, v2 = dt*f(x+alpha*v1)    
    
    Ttmp = T + beta*v1 + gamma*v2
    v3 = f( Ttmp, u, v, hx, hy)*ht   #  stage 3, v3 = dt*f(x+beta*v1+gamma*v2)
    
    dT = (a1*v1 + a2*v2 + a3*v3)*ht

    return T+dT


def F(u,Tx):
    '''
    deprecated. dont use unless you have to
    '''
    assert u.shape == Tx.shape , "u.shape == " +str(u.shape) +" != "+ str(Tx.shape) + " == Tx.shape."
    return u* Tx  

def G(v, Ty):
    '''
    deprecated, dont use unless you have to
    '''

    assert v.shape == Ty.shape ,"v.shape == " +str(v.shape) +" != "+ str(Ty.shape) + " == Ty.shape." 
    return  v*Ty
