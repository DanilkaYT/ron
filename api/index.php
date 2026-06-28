<?php
// index.php

// --- 1. Загружаем исходный файл (Base64) ---
$sourceUrl = 'https://subrostunnel.vercel.app/gen.txt';

$ch = curl_init();
curl_setopt($ch, CURLOPT_URL, $sourceUrl);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false); // отключаем проверку сертификата (если нужно)
curl_setopt($ch, CURLOPT_TIMEOUT, 10);
$raw = curl_exec($ch);
$httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($httpCode !== 200 || $raw === false) {
    http_response_code(500);
    die("Ошибка загрузки файла (HTTP $httpCode)");
}

// --- 2. Декодируем Base64 ---
$decoded = base64_decode($raw, true);
if ($decoded === false) {
    http_response_code(500);
    die("Ошибка декодирования Base64");
}

// --- 3. Обрабатываем строки ---
$lines = explode("\n", $decoded);
$result = [];
$counter = 1;

foreach ($lines as $line) {
    // ищем "LTE" без учёта регистра
    if (stripos($line, 'LTE') !== false) {
        // заменяем wlrus → fastflash-test
        $newLine = str_replace('wlrus', 'fastflash-test', $line);

        // удаляем всё после символа '#'
        if (($pos = strpos($newLine, '#')) !== false) {
            $newLine = substr($newLine, 0, $pos);
        }

        // добавляем флаг, номер и бота
        $newLine .= " #🇩🇪{$counter} @fastflashvpnbot";
        $result[] = $newLine;
        $counter++;
    }
}

// --- 4. Отдаём как plain text ---
header('Content-Type: text/plain');
echo implode("\n", $result);
?>
