--- Создает test_news_loader если она еще не существует
SELECT 'CREATE DATABASE test_news_loader'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'test_news_loader')\gexec