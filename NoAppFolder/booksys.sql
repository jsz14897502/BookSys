/*
Navicat MySQL Data Transfer

Source Server         : MySQL
Source Server Version : 50721
Source Host           : localhost:3306
Source Database       : booksys

Target Server Type    : MYSQL
Target Server Version : 50721
File Encoding         : 65001

Date: 2018-07-22 00:16:13
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of auth_group
-- ----------------------------

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of auth_group_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=40 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of auth_permission
-- ----------------------------
INSERT INTO `auth_permission` VALUES ('1', 'Can add log entry', '1', 'add_logentry');
INSERT INTO `auth_permission` VALUES ('2', 'Can change log entry', '1', 'change_logentry');
INSERT INTO `auth_permission` VALUES ('3', 'Can delete log entry', '1', 'delete_logentry');
INSERT INTO `auth_permission` VALUES ('4', 'Can add permission', '2', 'add_permission');
INSERT INTO `auth_permission` VALUES ('5', 'Can change permission', '2', 'change_permission');
INSERT INTO `auth_permission` VALUES ('6', 'Can delete permission', '2', 'delete_permission');
INSERT INTO `auth_permission` VALUES ('7', 'Can add group', '3', 'add_group');
INSERT INTO `auth_permission` VALUES ('8', 'Can change group', '3', 'change_group');
INSERT INTO `auth_permission` VALUES ('9', 'Can delete group', '3', 'delete_group');
INSERT INTO `auth_permission` VALUES ('10', 'Can add user', '4', 'add_user');
INSERT INTO `auth_permission` VALUES ('11', 'Can change user', '4', 'change_user');
INSERT INTO `auth_permission` VALUES ('12', 'Can delete user', '4', 'delete_user');
INSERT INTO `auth_permission` VALUES ('13', 'Can add content type', '5', 'add_contenttype');
INSERT INTO `auth_permission` VALUES ('14', 'Can change content type', '5', 'change_contenttype');
INSERT INTO `auth_permission` VALUES ('15', 'Can delete content type', '5', 'delete_contenttype');
INSERT INTO `auth_permission` VALUES ('16', 'Can add session', '6', 'add_session');
INSERT INTO `auth_permission` VALUES ('17', 'Can change session', '6', 'change_session');
INSERT INTO `auth_permission` VALUES ('18', 'Can delete session', '6', 'delete_session');
INSERT INTO `auth_permission` VALUES ('19', 'Can add book_list', '7', 'add_book_list');
INSERT INTO `auth_permission` VALUES ('20', 'Can change book_list', '7', 'change_book_list');
INSERT INTO `auth_permission` VALUES ('21', 'Can delete book_list', '7', 'delete_book_list');
INSERT INTO `auth_permission` VALUES ('22', 'Can add borrow', '8', 'add_borrow');
INSERT INTO `auth_permission` VALUES ('23', 'Can change borrow', '8', 'change_borrow');
INSERT INTO `auth_permission` VALUES ('24', 'Can delete borrow', '8', 'delete_borrow');
INSERT INTO `auth_permission` VALUES ('25', 'Can add login_record', '9', 'add_login_record');
INSERT INTO `auth_permission` VALUES ('26', 'Can change login_record', '9', 'change_login_record');
INSERT INTO `auth_permission` VALUES ('27', 'Can delete login_record', '9', 'delete_login_record');
INSERT INTO `auth_permission` VALUES ('28', 'Can add request', '10', 'add_request');
INSERT INTO `auth_permission` VALUES ('29', 'Can change request', '10', 'change_request');
INSERT INTO `auth_permission` VALUES ('30', 'Can delete request', '10', 'delete_request');
INSERT INTO `auth_permission` VALUES ('31', 'Can add user', '11', 'add_user');
INSERT INTO `auth_permission` VALUES ('32', 'Can change user', '11', 'change_user');
INSERT INTO `auth_permission` VALUES ('33', 'Can delete user', '11', 'delete_user');
INSERT INTO `auth_permission` VALUES ('34', 'Can add book_short_comment_like_and_collection_record', '12', 'add_book_short_comment_like_and_collection_record');
INSERT INTO `auth_permission` VALUES ('35', 'Can change book_short_comment_like_and_collection_record', '12', 'change_book_short_comment_like_and_collection_record');
INSERT INTO `auth_permission` VALUES ('36', 'Can delete book_short_comment_like_and_collection_record', '12', 'delete_book_short_comment_like_and_collection_record');
INSERT INTO `auth_permission` VALUES ('37', 'Can add book_short_comment', '13', 'add_book_short_comment');
INSERT INTO `auth_permission` VALUES ('38', 'Can change book_short_comment', '13', 'change_book_short_comment');
INSERT INTO `auth_permission` VALUES ('39', 'Can delete book_short_comment', '13', 'delete_book_short_comment');

-- ----------------------------
-- Table structure for auth_user
-- ----------------------------
DROP TABLE IF EXISTS `auth_user`;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of auth_user
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_groups
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_groups`;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_groups_user_id_group_id_94350c0c_uniq` (`user_id`,`group_id`),
  KEY `auth_user_groups_group_id_97559544_fk_auth_group_id` (`group_id`),
  CONSTRAINT `auth_user_groups_group_id_97559544_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `auth_user_groups_user_id_6a12ed8b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of auth_user_groups
-- ----------------------------

-- ----------------------------
-- Table structure for auth_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS `auth_user_user_permissions`;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of auth_user_user_permissions
-- ----------------------------

-- ----------------------------
-- Table structure for django_admin_log
-- ----------------------------
DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of django_admin_log
-- ----------------------------

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of django_content_type
-- ----------------------------
INSERT INTO `django_content_type` VALUES ('1', 'admin', 'logentry');
INSERT INTO `django_content_type` VALUES ('3', 'auth', 'group');
INSERT INTO `django_content_type` VALUES ('2', 'auth', 'permission');
INSERT INTO `django_content_type` VALUES ('4', 'auth', 'user');
INSERT INTO `django_content_type` VALUES ('5', 'contenttypes', 'contenttype');
INSERT INTO `django_content_type` VALUES ('7', 'LibrarySys', 'book_list');
INSERT INTO `django_content_type` VALUES ('13', 'LibrarySys', 'book_short_comment');
INSERT INTO `django_content_type` VALUES ('12', 'LibrarySys', 'book_short_comment_like_and_collection_record');
INSERT INTO `django_content_type` VALUES ('8', 'LibrarySys', 'borrow');
INSERT INTO `django_content_type` VALUES ('9', 'LibrarySys', 'login_record');
INSERT INTO `django_content_type` VALUES ('10', 'LibrarySys', 'request');
INSERT INTO `django_content_type` VALUES ('11', 'LibrarySys', 'user');
INSERT INTO `django_content_type` VALUES ('6', 'sessions', 'session');

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE `django_migrations` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of django_migrations
-- ----------------------------
INSERT INTO `django_migrations` VALUES ('1', 'LibrarySys', '0001_initial', '2018-07-18 07:28:25.598890');
INSERT INTO `django_migrations` VALUES ('2', 'contenttypes', '0001_initial', '2018-07-18 07:28:25.651749');
INSERT INTO `django_migrations` VALUES ('3', 'auth', '0001_initial', '2018-07-18 07:28:26.208784');
INSERT INTO `django_migrations` VALUES ('4', 'admin', '0001_initial', '2018-07-18 07:28:26.328464');
INSERT INTO `django_migrations` VALUES ('5', 'admin', '0002_logentry_remove_auto_add', '2018-07-18 07:28:26.337440');
INSERT INTO `django_migrations` VALUES ('6', 'contenttypes', '0002_remove_content_type_name', '2018-07-18 07:28:26.456123');
INSERT INTO `django_migrations` VALUES ('7', 'auth', '0002_alter_permission_name_max_length', '2018-07-18 07:28:26.505989');
INSERT INTO `django_migrations` VALUES ('8', 'auth', '0003_alter_user_email_max_length', '2018-07-18 07:28:26.524939');
INSERT INTO `django_migrations` VALUES ('9', 'auth', '0004_alter_user_username_opts', '2018-07-18 07:28:26.532918');
INSERT INTO `django_migrations` VALUES ('10', 'auth', '0005_alter_user_last_login_null', '2018-07-18 07:28:26.578795');
INSERT INTO `django_migrations` VALUES ('11', 'auth', '0006_require_contenttypes_0002', '2018-07-18 07:28:26.582784');
INSERT INTO `django_migrations` VALUES ('12', 'auth', '0007_alter_validators_add_error_messages', '2018-07-18 07:28:26.591787');
INSERT INTO `django_migrations` VALUES ('13', 'auth', '0008_alter_user_username_max_length', '2018-07-18 07:28:26.712439');
INSERT INTO `django_migrations` VALUES ('14', 'auth', '0009_alter_user_last_name_max_length', '2018-07-18 07:28:26.766295');
INSERT INTO `django_migrations` VALUES ('15', 'sessions', '0001_initial', '2018-07-18 07:28:26.813170');
INSERT INTO `django_migrations` VALUES ('16', 'LibrarySys', '0002_auto_20180718_1643', '2018-07-18 08:43:48.715836');
INSERT INTO `django_migrations` VALUES ('17', 'LibrarySys', '0003_auto_20180718_1908', '2018-07-18 11:08:50.502182');
INSERT INTO `django_migrations` VALUES ('18', 'LibrarySys', '0004_auto_20180722_0015', '2018-07-21 16:15:14.737727');

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS `django_session`;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of django_session
-- ----------------------------

-- ----------------------------
-- Table structure for librarysys_book_list
-- ----------------------------
DROP TABLE IF EXISTS `librarysys_book_list`;
CREATE TABLE `librarysys_book_list` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `isbn` varchar(15) NOT NULL,
  `book_name` varchar(20) NOT NULL,
  `author` varchar(100) NOT NULL,
  `translator` varchar(40) DEFAULT NULL,
  `press` varchar(20) NOT NULL,
  `price` double NOT NULL,
  `borrowed_times` int(11) NOT NULL,
  `state_code` int(11) NOT NULL,
  `owner_id` int(11) NOT NULL,
  `book_image` varchar(100) DEFAULT NULL,
  `profiles` varchar(300) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `LibrarySys_book_list_owner_id_ab846789_fk_LibrarySys_user_id` (`owner_id`),
  CONSTRAINT `LibrarySys_book_list_owner_id_ab846789_fk_LibrarySys_user_id` FOREIGN KEY (`owner_id`) REFERENCES `librarysys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of librarysys_book_list
-- ----------------------------
INSERT INTO `librarysys_book_list` VALUES ('1', '9787302333142', '汇编语言 第三版', '王爽', null, '清华大学出版社', '39.8', '1', '0', '4', null, null);
INSERT INTO `librarysys_book_list` VALUES ('2', '9787111400851', '数据库系统概念 第六版', 'Abraham Silberschatz; Henry F. Korth; S. Sudarshan', '杨冬青 李红燕 唐世渭', '机械工业出版社', '59', '1', '0', '3', null, null);
INSERT INTO `librarysys_book_list` VALUES ('3', '9787040108231', '托马斯微积分 第十版', 'Finney; Weir; Giordano', '叶其孝 王耀东 唐兢', '高等教育出版社', '88', '0', '0', '1', null, null);

-- ----------------------------
-- Table structure for librarysys_book_short_comment
-- ----------------------------
DROP TABLE IF EXISTS `librarysys_book_short_comment`;
CREATE TABLE `librarysys_book_short_comment` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `comment_text` longtext NOT NULL,
  `comment_time` datetime(6) NOT NULL,
  `like_num` int(11) NOT NULL,
  `unlike_num` int(11) NOT NULL,
  `collect_num` int(11) NOT NULL,
  `book_id` int(11) NOT NULL,
  `commentator_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `LibrarySys_book_shor_book_id_b7dbaf2f_fk_LibrarySy` (`book_id`),
  KEY `LibrarySys_book_shor_commentator_id_3aec72db_fk_LibrarySy` (`commentator_id`),
  CONSTRAINT `LibrarySys_book_shor_book_id_b7dbaf2f_fk_LibrarySy` FOREIGN KEY (`book_id`) REFERENCES `librarysys_book_list` (`id`),
  CONSTRAINT `LibrarySys_book_shor_commentator_id_3aec72db_fk_LibrarySy` FOREIGN KEY (`commentator_id`) REFERENCES `librarysys_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of librarysys_book_short_comment
-- ----------------------------

-- ----------------------------
-- Table structure for librarysys_book_short_comment_like_and_collection_record
-- ----------------------------
DROP TABLE IF EXISTS `librarysys_book_short_comment_like_and_collection_record`;
CREATE TABLE `librarysys_book_short_comment_like_and_collection_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `like_state` tinyint(1) NOT NULL,
  `unlike_state` tinyint(1) NOT NULL,
  `collection_state` tinyint(1) NOT NULL,
  `comment_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `LibrarySys_book_shor_comment_id_320ba44e_fk_LibrarySy` (`comment_id`),
  KEY `LibrarySys_book_shor_user_id_4c014308_fk_LibrarySy` (`user_id`),
  CONSTRAINT `LibrarySys_book_shor_comment_id_320ba44e_fk_LibrarySy` FOREIGN KEY (`comment_id`) REFERENCES `librarysys_book_short_comment` (`id`),
  CONSTRAINT `LibrarySys_book_shor_user_id_4c014308_fk_LibrarySy` FOREIGN KEY (`user_id`) REFERENCES `librarysys_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of librarysys_book_short_comment_like_and_collection_record
-- ----------------------------

-- ----------------------------
-- Table structure for librarysys_borrow
-- ----------------------------
DROP TABLE IF EXISTS `librarysys_borrow`;
CREATE TABLE `librarysys_borrow` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `end_time` datetime(6) NOT NULL,
  `book_name_id` int(11) NOT NULL,
  `previous_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `LibrarySys_borrow_book_name_id_22fd48ed_fk_LibrarySy` (`book_name_id`),
  KEY `LibrarySys_borrow_previous_id_8a6fa548_fk_LibrarySys_user_id` (`previous_id`),
  CONSTRAINT `LibrarySys_borrow_book_name_id_22fd48ed_fk_LibrarySy` FOREIGN KEY (`book_name_id`) REFERENCES `librarysys_book_list` (`id`),
  CONSTRAINT `LibrarySys_borrow_previous_id_8a6fa548_fk_LibrarySys_user_id` FOREIGN KEY (`previous_id`) REFERENCES `librarysys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of librarysys_borrow
-- ----------------------------
INSERT INTO `librarysys_borrow` VALUES ('1', '2018-10-01 19:26:26.000000', '1', '1');
INSERT INTO `librarysys_borrow` VALUES ('2', '2018-10-01 19:28:38.000000', '2', '1');

-- ----------------------------
-- Table structure for librarysys_login_record
-- ----------------------------
DROP TABLE IF EXISTS `librarysys_login_record`;
CREATE TABLE `librarysys_login_record` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login_time` datetime(6) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `LibrarySys_login_record_user_id_417b8f0a_fk_LibrarySys_user_id` (`user_id`),
  CONSTRAINT `LibrarySys_login_record_user_id_417b8f0a_fk_LibrarySys_user_id` FOREIGN KEY (`user_id`) REFERENCES `librarysys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of librarysys_login_record
-- ----------------------------
INSERT INTO `librarysys_login_record` VALUES ('5', '2018-07-20 11:39:44.239729', '3');
INSERT INTO `librarysys_login_record` VALUES ('6', '2018-07-20 11:41:04.287522', '2');
INSERT INTO `librarysys_login_record` VALUES ('7', '2018-07-20 11:46:12.393008', '2');
INSERT INTO `librarysys_login_record` VALUES ('8', '2018-07-20 12:37:42.643831', '2');
INSERT INTO `librarysys_login_record` VALUES ('9', '2018-07-20 12:39:18.958128', '5');
INSERT INTO `librarysys_login_record` VALUES ('10', '2018-07-20 12:51:41.785416', '2');
INSERT INTO `librarysys_login_record` VALUES ('11', '2018-07-20 12:52:58.836708', '6');
INSERT INTO `librarysys_login_record` VALUES ('12', '2018-07-20 12:54:19.049690', '2');
INSERT INTO `librarysys_login_record` VALUES ('13', '2018-07-20 12:54:51.907399', '2');
INSERT INTO `librarysys_login_record` VALUES ('14', '2018-07-20 12:59:43.888759', '2');
INSERT INTO `librarysys_login_record` VALUES ('15', '2018-07-20 13:00:29.423008', '2');
INSERT INTO `librarysys_login_record` VALUES ('16', '2018-07-20 13:03:45.486958', '2');
INSERT INTO `librarysys_login_record` VALUES ('17', '2018-07-20 13:04:23.458031', '2');
INSERT INTO `librarysys_login_record` VALUES ('18', '2018-07-20 13:05:54.955644', '2');
INSERT INTO `librarysys_login_record` VALUES ('19', '2018-07-20 13:07:50.777230', '7');
INSERT INTO `librarysys_login_record` VALUES ('20', '2018-07-20 14:15:24.427486', '2');
INSERT INTO `librarysys_login_record` VALUES ('21', '2018-07-21 07:47:54.386804', '2');
INSERT INTO `librarysys_login_record` VALUES ('22', '2018-07-21 07:48:03.259021', '2');
INSERT INTO `librarysys_login_record` VALUES ('23', '2018-07-21 07:49:06.505292', '2');
INSERT INTO `librarysys_login_record` VALUES ('24', '2018-07-21 15:24:38.972626', '2');

-- ----------------------------
-- Table structure for librarysys_request
-- ----------------------------
DROP TABLE IF EXISTS `librarysys_request`;
CREATE TABLE `librarysys_request` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cretime` datetime(6) NOT NULL,
  `confirm_code` smallint(6) NOT NULL,
  `expiry_time` datetime(6) NOT NULL,
  `book_name_id` int(11) NOT NULL,
  `requster_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `LibrarySys_request_book_name_id_97fec638_fk_LibrarySy` (`book_name_id`),
  KEY `LibrarySys_request_requster_id_dc3c0b38_fk_LibrarySys_user_id` (`requster_id`),
  CONSTRAINT `LibrarySys_request_book_name_id_97fec638_fk_LibrarySy` FOREIGN KEY (`book_name_id`) REFERENCES `librarysys_book_list` (`id`),
  CONSTRAINT `LibrarySys_request_requster_id_dc3c0b38_fk_LibrarySys_user_id` FOREIGN KEY (`requster_id`) REFERENCES `librarysys_user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of librarysys_request
-- ----------------------------
INSERT INTO `librarysys_request` VALUES ('1', '2018-07-18 19:23:15.000000', '0', '2018-10-03 19:23:42.000000', '1', '1');
INSERT INTO `librarysys_request` VALUES ('2', '2018-07-18 19:24:43.000000', '0', '2018-10-03 19:24:50.000000', '2', '1');
INSERT INTO `librarysys_request` VALUES ('3', '2018-07-18 19:25:22.000000', '0', '2018-10-03 19:25:27.000000', '2', '2');
INSERT INTO `librarysys_request` VALUES ('4', '2018-07-18 19:25:45.000000', '0', '2018-10-10 19:25:50.000000', '1', '3');

-- ----------------------------
-- Table structure for librarysys_user
-- ----------------------------
DROP TABLE IF EXISTS `librarysys_user`;
CREATE TABLE `librarysys_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `stu_id` varchar(12) NOT NULL,
  `user_name` varchar(10) NOT NULL,
  `password` varchar(16) NOT NULL,
  `email` varchar(30) NOT NULL,
  `phone` varchar(14) NOT NULL,
  `holds` int(11) DEFAULT NULL,
  `cretime` datetime(6) NOT NULL,
  `last_time` datetime(6) DEFAULT NULL,
  `cancellation` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4;

-- ----------------------------
-- Records of librarysys_user
-- ----------------------------
INSERT INTO `librarysys_user` VALUES ('1', 'library', 'library', 'library', 'library', 'library', '0', '2018-07-17 15:12:52.000000', '2018-07-17 15:12:52.000000', '0');
INSERT INTO `librarysys_user` VALUES ('2', '001', '001', 'python', 'biggrids@outlook.com', 'none', '0', '2018-07-18 18:57:06.000000', '2018-07-18 18:57:09.000000', '0');
INSERT INTO `librarysys_user` VALUES ('3', '002', '002', 'python', '*', 'none', '0', '2018-07-18 19:20:51.000000', '2018-07-18 19:20:54.000000', '0');
INSERT INTO `librarysys_user` VALUES ('4', '003', '003', 'python', '*', 'none', '0', '2018-07-18 19:21:25.000000', '2018-07-18 19:21:27.000000', '0');
INSERT INTO `librarysys_user` VALUES ('5', '004', '004', 'python', '*', 'none', '0', '2018-07-20 12:39:18.958128', '2018-07-20 12:39:18.958128', '0');
INSERT INTO `librarysys_user` VALUES ('6', '005', '005', 'python', '*', 'none', '0', '2018-07-20 12:52:58.836708', '2018-07-20 12:52:58.836708', '0');
INSERT INTO `librarysys_user` VALUES ('7', '006', '006', 'python', '*', 'none', '0', '2018-07-20 13:07:50.777230', '2018-07-20 13:07:50.777230', '0');
