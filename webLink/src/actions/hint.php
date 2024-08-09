<?php
if (!isset($_GET['q'])) {
    exit;
}

function encodeURIComponent($str) {
    $revert = array('%21'=>'!', '%2A'=>'*', '%27'=>"'", '%28'=>'(', '%29'=>')');
    return strtr(rawurlencode($str), $revert);
}

require_once '../../vendor/autoload.php';

try {
    $Client = new \GuzzleHttp\Client();

    $res = $Client->request('GET', "https://suggestqueries-clients6.youtube.com/complete/search?client=youtube&hl=en&gl=ph&gs_rn=64&gs_ri=youtube&ds=yt&cp=6&gs_id=s&q=" . encodeURIComponent($_GET['q']) . "&xhr=t&xssi=t");

    $data = $res->getBody()->getContents();

    $data = explode("\",[", $data);
    $data = join("\",[", array_slice($data, 1));

    $data = json_decode("[" . explode(",{\"", $data)[0]);

    if ($data === null) {
        http_response_code(204);
        exit;
    }

    $output = array();

    $dataLen = count($data);

    for ($i = 0; $i < $dataLen; $i++) {
        $output[] = html_entity_decode($data[$i][0]);
    }

    echo json_encode($output);
} catch (GuzzleHttp\Exception\ClientException $e) {
    http_response_code(204);
}