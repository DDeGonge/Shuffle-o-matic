<!DOCTYPE html>
<!--TheFreeElectron 2015, http://www.instructables.com/member/TheFreeElectron/ -->

<html>
    <head>
        <meta charset="utf-8" />
        <title>Raspberry Pi Gpio</title>
    </head>
 
    <body style="background-color: black;">
    <!-- On/Off button's picture -->
	<?php
	$val_array = array(0,0,0,0,0,0,0,0);
	//this php script generate the first page in function of the file
	for ( $i= 0; $i<8; $i++) {
		//set the pin's mode to output and read them
		system("gpio mode ".$i." out");
		exec ("gpio read ".$i, $val_array[$i], $return );
	}
	//for loop to read the value
	$i =0;
	for ($i = 0; $i < 8; $i++) {
		//if off
		if ($val_array[$i][0] == 0 ) {
			echo ("<img id='button_".$i."' src='data/img/red/red_".$i.".jpg' onclick='change_pin (".$i.");'/>");
		}
		//if on
		if ($val_array[$i][0] == 1 ) {
			echo ("<img id='button_".$i."' src='data/img/green/green_".$i.".jpg' onclick='change_pin (".$i.");'/>");
		}	 
	}
	?>
	 
	<!-- javascript -->
	<script src="script.js"></script>
    </body>
</html>