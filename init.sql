CREATE TABLE `t_ymx_detail` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `asin` varchar(100) NOT NULL DEFAULT '' COMMENT 'asin',
  `stars` float(5,2) NOT NULL DEFAULT '0.00',
  `reviews` int(10) NOT NULL,
  `last_review_time` timestamp NULL DEFAULT NULL,
  `title` varchar(500) DEFAULT NULL,
  `brand` varchar(200) DEFAULT NULL,
  `keyword` varchar(200) DEFAULT NULL,
  `keyword_id` int(11) NOT NULL COMMENT 'id',
  `creat_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `state` tinyint(5) NOT NULL DEFAULT '0' COMMENT ' 0 1',
  `detail_link` varchar(2000) DEFAULT NULL,
  `detail_link_id` int(11) NOT NULL COMMENT 'id',
  `is_variant` tinyint(3) DEFAULT NULL COMMENT 'is_variant',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=210347 DEFAULT CHARSET=utf8;


CREATE TABLE `t_ymx_detail_link` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `detail_link` varchar(300) NOT NULL DEFAULT '',
  `job_state` tinyint(5) NOT NULL DEFAULT '0' COMMENT '0123-1',
  `keyword_id` int(11) DEFAULT NULL COMMENT 'idt_ymx_keyword',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  `real_link` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `detail_link` (`detail_link`),
  UNIQUE KEY `detail_link_2` (`detail_link`)
) ENGINE=InnoDB AUTO_INCREMENT=455056 DEFAULT CHARSET=utf8;

CREATE TABLE `t_ymx_dir_detail_link` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `detail_link` varchar(2000) NOT NULL DEFAULT '',
  `job_state` tinyint(5) NOT NULL DEFAULT '0' COMMENT '0123-1',
  `keyword_id` int(11) DEFAULT NULL COMMENT 'idt_ymx_keyword',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `t_ymx_google_host` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `google_host` varchar(200) DEFAULT NULL COMMENT 'google 各国host',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=140 DEFAULT CHARSET=utf8;


CREATE TABLE `t_ymx_keyword` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `keyword` varchar(100) NOT NULL DEFAULT '',
  `job_state` tinyint(3) NOT NULL DEFAULT '0' COMMENT '0123-1',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=73641 DEFAULT CHARSET=utf8;



CREATE TABLE `t_ymx_slp_link` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT '主键',
  `slp_link` varchar(300) NOT NULL DEFAULT '' COMMENT '详细页连接',
  `job_state` tinyint(5) NOT NULL DEFAULT '0' COMMENT '详细页连接状态。0：待爬，1：爬取中，2：爬取成功，3：爬取失败，-1：不爬了',
  `keyword_id` int(11) DEFAULT NULL COMMENT '关键词id，关联t_ymx_keyword表',
  `create_time` timestamp NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` timestamp NULL DEFAULT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`),
  UNIQUE KEY `slp_link` (`slp_link`)
) ENGINE=InnoDB AUTO_INCREMENT=256974 DEFAULT CHARSET=utf8;