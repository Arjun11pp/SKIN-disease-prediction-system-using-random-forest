/*
SQLyog Community Edition- MySQL GUI v8.03 
MySQL - 5.6.12-log : Database - ai_skin
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

CREATE DATABASE /*!32312 IF NOT EXISTS*/`ai_skin` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `ai_skin`;

/*Table structure for table `appointment` */

DROP TABLE IF EXISTS `appointment`;

CREATE TABLE `appointment` (
  `appoint_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `sched_id` int(11) DEFAULT NULL,
  `token_no` int(11) DEFAULT NULL,
  PRIMARY KEY (`appoint_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `appointment` */

insert  into `appointment`(`appoint_id`,`user_id`,`sched_id`,`token_no`) values (1,8,5,0),(2,8,5,1),(3,8,1,1),(4,8,5,1),(5,8,5,1),(6,8,5,1),(7,8,1,1),(8,8,5,2);

/*Table structure for table `bank` */

DROP TABLE IF EXISTS `bank`;

CREATE TABLE `bank` (
  `bank_id` int(11) NOT NULL AUTO_INCREMENT,
  `bank_name` varchar(20) DEFAULT NULL,
  `account_no` varchar(20) DEFAULT NULL,
  `ifsc_no` varchar(20) DEFAULT NULL,
  `balance` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`bank_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `bank` */

insert  into `bank`(`bank_id`,`bank_name`,`account_no`,`ifsc_no`,`balance`) values (1,'sbi','12345','sbi0001','1400'),(2,'sbi','223344','sbi002','400'),(3,'axis','234234','axis11','50');

/*Table structure for table `chat` */

DROP TABLE IF EXISTS `chat`;

CREATE TABLE `chat` (
  `chat_id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(100) DEFAULT NULL,
  `time` varchar(100) DEFAULT NULL,
  `from_id` int(11) DEFAULT NULL,
  `to_id` int(11) DEFAULT NULL,
  `message` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`chat_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `chat` */

/*Table structure for table `disease` */

DROP TABLE IF EXISTS `disease`;

CREATE TABLE `disease` (
  `disease_id` int(11) NOT NULL AUTO_INCREMENT,
  `disease_name` varchar(100) DEFAULT NULL,
  `description` varchar(200) DEFAULT NULL,
  `dtype` varchar(100) DEFAULT NULL,
  `how_to_cure` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`disease_id`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

/*Data for the table `disease` */

insert  into `disease`(`disease_id`,`disease_name`,`description`,`dtype`,`how_to_cure`) values (1,'Acne','commonly located on the face ','Consult Doctor','get medicine'),(3,'Alopecia areata','losing your hair in small patches','Consult Doctor','get medicine'),(4,'Atopic dermatitis(eczema)','dry , itchy skin that leads to swelling ,cracking or scaliness ','Consult Doctor',' get medicine');

/*Table structure for table `doctor` */

DROP TABLE IF EXISTS `doctor`;

CREATE TABLE `doctor` (
  `doctor_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` int(11) DEFAULT NULL,
  `qualification` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`doctor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=latin1;

/*Data for the table `doctor` */

insert  into `doctor`(`doctor_id`,`name`,`email`,`phone`,`qualification`) values (1,'main','krjgn@gsmil.com',2345,'MBBS'),(2,'shanith','shanith1@gmail.com',123456788,'MD'),(7,'akshay','ak@123',987654,'MASTERS IN DERMATOLOGY');

/*Table structure for table `feedback` */

DROP TABLE IF EXISTS `feedback`;

CREATE TABLE `feedback` (
  `feedback_id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `feedback` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`feedback_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=latin1;

/*Data for the table `feedback` */

insert  into `feedback`(`feedback_id`,`user_id`,`date`,`feedback`) values (1,1,'2020-12-10','good'),(2,8,'2023-02-28','yttr'),(3,8,'2023-02-28','yess');

/*Table structure for table `login` */

DROP TABLE IF EXISTS `login`;

CREATE TABLE `login` (
  `login_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(100) DEFAULT NULL,
  `password` varchar(100) DEFAULT NULL,
  `usertype` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`login_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `login` */

insert  into `login`(`login_id`,`username`,`password`,`usertype`) values (1,'admin','admin','admin'),(2,'shanith','1234','doctor'),(4,'mani@123','kk','user'),(5,'jk@gmail.com','jk','user'),(6,'j@gmail.com','kk','user'),(7,'ak@123','akshay','doctor'),(8,'u','u','user');

/*Table structure for table `payment` */

DROP TABLE IF EXISTS `payment`;

CREATE TABLE `payment` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `appoinment_id` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=latin1;

/*Data for the table `payment` */

insert  into `payment`(`payment_id`,`appoinment_id`,`amount`) values (1,9,100),(2,10,100),(3,11,100),(4,12,100),(5,13,100),(6,14,100),(7,15,100),(8,16,100),(9,17,100),(10,18,100),(11,19,100),(12,1,100),(13,2,100),(14,3,100),(15,1,100),(16,2,100),(17,3,100),(18,4,100),(19,5,100),(20,6,100),(21,7,100),(22,8,100);

/*Table structure for table `review` */

DROP TABLE IF EXISTS `review`;

CREATE TABLE `review` (
  `review_id` int(11) NOT NULL AUTO_INCREMENT,
  `date` varchar(100) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `doctor_id` int(11) DEFAULT NULL,
  `review` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`review_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `review` */

insert  into `review`(`review_id`,`date`,`user_id`,`doctor_id`,`review`) values (1,'2022-12-09',1,2,'good service'),(2,'2222-12-30',2,1,'GOOD'),(3,'2023-02-28',8,2,'hrjrjr'),(4,'2023-02-28',8,1,'asd'),(5,'2023-02-28',8,1,'addg');

/*Table structure for table `schedule` */

DROP TABLE IF EXISTS `schedule`;

CREATE TABLE `schedule` (
  `sched_id` int(11) NOT NULL AUTO_INCREMENT,
  `doctor_id` int(11) DEFAULT NULL,
  `date` varchar(100) DEFAULT NULL,
  `time_from` varchar(100) DEFAULT NULL,
  `time_to` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`sched_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

/*Data for the table `schedule` */

insert  into `schedule`(`sched_id`,`doctor_id`,`date`,`time_from`,`time_to`) values (1,2,'2023-01-02','10:00','12:00'),(5,2,'2023-02-14','22:22','12:00');

/*Table structure for table `symptoms` */

DROP TABLE IF EXISTS `symptoms`;

CREATE TABLE `symptoms` (
  `symptom_id` int(11) NOT NULL AUTO_INCREMENT,
  `disease_id` int(11) DEFAULT NULL,
  `symptom_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`symptom_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `symptoms` */

insert  into `symptoms`(`symptom_id`,`disease_id`,`symptom_name`) values (1,2,'asd'),(2,1,'whiteheads, blackheads,pimples'),(6,3,'madness'),(7,3,'loosing hair'),(8,4,'dry and itchy skin');

/*Table structure for table `user` */

DROP TABLE IF EXISTS `user`;

CREATE TABLE `user` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(100) DEFAULT NULL,
  `phone` int(11) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `gender` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=latin1;

/*Data for the table `user` */

insert  into `user`(`user_id`,`name`,`email`,`phone`,`age`,`gender`) values (1,'sh','sh1@gmail.com',987,44,'m'),(2,'manu','mn@123',423,33,'m'),(8,'arjun','a@123',987654,20,'Male');

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
