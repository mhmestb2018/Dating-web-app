CREATE TABLE IF NOT EXISTS users (
  id int NOT NULL AUTO_INCREMENT,
  name varchar(32) NOT NULL,
  picture_url varchar(1000) NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO users (name, picture_url) VALUES
('Toto', 'gjhgh'),
('Jack', 'gjhgh'),
('Titi', 'gjhgh');