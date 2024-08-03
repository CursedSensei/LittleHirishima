<?php

require_once 'autoload.php';

$Client = new \GuzzleHttp\Client(['base_uri' => 'https://discord.com/api/v10/']);
$redirectURL = (empty($_SERVER['HTTPS']) ? 'http' : 'https') . "://$_SERVER[HTTP_HOST]$_SERVER[PHP_SELF]";
$headers = ['Content-Type' => 'application/x-www-form-urlencoded'];
$botGuilds = json_decode(file_get_contents(__DIR__ . '/../../lib/Guild/guilds.json'));


define('ID', '1000885935107473458');
define('TOKEN', file_get_contents(__DIR__ . '/../vendor/discordTOKEN.secret'));



function authorizeUser($code) {
    try {
        $data = [
            'grant_type' => 'authorization_code',
            'code' => $code,
            'redirect_uri' => $GLOBALS['redirectURL'],
        ];

        $res = $GLOBALS['Client']->request('POST', 'oauth2/token', [
            'headers' => $GLOBALS['headers'],
            'form_params' => $data,
            'auth' => [ID, TOKEN]
        ]);

        return json_decode($res->getBody()->getContents());
    } catch (GuzzleHttp\Exception\ClientException $e) {
        return false;
    }
}

function refreshUser() {
    try {
        $data = [
            'grant_type' => 'refresh_token',
            'refresh_token' => $_SESSION['refresh_token'],
        ];

        $res = $GLOBALS['Client']->request('POST', 'oauth2/token', [
            'headers' => $GLOBALS['headers'],
            'form_params' => $data,
            'auth' => [ID, TOKEN]
        ]);

        $token = json_decode($res->getBody()->getContents());

        $_SESSION['access_token'] = $token->access_token;
        $_SESSION['refresh_token'] = $token->refresh_token;

        return true;
    } catch (GuzzleHttp\Exception\ClientException $e) {
        return false;
    }
}

function revokeUser() {
    try {
        $data = [
            'token' => $_SESSION['access_token'],
            'token_type_hint' => 'access_token',
        ];

        $res = $GLOBALS['Client']->request('POST', 'oauth2/token/revoke', [
            'headers' => $GLOBALS['headers'],
            'form_params' => $data,
            'auth' => [ID, TOKEN]
        ]);

        return $res->getStatusCode() == 200;
    } catch (GuzzleHttp\Exception\ClientException $e) {
        return False;
    }
}



function getUser($access_token) {
    try {
        $res = $GLOBALS['Client']->request('GET', 'users/@me', [
            'headers' => ['Authorization' => "Bearer " . $access_token]
        ]);

        $data = json_decode($res->getBody()->getContents());

        return [
            'id' => $data->id,
            'name' => $data->global_name,
            'avatar' => $data->avatar,
        ];
    } catch (GuzzleHttp\Exception\ClientException $e) {
        return False;
    }
}

function filterGuilds($val) {
    if (array_search($val->id, $GLOBALS['botGuilds']) == false) {
        if (count($GLOBALS['botGuilds']) > 0 && $GLOBALS['botGuilds'][0] == $val->id) return true;
        return false;
    }
    return true;
}

function getGuilds() {
    $refreshed = false;

    while (true) {
        try {
            $res = $GLOBALS['Client']->request('GET', 'users/@me/guilds', [
                'headers' => ['Authorization' => "Bearer " . $_SESSION['access_token']]
            ]);

            $userGuilds = json_decode($res->getBody()->getContents());

            return array_values(array_filter($userGuilds, "filterGuilds"));
        } catch (GuzzleHttp\Exception\ClientException $e) {
            if ($refreshed) return false;
            if (!refreshUser()) return false;
            $refreshed = true;
        }
    }
}