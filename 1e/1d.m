OpenWrite["str1d.txt"]
A = Function[{arr,T},  Function[i, -u[i+0.5]*(T[arr,Mod[i+1,n]] + T[arr,Mod[i,n]])/(2HX) +
				u[i-0.5]*(T[arr,Mod[i,n]] + T[arr,Mod[i-1,n]])/(2HX)]]
string = ToString[CForm[ T[Tin,i] + A[Tin,T][i]*HT]]
WriteString["str1d.txt", string]
Close["str1d.txt"]

