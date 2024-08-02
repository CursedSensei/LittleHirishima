<?php

require_once 'autoload.php';

$Client = new \GuzzleHttp\Client(['base_uri' => 'https://discord.com/api/v10/']);
$redirectURL = (empty($_SERVER['HTTPS']) ? 'http' : 'https') . "://$_SERVER[HTTP_HOST]$_SERVER[PHP_SELF]";
$auth = ['1000885935107473458', json_decode(file_get_contents('../../Little_Hirishima Secrets.json'))];



function authorizeUser($code) {
    $data = [
        'grant_type' => 'authorization_code',
        'code' => $code,
        'redirect_uri' => $GLOBALS['redirectURL'],
    ];

    $headers = [
        'Content-Type' => 'application/x-www-form-urlencoded'
    ];

    $res = $GLOBALS['Client']->request('POST', 'oauth2/token', [
        'headers' => $headers,
        'form_params' => $data,
        'auth' => $GLOBALS['auth']
    ]);

    return json_decode($res->getBody());
}

function refreshUser($refresh_token) {
    $data = [
        'grant_type' => 'refresh_token',
        'refresh_token' => $refresh_token,
    ];

    $headers = [
        'Content-Type' => 'application/x-www-form-urlencoded'
    ];

    $res = $GLOBALS['Client']->request('POST', 'oauth2/token', [
        'headers' => $headers,
        'form_params' => $data,
        'auth' => $GLOBALS['auth']
    ]);

    return json_decode($res->getBody());
}

function revokeUser($access_token) {
    $data = [
        'token' => $access_token,
        'token_type_hint' => 'access_token',
    ];

    $headers = [
        'Content-Type' => 'application/x-www-form-urlencoded'
    ];

    $res = $GLOBALS['Client']->request('POST', 'oauth2/token/revoke', [
        'headers' => $headers,
        'form_params' => $data,
        'auth' => $GLOBALS['auth']
    ]);

    return $res->getStatusCode() == 200;
}



// API functions here