-- MySQL dump 10.16  Distrib 10.1.34-MariaDB, for debian-linux-gnu (x86_64)
--
-- Host: localhost    Database: staffms
-- ------------------------------------------------------
-- Server version	10.1.34-MariaDB-0ubuntu0.18.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth`
--

DROP TABLE IF EXISTS `auth`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `is_active` tinyint(1) NOT NULL DEFAULT '1',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modify_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `last_time` datetime DEFAULT NULL,
  `last_ip` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth`
--

LOCK TABLES `auth` WRITE;
/*!40000 ALTER TABLE `auth` DISABLE KEYS */;
INSERT INTO `auth` VALUES (1,'admin','e10adc3949ba59abbe56e057f20f883e',1,'2019-06-18 11:20:12','2019-07-05 16:36:41','2019-07-05 16:36:41','127.0.0.1');
/*!40000 ALTER TABLE `auth` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `company`
--

DROP TABLE IF EXISTS `company`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `company` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `is_default` tinyint(1) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modify_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `company`
--

LOCK TABLES `company` WRITE;
/*!40000 ALTER TABLE `company` DISABLE KEYS */;
INSERT INTO `company` VALUES (1,'北京测试数据服务公司',1,'2019-06-20 13:41:00','2019-06-20 17:07:24'),(5,'上海人工智障科技有限公司',0,'2019-06-20 17:07:29','2019-07-04 17:43:52');
/*!40000 ALTER TABLE `company` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `department`
--

DROP TABLE IF EXISTS `department`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `department` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `parent` int(255) NOT NULL DEFAULT '0' COMMENT '上级部门',
  `leader` int(255) NOT NULL COMMENT '部门领导',
  `vp` int(255) NOT NULL,
  `hrbp` int(255) NOT NULL,
  `level` int(24) NOT NULL,
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modify_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `department`
--

LOCK TABLES `department` WRITE;
/*!40000 ALTER TABLE `department` DISABLE KEYS */;
INSERT INTO `department` VALUES (1,'高管办公室',0,1,1,1,1,'2019-06-24 14:56:58','2019-06-24 14:56:58'),(2,'销售部',0,1,2,3,1,'2019-06-24 15:26:25','2019-06-24 15:41:05'),(4,'华东大区部',2,1,1,1,2,'2019-06-24 15:27:30','2019-06-24 15:27:30'),(5,'人力行政中心',0,1,1,1,1,'2019-06-24 17:29:30','2019-06-24 17:29:30'),(6,'人力资源部',5,1,1,1,2,'2019-06-24 17:30:18','2019-06-24 17:30:18'),(7,'技术中心',0,1,4,5,1,'2019-07-03 17:21:22','2019-07-03 17:21:22');
/*!40000 ALTER TABLE `department` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job`
--

DROP TABLE IF EXISTS `job`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `job` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `title` varchar(24) NOT NULL COMMENT '职能',
  `level` int(11) NOT NULL COMMENT '职级',
  `sublevel` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job`
--

LOCK TABLES `job` WRITE;
/*!40000 ALTER TABLE `job` DISABLE KEYS */;
INSERT INTO `job` VALUES (1,'运维工程师','P',2,1),(2,'网络工程师','T',3,2),(3,'PHP开发工程师','R',3,1),(4,'产品经理','N',4,3);
/*!40000 ALTER TABLE `job` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `log`
--

DROP TABLE IF EXISTS `log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `log` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `of_operator` int(11) NOT NULL COMMENT '被操作人',
  `message` text NOT NULL COMMENT '消息',
  `operator` int(11) NOT NULL COMMENT '被操作人',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `log`
--

LOCK TABLES `log` WRITE;
/*!40000 ALTER TABLE `log` DISABLE KEYS */;
INSERT INTO `log` VALUES (1,1,'岗位更改日志-由原来的3改变成了3',1,'2019-07-05 18:53:49'),(2,1,'字段：job-日志类型：职位-原值：产品经理-现值：产品经理',1,'2019-07-05 20:21:44'),(3,1,'字段：job-日志类型：职位-原值：产品经理-现值：运维工程师',1,'2019-07-05 20:25:24');
/*!40000 ALTER TABLE `log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `staff` (
  `id` int(255) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL COMMENT '姓名',
  `number` varchar(24) NOT NULL COMMENT '员工编号',
  `email` varchar(255) NOT NULL COMMENT '邮箱',
  `jointime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '入职时间',
  `leavetime` datetime DEFAULT NULL COMMENT '离职时间',
  `is_leave` tinyint(1) NOT NULL DEFAULT '0',
  `job` int(255) NOT NULL,
  `salary` int(255) NOT NULL,
  `equity` int(11) NOT NULL DEFAULT '0' COMMENT '股权',
  `salary_structure` int(11) NOT NULL DEFAULT '12' COMMENT '薪资结构',
  `performance` int(11) NOT NULL DEFAULT '0' COMMENT '绩效奖金',
  `company` int(24) NOT NULL,
  `department` int(24) NOT NULL COMMENT '部门',
  `staffinfo` int(11) NOT NULL COMMENT '链接到info',
  `leader` int(24) NOT NULL COMMENT '直属领导',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modify_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (1,'张小明','BJ0001','zhangxiaoming@zx.com','2019-07-04 00:00:00',NULL,0,1,18000,100,12,10000,5,5,1,0,'2019-07-04 17:49:43','2019-07-05 20:25:24'),(2,'李刚','BJ0002','ligang@test.com','2019-07-03 00:00:00',NULL,0,2,10800,100,15,100,5,6,2,1,'2019-07-04 18:25:44','2019-07-05 18:14:22');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `staffinfo`
--

DROP TABLE IF EXISTS `staffinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `staffinfo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `gender` tinyint(1) NOT NULL DEFAULT '1' COMMENT '1为男0为女',
  `national` varchar(24) DEFAULT NULL COMMENT '民族',
  `birth` date NOT NULL COMMENT '出生年月',
  `place` varchar(255) NOT NULL COMMENT '籍贯',
  `height` int(11) DEFAULT NULL COMMENT '身高',
  `weight` int(11) DEFAULT NULL COMMENT '体重',
  `blood` varchar(24) DEFAULT NULL COMMENT '血型',
  `schooling` varchar(24) NOT NULL COMMENT '学历',
  `school` varchar(255) NOT NULL COMMENT '学校',
  `marriage` tinyint(1) DEFAULT '0' COMMENT '婚否0未婚',
  `qq` varchar(24) DEFAULT NULL COMMENT 'QQ',
  `wechat` varchar(24) DEFAULT NULL COMMENT '微信',
  `oemail` varchar(255) DEFAULT NULL COMMENT '其他邮箱',
  `phone` varchar(24) NOT NULL COMMENT '手机',
  `address` varchar(255) NOT NULL COMMENT '家庭住址',
  `emergency` varchar(255) NOT NULL COMMENT '紧急联系人',
  `emergency_phone` varchar(24) NOT NULL COMMENT '紧急联系人电话',
  `hobby` varchar(255) DEFAULT NULL COMMENT '兴趣爱好',
  `card` varchar(255) NOT NULL COMMENT '身份证',
  `professional` varchar(255) NOT NULL COMMENT '专业',
  `finished` tinyint(1) NOT NULL DEFAULT '0' COMMENT '完成度',
  `create_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `modify_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staffinfo`
--

LOCK TABLES `staffinfo` WRITE;
/*!40000 ALTER TABLE `staffinfo` DISABLE KEYS */;
INSERT INTO `staffinfo` VALUES (1,'张小明',1,'汉族','1990-08-04','浙江省杭州市',0,0,'','博士','浙江大学',0,'888888','z88888','888888@qq.com','18989010000','北京市朝阳区','张大明','13888888888','睡觉','130192199008041234','人工智能',1,'2019-07-04 17:48:18','2019-07-05 19:57:12'),(2,'李刚',1,'维吾尔族','1980-06-24','北京市西城区',0,0,'','硕士','北京大学',1,'101101','','','19999999999','北京市西城区','李大刚','19900000000','','183108198006244819','软件工程',1,'2019-07-04 18:06:52','2019-07-04 18:25:44');
/*!40000 ALTER TABLE `staffinfo` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2019-07-11 11:03:32
