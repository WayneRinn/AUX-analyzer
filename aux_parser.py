#!/usr/bin/env python


#f = open('AUX.html')

#for lines in f.readlines():
#	print(lines)

#f.close()

DetailsTxt = ["123","456","789"]
ShortTxt = ["abc","def","ghi"]

entry = {"detail":DetailsTxt, "short":ShortTxt}
log = [entry]
print(log)

DetailsTxt = ["111","222","333"]
ShortTxt = ["aaa","bbb","ccc"]
entry = {"detail":DetailsTxt, "short":ShortTxt}
log.append(entry)
print(log)

item = log[0]
print(item["detail"])
print(item["short"])
detailTxt = item["detail"]
print(detailTxt[0])
shortTxt =item["short"]
print(shortTxt[0])

item = log[1]
print(item["detail"])
print(item["short"])

