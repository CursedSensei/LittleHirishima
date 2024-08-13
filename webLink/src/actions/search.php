<?php
if (!isset($_GET['q']) && !isset($_GET['c'])) {
    exit;
}

function lengthString($length) {
    $length = explode(":", $length);
    $out = 0;
    for ($i = count($length) - 1; $i >= 0; $i--) {
        $out += $length[$i] * max(1, 60 * $i);
    }

    return $out;
}

require_once '../../vendor/autoload.php';

try {
    $Client = new \GuzzleHttp\Client();

    $res = $Client->request('POST', "https://www.youtube.com/youtubei/v1/search?prettyPrint=false", [
        'json' => [
            "context" => [
                "client" => [
                    "hl" => "en",
                    "gl" => "PH",
                    "clientName" => "WEB",
                    "clientVersion" => "2.20240702.09.00",
                ]
            ],
            (isset($_GET['q']) ? "query" : "continuation") => (isset($_GET['q']) ? $_GET['q'] : $_GET['c'])
        ]
    ]);

    if (isset($_GET['q'])) {
        $contents = json_decode($res->getBody()->getContents())->contents->twoColumnSearchResultsRenderer->primaryContents->sectionListRenderer->contents;
    } else {
        $contents = json_decode($res->getBody()->getContents())->onResponseReceivedCommands[0]->appendContinuationItemsAction->continuationItems;
    }
    $data = $contents[0]->itemSectionRenderer->contents;
    $data_len = count($data);

    $output = array();
    $empty = true;

    for ($i = 0; $i < $data_len; $i++) {
        $type = key($data[$i]);

        if ($type == "videoRenderer") {
            if (property_exists($data[$i]->videoRenderer, "lengthText")) {
                $len_url = count($data[$i]->videoRenderer->thumbnail->thumbnails) - 1;
                $output[] = [
                    "key" => $data[$i]->videoRenderer->videoId,
                    "name" => $data[$i]->videoRenderer->title->runs[0]->text,
                    "channel" => $data[$i]->videoRenderer->ownerText->runs[0]->text,
                    "thumb" => $data[$i]->videoRenderer->thumbnail->thumbnails[$len_url]->url,
                    "length" => lengthString($data[$i]->videoRenderer->lengthText->simpleText),
                    "rawlength" => $data[$i]->videoRenderer->lengthText->simpleText
                ];
                $empty = false;
            }
        } else if ($type == "shelfRenderer") {
            $data_child = $data[$i]->shelfRenderer->content;

            if (!property_exists($data_child, "verticalListRenderer")) {
                continue;
            }
            $data_child = $data_child->verticalListRenderer->items;
            $child_len = count($data_child);

            for ($j = 0; $j < $child_len; $j++) {
                $type = key($data_child[$j]);

                if ($type == "videoRenderer") {
                    if (property_exists($data_child[$j]->videoRenderer, "lengthText")) {
                        $len_url = count($data_child[$j]->videoRenderer->thumbnail->thumbnails) - 1;
                        $output[] = [
                            "key" => $data_child[$j]->videoRenderer->videoId,
                            "name" => $data_child[$j]->videoRenderer->title->runs[0]->text,
                            "channel" => $data_child[$j]->videoRenderer->ownerText->runs[0]->text,
                            "thumb" => $data_child[$j]->videoRenderer->thumbnail->thumbnails[$len_url]->url,
                            "length" => lengthString($data_child[$j]->videoRenderer->lengthText->simpleText),
                            "rawlength" => $data_child[$j]->videoRenderer->lengthText->simpleText
                        ];
                        $empty = false;
                    }
                }
            }
        }
    }

    if ($empty) {
        http_response_code(204);
    } else {
        $output[] = $contents[1]->continuationItemRenderer->continuationEndpoint->continuationCommand->token;
        echo json_encode($output);
    }
} catch (GuzzleHttp\Exception\ClientException $e) {
    http_response_code(204);
}