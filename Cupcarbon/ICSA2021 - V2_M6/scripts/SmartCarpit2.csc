atget id id
loop
areadsensor x
rdata $x a b c
data p $id $c
function y adapter p1en,100,10
if($y==10.0)
	send $p 3
end
if($y==20.0)
	send $p 4
end
if($y==30.0)
	#Internal Processing
	send $p $id		
end
delay 1000