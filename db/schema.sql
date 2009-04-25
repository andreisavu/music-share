
drop table if exists `ms_files`;
create table `ms_files` (
	`id` integer not null auto_increment,
	`title` varchar(128) not null,
	`artist` varchar(128) not null,
	`album` varchar(128) not null,
	`year` integer not null,
	`filename` varchar(128) not null,
	`date` timestamp not null,
	primary key(`id`)
)engine=InnoDb

