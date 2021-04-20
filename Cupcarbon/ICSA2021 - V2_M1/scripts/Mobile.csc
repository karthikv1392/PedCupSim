atget id id
loop
wait
read v
#for i 0 3	
	#send "Processing!" $id
	#wait
	#read val
	#cprint $val
#end
send $v 4