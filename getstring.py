import math
from constants import *
def get(order , hx, hy, ht, nxCenters, nyCenters):
   
    

    # get and modify kernel string
    prg_file = open('ker.c' , 'r')
    prg_str = prg_file.read()
    prg_file.close()# Close file

    # append the constants
    hx_str = "#define HX " + str(hx) + "f\n"
    hy_str = "#define HY " + str(hy) + "f\n"
    ht_str = "#define HT " + str(ht) + "f\n"
    N_str  = "#define N  " + str(nxCenters)  + "\n"
    M_str  = "#define M  " + str(nyCenters)  + "\n"
    PP_str = "#define PP " + str(P)  + "f\n" 
    PSI_str= "#define PSI "+ str(psi)+ "f\n" 
    A_str  = "#define A "  + str(A)  + "f\n" 
    B_str  = "#define B "  + str(B)  + "f\n" 
    PIB_str= "#define PIB "+ str(PIB)+ "f\n"
    D_str  = "#define D "  + str(D)  + "f\n"

    # now we cut and paste and mess with the kernel
    prg_str  =  N_str + M_str + hx_str  + hy_str  + ht_str + prg_str # Add constatns...
    prg_str  =  PP_str  + PSI_str + A_str  + B_str + PIB_str + D_str + prg_str # ...and more constants 
    parts    =  prg_str.split("SPLIT") # Split were we put the Mathematica expression
    op_file  =  open('rk' + str(order) +'.txt' ,'r') # open Mathmatica txt file with RK expression
    op_str   =  op_file.read() # Read the Mathematica expression
    op_file.close() # Close file
    prg_str  =  "\n\n\n" + parts[0] +  op_str + parts[1] + "\n\n\n" #put the expression where it belongs
    
    # Save temporary kernel
    file_    =  open('tmp_ker.c' , 'w')
    file_.write(prg_str)  # save to file, so we see the new kernel
    file_.close()

    return prg_str
