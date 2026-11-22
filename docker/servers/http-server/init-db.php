<?php
// Same request flow as the "Create / Reset Database" button of setup.php.
$url = 'http://127.0.0.1/setup.php';
$page = file_get_contents($url);
preg_match("/name='user_token' value='([0-9a-f]+)'/", $page, $token);
preg_match('/PHPSESSID=([^;]+)/', implode("\n", $http_response_header), $sid);
file_get_contents($url, false, stream_context_create(['http' => [
    'method' => 'POST',
    'header' => "Content-Type: application/x-www-form-urlencoded\r\nCookie: PHPSESSID={$sid[1]}\r\n",
    'content' => http_build_query(['create_db' => 'Create / Reset Database', 'user_token' => $token[1]]),
    'follow_location' => 0,
]]));
$db = new mysqli('127.0.0.1', 'app', 'vulnerables', 'dvwa');
exit($db->query("SELECT user FROM users WHERE user = 'admin'")->num_rows === 1 ? 0 : 1);
