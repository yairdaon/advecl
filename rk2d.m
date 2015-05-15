A = Function[T , Function[{arr,i,j},  
			  -(u[i+0.5,j]*( T[arr,i+1,j  ] + T[arr,i,j] ) - u[i-0.5 ,j]*(T[arr,i,j] +T[arr,i-1,j  ] ))/(2*HX)  
			  -(v[i,j+0.5]*( T[arr,i  ,j+1] + T[arr,i,j] ) - v[i ,j-0.5]*(T[arr,i,j] +T[arr,i  ,j-1] ))/(2*HY)
 				]]
  
  i = xCol
  j = yRow
  OpenWrite["rk3.txt"]
  rk3     = T[Tin,i,j] - HT*A[T][Tin,i,j] - 0.5*HT*HT*A[A[T]][Tin,i,j] + 0.25*HT*HT*HT*A[A[A[T]]][Tin,i,j]
  rk3     = ToString[CForm[Simplify[rk3]]]
  rk3     = StringReplace[rk3  , "Power(HX,2)"->"HX*HX"]
  rk3     = StringReplace[rk3 , "Power(HY,2)"->"HY*HY"]
  rk3     = StringReplace[rk3  , "Power(HT,2)"->"HT*HT"]
  rk3     = StringReplace[rk3  , "Power(HT,3)"->"HT*HT*HT"]
  rk3     = StringReplace[rk3  , "Power(HX,3)"->"HX*HX*HX"]
  rk3     = StringReplace[rk3  , "Power(HY,3)"->"HY*HY*HY"]
  rk3     = StringReplace[rk3  , "Power"->"pow"]
  WriteString["rk3.txt", rk3]
  Close["rk3.txt"]


  OpenWrite["rk2.txt"]
  rk2     = T[Tin,i,j] + HT*A[T][Tin,i,j] + 0.5*HT*HT*A[A[T]][Tin,i,j]
  rk2     = ToString[CForm[Simplify[rk2]]]
  rk2     = StringReplace[rk2  , "Power(HX,2)"->"HX*HX"]
  rk2     = StringReplace[rk2  , "Power(HY,2)"->"HY*HY"]
  rk2     = StringReplace[rk2  , "Power(HT,2)"->"HT*HT"]
  rk2     = StringReplace[rk2  , "Power(HT,3)"->"HT*HT*HT"]
  rk2     = StringReplace[rk2  , "Power(HX,3)"->"HX*HX*HX"]
  rk2     = StringReplace[rk2  , "Power(HY,3)"->"HY*HY*HY"]
  rk2     = StringReplace[rk2  , "Power"->"pow"]
  WriteString["rk2.txt", rk2]
  Close["rk2.txt"]

  OpenWrite["rk1.txt"]
  rk1     = T[Tin,i,j] + HT*A[T][Tin,i,j]
  rk1     = ToString[CForm[Simplify[rk1]]]
  rk1     = StringReplace[rk1  , "Power(HX,2)"->"HX*HX"]
  rk1     = StringReplace[rk1  , "Power(HY,2)"->"HY*HY"]
  rk1     = StringReplace[rk1  , "Power(HT,2)"->"HT*HT"]
  rk1     = StringReplace[rk1  , "Power(HT,3)"->"HT*HT*HT"]
  rk1     = StringReplace[rk1  , "Power(HX,3)"->"HX*HX*HX"]
  rk1     = StringReplace[rk1  , "Power(HY,3)"->"HY*HY*HY"]
  rk1     = StringReplace[rk1  , "Power"->"pow"]
  WriteString["rk1.txt", rk1]
  Close["rk1.txt"]


  rk3 = T + HT*A[T][Tin,i,j] + (HT*HT/3)*A[A[T]][Tin,i,j] + (HT*HT*HT/6)*A[A[A[T]]][Tin,i,j]


 
  
  





  






