/*by postgres*/

CREATE TABLE animal_hospitals(
id SERIAL PRIMARY KEY,
area integer NOT NULL,
name text NOT NULL,
url text,
address text,
phone_number VARCHAR (30),
lon float,
lat float,
hospital_url text
);

INSERT INTO animal_hospitals (area, name, url, address, phone_number, lon, lat, hospital_url)
VALUES (3, 'xxx動物病院', '/hospital/detail_xxx/xxxx.html', '東京都xxxxxxxxxxx1-2-3', 'xxx-xxxx-xxxx', 123.45678999, 34.567899999, 'http://test.net/');
