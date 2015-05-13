OpenWrite["str2d.txt"]
A = Function[T , Function[{arr,i,j},  
			  -(u[i+1,j]*( T[arr,i+1,j  ] + T[arr,i,j] ) - u[i ,j]*(T[arr,i,j] +T[arr,i-1,j  ] ))/(2*HX)  
			  -(v[i,j+1]*( T[arr,i  ,j+1] + T[arr,i,j] ) - v[i ,j]*(T[arr,i,j] +T[arr,i  ,j-1] ))/(2*HY)
 				]]
  
  rk3 = T +HT*A[T][Tin,i,j] + (HT*HT/3)*A[A[T]][Tin,i,j] + (HT*HT*HT/6)*A[A[A[T]]][Tin,i,j]
  rk2 = T[Tin,i,j] + HT*A[T][Tin,i,j] +0.5*HT*HT*A[A[T]][Tin,i,j]
  euler =  T[Tin,i,j] + HT*A[T][Tin,i,j]
  

  expression = euler
  string     = ToString[CForm[Simplify[expression]]]
  string     = StringReplace[string  , ".5"->".5f"]
  string     = StringReplace[string  , "2."->"2.f"]
  string     = StringReplace[string  , "4."->"4.f"]
  string     = StringReplace[string  , "6."->"6.f"]
  string     = StringReplace[string  , ".125"->".125f"]
  string     = StringReplace[string  , "Power(HX,2)"->"HX*HX"]
  string     = StringReplace[string  , "Power(HY,2)"->"HY*HY"]
  string     = StringReplace[string  , "Power(HT,2)"->"HT*HT"]
  string     = StringReplace[string  , "Power(HT,3)"->"HT*HT*HT"]
  string     = StringReplace[string  , "Power(HX,3)"->"HX*HX*HX"]
  string     = StringReplace[string  , "Power(HY,3)"->"HY*HY*HY"]
  string     = StringReplace[string  , "Power"->"pow"]
  WriteString["str2d.txt",string]
  Close["str2d.txt"]
  





  






