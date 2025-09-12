# Nginx + PHP-FPM + MariaDB 環境でつまづきやすいポイント

WordPress を動かすために **Nginx + PHP-FPM + MariaDB** を構築する場合、いくつかのハマりポイントがあります。今回はその中でも特によくあるものを3つ紹介します。

---

## 1. `localhost` と `127.0.0.1` の違い
WordPress の `wp-config.php` で  
```php
define( 'DB_HOST', 'localhost' );
```
と書いた場合、MariaDB へは **ソケット接続** が使われます。一方で  
```php
define( 'DB_HOST', '127.0.0.1' );
```
とすれば **TCP接続** になります。  
MariaDB の設定と合わないと「Error establishing a database connection」が出るので注意が必要です。

---

## 2. PHP-FPM のログ出力先
`php-fpm.conf` の `error_log` が存在しないディレクトリを指していると、起動自体に失敗します。  
特に `/usr/local/var/log/` 配下は、権限やファイルシステムの状態でエラーが出やすいので、`/var/log/php-fpm.log` など OS 標準の場所に寄せるのが安全です。

---

## 3. SELinux やファイルパーミッション
一見正しく設定していても、`502 Bad Gateway` や DB 接続エラーが出る場合は、SELinux やディレクトリの権限を疑いましょう。  
テスト時は `getenforce` で Disabled/Permissive を確認、本番では適切なコンテキストを付与するのがベストです。

---

## まとめ
環境構築でハマったときは  
1. DB 接続方法（ソケットかTCPか）  
2. PHP-FPM の設定ファイルとログパス  
3. SELinuxや権限まわり  

この3つを順に確認すると、原因切り分けがスムーズになります。

