ALTER TABLE mai2_profile_detail
    ADD currentPlayCount INT NULL AFTER playCount,
    ADD renameCredit INT NULL AFTER banState;

ALTER TABLE mai2_playlog
    ADD extBool1 BOOLEAN NULL AFTER extNum4;

CREATE TABLE `mai2_playlog_2p` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `user` INT NOT NULL,
    `userId1` BIGINT,
    `userId2` BIGINT,
    `userName1` VARCHAR(255),
    `userName2` VARCHAR(255),
    `regionId` INT,
    `placeId` INT,
    `user2pPlaylogDetailList` JSON,
    PRIMARY KEY (`id`),
    FOREIGN KEY (`user`) REFERENCES `aime_user` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
