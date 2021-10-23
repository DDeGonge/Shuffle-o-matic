<?php
$NB_BLACKJACK_PLAYER = 5;
$NB_HOLDEM_PLAYER = 7;
$SIZE_HOLDEM_HANDS = 2;
?>

<html>
	<head>
	<title>Shuffl-o-Matic</title>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1">

		<link rel="stylesheet" href="weblib/bootstrap-5.1.3-dist/css/bootstrap.min.css">
        <link rel="stylesheet" href="css/style.css">
    </head>

	<body>
		<header class="bg-dark p-4 text-center text-white">
		<h2>Shuffl-o-matic</h2>
		</header>

		<iframe name="hidden_iframe" width="0" height="0" style="border:none"></iframe>

		<div class="container-fluid">
			<div class="row">
            <!--Random shuffle column-->
			<div id="rand" class="col-md-6 col-xxl-4">
				<h1>Random Shuffle</h1>
				<p>Enter shuffle parameters.</p>
				<form method="post" action="formhandler.php">
					<div class="mb-3">
						<label for="r_cycles" class="form-label">Number of Shuffle Cycles:</label>
						<input type="number" class="form-control" id="r_cycles" name="r_cycles" value="4">
					</div>
					<div class="mb-5">
						<label for="r_cards" class="form-label">Number of Cards per Cycles:</label>
						<input type="number" class="form-control" id="r_cards" name="r_cards" value="20">
					</div>
					<input type="submit" class="btn btn-dark" name="random_shuffle" value="Shuffle">
				</form>
			</div>

            <!--blackjack shuffle column-->
            <div id="bjack" class="col-md-6 col-xxl-4 text-white">
				<h1>Blackjack Shuffle</h1>
				<p>Enter number of players and who will win.</p>
				<form method="post" action="formhandler.php">
					<div class="mb-5">
						<label for="nplayers" class="form-label">Number of Players (Include Dealer):</label>
						<input type="number" class="form-control" id="nplayers" name="nplayers">
					</div>
                    <?php
                    for ($i = 0; $i <= $NB_BLACKJACK_PLAYER; $i++) {
                        if ($i == 0){
                            $playerIdPart = "d";
                            $playerNamePart = "Dealer";
                        }
                        else {
                            $playerIdPart = "p" . $i;
                            $playerNamePart = "Player " . $i;
                        }

                        echo '<div class="mb-3" >';
                        echo '	<input type = "checkbox" class="form-check-input" id = "' . $playerIdPart . '_win" name = "' . $playerIdPart . '_win" value = "true" >';
                        echo '	<label for="' . $playerIdPart . '_win" class="form-check-label" > ' . $playerNamePart . ' Blackjack </label >';
                        echo '</div >';
					}
					?>
					<input type="submit" class="btn btn-dark mt-3" name="blackjack_shuffle" value="Shuffle">
				</form>
			</div>

            <!--hold'em shuffle column-->
            <div id="hold" class="col-md-12 col-xxl-4 text-white">
                <?php
                function buildHoldEmChoice($choiceName, $choiceNb){
                    echo '<div class="row g-1">';
                    echo '    <div class="col-5">';
                    echo '        <select class="form-select px-2" name="' . $choiceName . '_card' . $choiceNb . '">';
                    echo '	          <option value=""></option>';
                    echo '	          <option value="A">A</option>';
                    echo '	          <option value="2">2</option>';
                    echo '	          <option value="3">3</option>';
                    echo '	          <option value="4">4</option>';
                    echo '	          <option value="5">5</option>';
                    echo '	          <option value="6">6</option>';
                    echo '	          <option value="7">7</option>';
                    echo '	          <option value="8">8</option>';
                    echo '	          <option value="9">9</option>';
                    echo '	          <option value="10">10</option>';
                    echo '	          <option value="J">J</option>';
                    echo '	          <option value="Q">Q</option>';
                    echo '	          <option value="K">K</option>';
                    echo '        </select>';
                    echo '    </div>';
                    echo '    <div class="col-7">';
                    echo '        <select class="form-select px-2" name="' . $choiceName . '_suit' . $choiceNb . '">';
                    echo '	          <option value=""></option>';
                    echo '	          <option value="Heart">&hearts;</option>';
                    echo '	          <option value="Diamond">&diams;</option>';
                    echo '	          <option value="Spade">&spades;</option>';
                    echo '	          <option value="Club">&clubs;</option>';
                    echo '	      </select>';
                    echo '    </div>';
                    echo '</div>';
                }
                ?>

				<h1>Hold-em Shuffle</h1>
				<p>Designate cards as desired. Any unfilled fields will use a random card.</p>
				<form method="post" action="formhandler.php">
					<div>
						<label for="nplayers" class="form-label">Number of Players (Include Dealer):</label>
						<input type="number" class="form-control" id="nplayers" name="nplayers">
					</div>

					<!-- Flop/Turn/River Cards-->
					<div class="container-fluid mt-4 p-0">
						<div class="row">
							<div class="col-4 container-fluid">
								<h6 class="text-center">Flop</h6>
                                <?php
                                buildHoldEmChoice('flop', '0');
                                buildHoldEmChoice('flop', '1');
                                buildHoldEmChoice('flop', '2');
								?>
							</div>
							<div class="col-4 container-fluid">
								<h6 class="text-center">Turn</h6>
                                <?php
                                buildHoldEmChoice('turn', '0');
                                ?>
							</div>
							<div class="col-4 container-fluid">
								<h6 class="text-center">River</h6>
                                <?php
                                buildHoldEmChoice('river', '0');
                                ?>
							</div>
						</div>
					</div>

                    <?php
                    for ($i = 0; $i <= $NB_HOLDEM_PLAYER; $i++) {
                        if ($i == 0){
                            $playerIdPart = "dealer";
                            $playerNamePart = "Dealer";
                        }
                        else {
                            $playerIdPart = "p" . $i;
                            $playerNamePart = "Player " . $i;
                        }

                        echo '<div class="container-fluid mt-4 p-0">';
                        echo '    <div class="row justify-content-start">';
                        echo '        <div class="col-4 container-fluid ms-0">';
                        echo '            <h6 class="text-center">' . $playerNamePart . ' Cards</h6>';
                        for ($j = 0; $j < $SIZE_HOLDEM_HANDS; $j++){
                            buildHoldEmChoice($playerIdPart, $j);
                        }
                        echo '        </div>';
						echo '    </div>';
					    echo '</div>';
                    }
                    ?>
                    <!--Dealer cards-->
<!--					<div class="container-fluid mt-4 p-0">-->
<!--						<div class="row justify-content-start">-->
<!--							<div class="col-4 container-fluid ms-0">-->
<!--								<h6 class="text-center">Dealer Cards</h6>-->
<!--								<div class="row g-1">-->
<!--									<div class="col-4">-->
<!--										<input list="cards" class="form-control px-2" name="dealer_card0" size="1">-->
<!--									</div>-->
<!--									<div class="col-8">-->
<!--										<input list="suits" class="form-control px-2" name="dealer_suit0" size="10">-->
<!--									</div>-->
<!--								</div>-->
<!--								<div class="row g-1">-->
<!--									<div class="col-4">-->
<!--										<input list="cards" class="form-control px-2" name="dealer_card1" size="1">-->
<!--									</div>-->
<!--									<div class="col-8">-->
<!--										<input list="suits" class="form-control px-2" name="dealer_suit1" size="10">-->
<!--									</div>-->
<!--								</div>-->
<!--							</div>-->
<!--						</div>-->
<!--					</div>-->
<!---->
					<!--Player 1 cards-->
<!--					<div class="container-fluid mt-4 p-0">-->
<!--						<div class="row justify-content-start">-->
<!--							<div class="col-4 container-fluid ms-0">-->
<!--								<h6 class="text-center">Player 1 Cards</h6>-->
<!--								<div class="row g-1">-->
<!--									<div class="col-4">-->
<!--										<input list="cards" class="form-control px-2" name="p1_card0" size="1">-->
<!--									</div>-->
<!--									<div class="col-8">-->
<!--										<input list="suits" class="form-control px-2" name="p1_suit0" size="10">-->
<!--									</div>-->
<!--								</div>-->
<!--								<div class="row g-1">-->
<!--									<div class="col-4">-->
<!--										<input list="cards" class="form-control px-2" name="p1_card1" size="1">-->
<!--									</div>-->
<!--									<div class="col-8">-->
<!--										<input list="suits" class="form-control px-2" name="p1_suit1" size="10">-->
<!--									</div>-->
<!--								</div>-->
<!--							</div>-->
<!--						</div>-->
<!--					</div>-->
<!---->
					<!--Player 2 cards-->
<!--					<div class="container-fluid mt-4 p-0">-->
<!--						<div class="row justify-content-start">-->
<!--							<div class="col-4 container-fluid ms-0">-->
<!--								<h6 class="text-center">Player 2 Cards</h6>-->
<!--								<div class="row g-1">-->
<!--									<div class="col-4">-->
<!--										<input list="cards" class="form-control px-2" name="p2_card0" size="1">-->
<!--									</div>-->
<!--									<div class="col-8">-->
<!--										<input list="suits" class="form-control px-2" name="p2_suit0" size="10">-->
<!--									</div>-->
<!--								</div>-->
<!--								<div class="row g-1">-->
<!--									<div class="col-4">-->
<!--										<input list="cards" class="form-control px-2" name="p2_card1" size="1">-->
<!--									</div>-->
<!--									<div class="col-8">-->
<!--										<input list="suits" class="form-control px-2" name="p2_suit1" size="10">-->
<!--									</div>-->
<!--								</div>-->
<!--							</div>-->
<!--						</div>-->
<!--					</div>-->
<!---->
					<!--Player 3 cards-->
<!--					<div class="container-fluid mt-4 p-0">-->
<!--						<div class="row justify-content-start">-->
<!--							<div class="col-4 container-fluid ms-0">-->
<!--								<h6 class="text-center">Player 3 Cards</h6>-->
<!--								<div class="row g-1">-->
<!--									<div class="col-4">-->
<!--										<input list="cards" class="form-control px-2" name="p3_card0" size="1">-->
<!--									</div>-->
<!--									<div class="col-8">-->
<!--										<input list="suits" class="form-control px-2" name="p3_suit0" size="10">-->
<!--									</div>-->
<!--								</div>-->
<!--								<div class="row g-1">-->
<!--									<div class="col-4">-->
<!--										<input list="cards" class="form-control px-2" name="p3_card1" size="1">-->
<!--									</div>-->
<!--									<div class="col-8">-->
<!--										<input list="suits" class="form-control px-2" name="p3_suit1" size="10">-->
<!--									</div>-->
<!--								</div>-->
<!--							</div>-->
<!--						</div>-->
<!--					</div>-->
<!---->
					<!--Player 4 cards-->
<!--					<div class="container-fluid mt-4 p-0">-->
<!--						<div class="row justify-content-start">-->
<!--							<div class="col-4 container-fluid ms-0">-->
<!--								<h6 class="text-center">Player 4 Cards</h6>-->
<!--								<div class="row g-1">-->
<!--									<div class="col-4">-->
<!--										<input list="cards" class="form-control px-2" name="p3_card0" size="1">-->
<!--									</div>-->
<!--									<div class="col-8">-->
<!--										<input list="suits" class="form-control px-2" name="p4_suit0" size="10">-->
<!--									</div>-->
<!--								</div>-->
<!--								<div class="row g-1">-->
<!--									<div class="col-4">-->
<!--										<input list="cards" class="form-control px-2" name="p4_card1" size="1">-->
<!--									</div>-->
<!--									<div class="col-8">-->
<!--										<input list="suits" class="form-control px-2" name="p4_suit1" size="10">-->
<!--									</div>-->
<!--								</div>-->
<!--							</div>-->
<!--						</div>-->
<!--					</div>-->
<!---->
					<!--Player 5 cards-->
<!--					<div class="container-fluid mt-4 p-0">-->
<!--						<div class="row justify-content-start">-->
<!--							<div class="col-4 container-fluid ms-0">-->
<!--								<h6 class="text-center">Player 5 Cards</h6>-->
<!--								<div class="row g-1">-->
<!--									<div class="col-4">-->
<!--										<input list="cards" class="form-control px-2" name="p5_card0" size="1">-->
<!--									</div>-->
<!--									<div class="col-8">-->
<!--										<input list="suits" class="form-control px-2" name="p5_suit0" size="10">-->
<!--									</div>-->
<!--								</div>-->
<!--								<div class="row g-1">-->
<!--									<div class="col-4">-->
<!--										<input list="cards" class="form-control px-2" name="p5_card1" size="1">-->
<!--									</div>-->
<!--									<div class="col-8">-->
<!--										<input list="suits" class="form-control px-2" name="p5_suit1" size="10">-->
<!--									</div>-->
<!--								</div>-->
<!--							</div>-->
<!--						</div>-->
<!--					</div>-->
<!---->
					<!--Player 6 cards-->
<!--					<div class="container-fluid mt-4 p-0">-->
<!--						<div class="row justify-content-start">-->
<!--							<div class="col-4 container-fluid ms-0">-->
<!--								<h6 class="text-center">Player 6 Cards</h6>-->
<!--								<div class="row g-1">-->
<!--									<div class="col-4">-->
<!--										<input list="cards" class="form-control px-2" name="p6_card0" size="1">-->
<!--									</div>-->
<!--									<div class="col-8">-->
<!--										<input list="suits" class="form-control px-2" name="p6_suit0" size="10">-->
<!--									</div>-->
<!--								</div>-->
<!--								<div class="row g-1">-->
<!--									<div class="col-4">-->
<!--										<input list="cards" class="form-control px-2" name="p6_card1" size="1">-->
<!--									</div>-->
<!--									<div class="col-8">-->
<!--										<input list="suits" class="form-control px-2" name="p6_suit1" size="10">-->
<!--									</div>-->
<!--								</div>-->
<!--							</div>-->
<!--						</div>-->
<!--					</div>-->
<!---->
					<!--Player 7 cards-->
<!--					<div class="container-fluid mt-4 p-0">-->
<!--						<div class="row justify-content-start">-->
<!--							<div class="col-4 container-fluid ms-0">-->
<!--								<h6 class="text-center">Player 7 Cards</h6>-->
<!--								<div class="row g-1">-->
<!--									<div class="col-4">-->
<!--										<input list="cards" class="form-control px-2" name="p7_card0" size="1">-->
<!--									</div>-->
<!--									<div class="col-8">-->
<!--										<input list="suits" class="form-control px-2" name="p7_suit0" size="10">-->
<!--									</div>-->
<!--								</div>-->
<!--								<div class="row g-1">-->
<!--									<div class="col-4">-->
<!--										<input list="cards" class="form-control px-2" name="p7_card1" size="1">-->
<!--									</div>-->
<!--									<div class="col-8">-->
<!--										<input list="suits" class="form-control px-2" name="p7_suit1" size="10">-->
<!--									</div>-->
<!--								</div>-->
<!--							</div>-->
<!--						</div>-->
<!--					</div>-->

					<div class="mt-4">
						<input type="checkbox" class="form-check-input" id="discard_bool" name="discard_bool" value="true" checked>
						<label for="discard_bool" class="form-check-label"> One card discarded before flop, turn, and river</label><br><br>
					</div>
					<input type="submit" class="btn btn-dark" name="holdem_shuffle" value="Shuffle">
				</form>
			</div>
		</div>
		</div>
	</body>

	<footer class="text-white text-center p-2">
	<p>www.youtube.com/3DprintedLife</p>
	</footer>
    <script src="weblib/bootstrap-5.1.3-dist/js/bootstrap.bundle.min.js"></script>

</html>
