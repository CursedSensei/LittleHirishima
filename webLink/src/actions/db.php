<?php 
$conn = mysqli_connect("localhost", "root", "", "littlehirishima");

if (mysqli_connect_errno()) {
    echo "Failed to connect to MySQL: " . mysqli_connect_error();
    http_response_code(500);
    exit;
}