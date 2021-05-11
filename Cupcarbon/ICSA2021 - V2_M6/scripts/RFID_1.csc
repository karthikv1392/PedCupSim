loop
areadsensor v
if($v!=X)
	print $v
	rdata $v a b c
	send $c 3
end
if($c>2)
	delay 30000
else
	delay 60000
end