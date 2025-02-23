<?php
ini_set('display_errors', 1);
error_reporting(E_ALL);

$uploadDir = "/home/zeus/lightcurves/";

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file']) && $_FILES['file']['error'] === UPLOAD_ERR_OK) {
    $uploadedFile = $_FILES['file'];
    $filename = basename($uploadedFile['name']);    
    $destination = $uploadDir . $filename;
    
    if (move_uploaded_file($uploadedFile['tmp_name'], $destination)) {
        echo 'File uploaded successfully.';
    } else {
        $error = error_get_last();
        error_log(print_r($error, true));
        echo print_r($error, true); // turn this off once you debug hellish perms issue
    }
} else {
    echo 'No file uploaded or there was an upload error.';
}
?>
