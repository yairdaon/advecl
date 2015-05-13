


  a = HT*A[T][Tin,i,j]
  b = HT*A[T][Tin,i,j] + HT*HT*A[A[T]][Tin,i,j]
  c = HT*A[T][Tin,i,j] + HT*HT*A[A[T]][Tin,i,j] +HT*HT*HT*A[A[A[T]]][Tin,i,j]
  string     = StringReplace[string  , ".5"->".5f"]
  string     = StringReplace[string  , "2."->"2.f"]
  string     = StringReplace[string  , "4."->"4.f"]
  string     = StringReplace[string  , "6."->"6.f"]
  string     = StringReplace[string  , "Power(HX,2)"->"HX*HX"]
  string     = StringReplace[string  , "Power(HY,2)"->"HY*HY"]
  string     = StringReplace[string  , "Power(HT,2)"->"HT*HT"]
  string     = StringReplace[string  , "Power(HT,3)"->"HT*HT*HT"]
  string     = StringReplace[string  , "Power(HX,3)"->"HX*HX*HX"]
  string     = StringReplace[string  , "Power(HY,3)"->"HY*HY*HY"]
