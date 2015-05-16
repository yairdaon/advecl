A = Function[T , Function[{arr,i,j,k},  
			  -(u[i+0.5,j,k]*( T[arr,i+1,j  ,k] + T[arr,i,j,k] ) - u[i-0.5 ,j,k]*(T[arr,i,j,k] +T[arr,i-1,j  ,k] ))/(2*HX)  
			  -(v[i,j+0.5,k]*( T[arr,i  ,j+1,k] + T[arr,i,j,k] ) - v[i ,j-0.5,k]*(T[arr,i,j,k] +T[arr,i  ,j-1,k] ))/(2*HY)
			  -(w[i,j,k+0.5]*( T[arr,i  ,j,k+1] + T[arr,i,j,k] ) - w[i ,j,k-0.5]*(T[arr,i,j,k] +T[arr,i  ,j,k-1] ))/(2*HZ)
 				]]
  
  i = xCol
  j = yRow
  k = zDep
  OpenWrite["3Drk3.txt"]
  rk3     = T[Tin,i,j,k] - HT*A[T][Tin,i,j,k] - 0.5*HT*HT*A[A[T]][Tin,i,j,k] + 0.25*HT*HT*HT*A[A[A[T]]][Tin,i,j,k]
  rk3     = ToString[CForm[Simplify[rk3]]]
  rk3     = StringReplace[rk3  , "Power(HX,2)"->"HX*HX"]
  rk3     = StringReplace[rk3  , "Power(HY,2)"->"HY*HY"]
  rk3     = StringReplace[rk3  , "Power(HZ,2)"->"HZ*HZ"]
  rk3     = StringReplace[rk3  , "Power(HT,2)"->"HT*HT"]
  rk3     = StringReplace[rk3  , "Power(HT,3)"->"HT*HT*HT"]
  rk3     = StringReplace[rk3  , "Power(HX,3)"->"HX*HX*HX"]
  rk3     = StringReplace[rk3  , "Power(HY,3)"->"HY*HY*HY"]
  rk3     = StringReplace[rk3  , "Power(HZ,3)"->"HZ*HZ*HZ"]
  rk3     = StringReplace[rk3  , "Power"->"pow"]
  WriteString["3Drk3.txt", rk3]
  Close["3Drk3.txt"]


  OpenWrite["3Drk2.txt"]
  rk2     = T[Tin,i,j,k] + HT*A[T][Tin,i,j,k] + 0.5*HT*HT*A[A[T]][Tin,i,j,k]
  rk2     = ToString[CForm[Simplify[rk2]]]
  rk2     = StringReplace[rk2  , "Power(HX,2)"->"HX*HX"]
  rk2     = StringReplace[rk2  , "Power(HY,2)"->"HY*HY"]
  rk2     = StringReplace[rk2  , "Power(HZ,2)"->"HZ*HZ"]
  rk2     = StringReplace[rk2  , "Power(HT,2)"->"HT*HT"]
  rk2     = StringReplace[rk2  , "Power(HT,3)"->"HT*HT*HT"]
  rk2     = StringReplace[rk2  , "Power(HX,3)"->"HX*HX*HX"]
  rk2     = StringReplace[rk2  , "Power(HY,3)"->"HY*HY*HY"]
  rk2     = StringReplace[rk2  , "Power(HZ,3)"->"HZ*HZ*HZ"]
  rk2     = StringReplace[rk2  , "Power"->"pow"]
  WriteString["3Drk2.txt", rk2]
  Close["3Drk2.txt"]

  OpenWrite["3Drk1.txt"]
  rk1     = T[Tin,i,j,k] + HT*A[T][Tin,i,j,k]
  rk1     = ToString[CForm[Simplify[rk1]]]
  rk1     = StringReplace[rk1  , "Power(HX,2)"->"HX*HX"]
  rk1     = StringReplace[rk1  , "Power(HY,2)"->"HY*HY"]
  rk1     = StringReplace[rk1  , "Power(HZ,2)"->"HZ*HZ"]
  rk1     = StringReplace[rk1  , "Power(HT,2)"->"HT*HT"]
  rk1     = StringReplace[rk1  , "Power(HT,3)"->"HT*HT*HT"]
  rk1     = StringReplace[rk1  , "Power(HX,3)"->"HX*HX*HX"]
  rk1     = StringReplace[rk1  , "Power(HY,3)"->"HY*HY*HY"]
  rk1     = StringReplace[rk1  , "Power(HY,3)"->"HZ*HZ*HZ"]
  rk1     = StringReplace[rk1  , "Power"->"pow"]
  WriteString["3Drk1.txt", rk1]
  Close["3Drk1.txt"]


  rk3 = T + HT*A[T][Tin,i,j] + (HT*HT/3)*A[A[T]][Tin,i,j] + (HT*HT*HT/6)*A[A[A[T]]][Tin,i,j]


 
  
  





  






