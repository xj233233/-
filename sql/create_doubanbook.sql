CREATE TABLE IF NOT EXISTS `books` (
  `title` varchar(255) DEFAULT NULL,
  `link` varchar(255) DEFAULT 'NULL' primary key ,
  `country` varchar(255) DEFAULT NULL,
  `author` varchar(255) DEFAULT NULL,
  `translator` varchar(255) DEFAULT NULL,
  `publisher` varchar(255) DEFAULT NULL,
  `press_time` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `star` float DEFAULT NULL,
  `score` float DEFAULT NULL,
  `people` int(11) DEFAULT 0,
  `comment` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS  `book_country_num` (
  `country` varchar(255)  DEFAULT NULL COMMENT '国家',
  `num` int(11) DEFAULT NULL COMMENT '数量'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `book_publisher_num` (
  `publisher` varchar(255)  DEFAULT NULL COMMENT '出版社',
  `num` int(11) DEFAULT NULL COMMENT '数量'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `book_presstime_num` (
  `press_time` varchar(255)  DEFAULT NULL COMMENT '出版时间',
  `num` int(11) DEFAULT NULL COMMENT '数量'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE IF NOT EXISTS `book_people_title` (
  `people` int(11) DEFAULT 0 COMMENT '评论人数',
  `title` varchar(255) DEFAULT NULL COMMENT '书名'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE IF NOT EXISTS `book_score_num` (
  `score` float DEFAULT NULL COMMENT '评分',
  `num` int(11) DEFAULT NULL COMMENT '数量'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
