CREATE TABLE IF NOT EXISTS demo (
  message varchar(255) NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

INSERT INTO demo (message) VALUES('Hello World!');

CREATE TABLE IF NOT EXISTS `tracking` (
  `id` varchar(255) NOT NULL,
  `parent_id` varchar(255) DEFAULT NULL,
  `operation` varchar(255) DEFAULT NULL,
  `service` varchar(255) NOT NULL,
  `interface` varchar(255) DEFAULT NULL,
  `status` varchar(45) NOT NULL,
  `note` text,
  `correlation_id` varchar(255) NOT NULL,
  `namespace` varchar(1000) NOT NULL,
  `user` varchar(255) NOT NULL,
  `client_id` varchar(255) NOT NULL,
  `in` text NOT NULL,
  `out` mediumtext,
  `created` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `server` varchar(255) NOT NULL,
  `original_id` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `IX_tracking_service_operation` (`service`,`operation`),
  KEY `IX_tracking_clientid` (`client_id`),
  KEY `IX_tracking_status` (`status`),
  KEY `IX_tracking_created` (`created`),
  KEY `IX_tracking_correlation_id` (`correlation_id`),
  KEY `IX_tracking_parent_id` (`parent_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE IF NOT EXISTS `tracking_error` (
  `id` int(10) unsigned NOT NULL AUTO_INCREMENT,
  `tracking_id` varchar(255) NOT NULL,
  `type` varchar(255) NOT NULL,
  `message` text,
  `stack` text,
  `created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `FK_TRACKING_ID` (`tracking_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;