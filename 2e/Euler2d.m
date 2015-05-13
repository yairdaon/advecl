OpenWrite["str2d.txt"]
A = Function[{arr,T} , Function[{i,j},  
				-(u[i+0.5,j]*( T[arr,i+1,j  ] + T[arr,i,j] ) - u[i-0.5 ,j    ]*(T[arr,i,j] +T[arr,i-1,j  ] ))/(2*HX)  
 				-(v[i,j+0.5]*( T[arr,i  ,j+1] + T[arr,i,j] ) - v[i     ,j-0.5]*(T[arr,i,j] +T[arr,i  ,j-1] ))/(2*HY)
 				]]
string  = ToString[CForm[T[Tin,i,j] + HT*A[Tin,T][i,j]]]
string1 = StringReplace[string  , "0.5"->"0.5f"]
string2 = StringReplace[string1 , "2."->"2.f"]
WriteString["str2d.txt",string2]
Close["str2d.txt"]
