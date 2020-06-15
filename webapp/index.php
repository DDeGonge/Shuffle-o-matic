<html>
	<head>
	</head>

	<body>
		
		<iframe name="hidden_iframe" width="0" height="0" style="border:none"></iframe>
		<form method="post" action="out.php" target="hidden_iframe">
			
	        <input type="submit" name="foo" value="A" />
			<input type="submit" name="foo" value="B" />
			<input type="submit" name="foo" value="C" />
			<input type="submit" name="foo" value="D" />
			<input type="submit" name="foo" value="E" />
			<input type="submit" name="foo" value="F" />
			<input type="submit" name="foo" value="G" />
		
		</form>
		
		<?php
		$name = $_POST['foo'];
		$fp = fopen("formdata.txt", "w");
		fwrite($fp, "");
		$savestring = $name;
		fwrite($fp, $savestring);
		fclose($fp);
		?>
		
	</body>
</html>