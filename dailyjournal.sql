CREATE TABLE `journal_entries` (
	`id`  INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`concept`  TEXT NOT NULL,
	`entry` TEXT NOT NULL,
	`mood_id` INTEGER NOT NULL,
	`date` DATE NOT NULL,
	FOREIGN KEY(`mood_id`) REFERENCES `moods`(`id`)
);

CREATE TABLE `entry_tags` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    `entry_id` INTEGER NOT NULL,
    `tag_id` INTEGER NOT NULL,
	FOREIGN KEY(`entry_id`) REFERENCES `journal_entries`(`id`),
	FOREIGN KEY(`tag_id`) REFERENCES `tags`(`id`)
);

CREATE TABLE `moods` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`label`	TEXT NOT NULL
);

CREATE TABLE `tags` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`label`	TEXT NOT NULL
);

INSERT INTO `moods` VALUES (null, "Groovy");
INSERT INTO `moods` VALUES (null, "Mercurial");
INSERT INTO `moods` VALUES (null, "Dead Inside");
INSERT INTO `moods` VALUES (null, "Spiffy");
INSERT INTO `moods` VALUES (null, "Dandy");
INSERT INTO `moods` VALUES (null, "Pensive");
INSERT INTO `moods` VALUES (null, "Ennui");
INSERT INTO `moods` VALUES (null, "Brain Fuzz");
INSERT INTO `moods` VALUES (null, "Spicy");
INSERT INTO `moods` VALUES (null, "Demure");
INSERT INTO `moods` VALUES (null, "Elated");
INSERT INTO `moods` VALUES (null, "Enraged");
INSERT INTO `moods` VALUES (null, "Enraptured");
INSERT INTO `moods` VALUES (null, "Erudite");
INSERT INTO `moods` VALUES (null, "Egocentric");

INSERT INTO `journal_entries` VALUES (null, "Hello World", "Dear Diary, oh what adventures we'll share", 1, 2022-07-08);
INSERT INTO `journal_entries` VALUES (null, "Avast", "Thinking of getting more into sea shanties", 6, 20220710);
INSERT INTO `journal_entries` VALUES (null, "Testing Dates", "What format do these damned dates need to be in", 6, 20220710);

INSERT INTO `tags` VALUES (null, "Schemes");
INSERT INTO `tags` VALUES (null, "Updates");
INSERT INTO `tags` VALUES (null, "Rants");

INSERT INTO `entry_tags` VALUES (null, 1, 2);
INSERT INTO `entry_tags` VALUES (null, 2, 1);