CREATE DATABASE IF NOT EXISTS slack;
 
USE slack;
 
CREATE TABLE game(
   game_id int not null auto_increment primary key,
   challenger_id varchar(355) not null,
   challenger_name varchar(355) not null,
   opponent_id varchar(355) not null,
   opponent_name varchar(355) not null,
   winner varchar(355) null,
   turn varchar(355) not null,
   board_id int not null,
   FOREIGN KEY (board_id) REFERENCES board(board_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE channel(
   channel_id varchar(45) primary key not null,
   channel_name varchar(355) not null,
   team_id varchar(355) not null,
   team_domain varchar(355) not null,
   game_id int not null,
   FOREIGN KEY (game_id) REFERENCES game(game_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE board(
   board_id int not null auto_increment primary key,
   contents varchar(45) not null default '---------',
   game_id int not null,
   FOREIGN KEY (game_id) REFERENCES game(game_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;