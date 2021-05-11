loop
areadsensor v
if($v!=X)
	print $v
	rdata $v a b c
	send $c 3
end
if($c>2)
	delay 75000
else
	delay 150000
end