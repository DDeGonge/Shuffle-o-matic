<?php

$fp = fopen('data.txt', 'a');

if(isset($_POST['random_shuffle']))
{
    fwrite($fp, "RAND," . $_POST['r_cycles'] . "," . $_POST['r_cards'] . "\r\n");
}

if(isset($_POST['blackjack_shuffle']))
{
    fwrite($fp, "BJACK," . $_POST['nplayers'] . "," . $_POST['d_win'] . "," . $_POST['p1_win'] . "," . $_POST['p2_win']
    . "," . $_POST['p3_win'] . "," . $_POST['p4_win'] . "," . $_POST['p5_win'] . "\r\n");
}

if(isset($_POST['holdem_shuffle']))
{
    fwrite($fp, "HOLD," . $_POST['nplayers'] . "," . $_POST['discard_bool']
    . "," . $_POST['dealer_card0'] . "," . $_POST['dealer_suit0'] . "," . $_POST['dealer_card1'] . "," . $_POST['dealer_suit1']
    . "," . $_POST['p1_card0'] . "," . $_POST['p1_suit0'] . "," . $_POST['p1_card1'] . "," . $_POST['p1_suit1']
    . "," . $_POST['p2_card0'] . "," . $_POST['p2_suit0'] . "," . $_POST['p2_card1'] . "," . $_POST['p2_suit1']
    . "," . $_POST['p3_card0'] . "," . $_POST['p3_suit0'] . "," . $_POST['p3_card1'] . "," . $_POST['p3_suit1']
    . "," . $_POST['p4_card0'] . "," . $_POST['p4_suit0'] . "," . $_POST['p4_card1'] . "," . $_POST['p4_suit1']
    . "," . $_POST['p5_card0'] . "," . $_POST['p5_suit0'] . "," . $_POST['p5_card1'] . "," . $_POST['p5_suit1']
    . "," . $_POST['p6_card0'] . "," . $_POST['p6_suit0'] . "," . $_POST['p6_card1'] . "," . $_POST['p6_suit1']
    . "," . $_POST['p7_card0'] . "," . $_POST['p7_suit0'] . "," . $_POST['p7_card1'] . "," . $_POST['p7_suit1']
    . "," . $_POST['flop_card0'] . "," . $_POST['flop_suit0'] . "," . $_POST['flop_card1'] . "," . $_POST['flop_suit1'] . "," . $_POST['flop_card2'] . "," . $_POST['flop_suit2']
    . "," . $_POST['turn_card0'] . "," . $_POST['turn_suit0']
    . "," . $_POST['river_card0'] . "," . $_POST['river_suit0'] . "\r\n");
}

fclose($fp);
header("Location: index.html");
?>
