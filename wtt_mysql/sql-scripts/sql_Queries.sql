CREATE DATABASE  IF NOT EXISTS wireless_tracker;
USE wireless_tracker;


--
-- Table structure for  `commands_queue`
--

DROP TABLE IF EXISTS commands_queue;
CREATE TABLE commands_queue (
  idcommands_queue int(11) NOT NULL AUTO_INCREMENT,
  userId varchar(50) DEFAULT NULL,
  cardId varchar(50) DEFAULT NULL,
  action varchar(50),
  content varchar(5550),
  dt_stamp timestamp DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (idcommands_queue)
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=latin1;

--
-- Table structure for table `controller_status`
--

DROP TABLE IF EXISTS card_status;
CREATE TABLE card_status(
  cardId varchar(50),
  cardUid varchar(50),
  cardStatus enum('created','active','deleted','archived') DEFAULT 'created',
  cardAssociated BOOLEAN default False,
  dt_stamp timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (cardId)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Table structure for table `controller`
--

DROP TABLE IF EXISTS card;
CREATE TABLE card (
cardId int(11) NOT NULL AUTO_INCREMENT,
cardUid varchar(50),
cardName varchar(50) DEFAULT Null,
cardContent varchar(55000),
dt_stamp timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
PRIMARY KEY (cardId)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;


--
-- Table structure for table `user_card`
--

DROP TABLE IF EXISTS user_card;
CREATE TABLE user_card (
  cardId int(11) NOT NULL,
  userId int(11) NOT NULL,
  cardContent varchar(55000),
  dt_stamp timestamp DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (cardId,userId)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1;

--
-- Table structure for table `user_session`
--


DROP TABLE IF EXISTS user_session;
CREATE TABLE user_session (
    userId int NOT NULL ,
    token varchar(555),
    mfaCode varchar(10) DEFAULT Null,
    user_Agent varchar(255)
);

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS user;
CREATE TABLE user (
    userId int NOT NULL auto_increment,
    userLogo blob,
    userName varchar(255),
    password varchar(255),
    firstName varchar(255),
    lastName varchar(255),
    emailId varchar(255),
    mobileNo varchar(255),
    policy varchar(1000),
    PRIMARY KEY (UserID)
);

insert into user(username,password) values ('admin','eb8775be2134170de41d74d1d8630ab83cee2847b8ee92b00878dec03439178b7e163ad3144de3d0cd95f04cc6af7f2a963112451281c67b72154771a6a872e4');

set global max_connections = 200;

--
--
--

-- Email summary
--SELECT cardId,cardContent, GROUP_CONCAT(userId) FROM user_card GROUP BY userId;