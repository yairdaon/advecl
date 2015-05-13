OpenWrite["str1d.txt"]
A = Function[T,  Function[{arr,}i, -u[i+0.5]*(T[arr,Mod[i+1,n]] + T[arr,Mod[i,n]])/(2HX) +
				u[i-0.5]*(T[arr,Mod[i,n]] + T[arr,Mod[i-1,n]])/(2HX)]]



string = ToString[CForm[ T[Tin,i] + A[Tin,T][i]*HT]]
string = StringReplace[string  , "0.5"->"0.5f"]
string = StringReplace[string , "2."->"2.f"]

WriteString["str1d.txt", string]
Close["str1d.txt"]
