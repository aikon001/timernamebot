<?php 

$command = escapeshellcmd('bot.py');
$output = shell_exec($command);
echo $output;

?>