SET FOREIGN_KEY_CHECKS = 0;

ALTER TABLE chuni_score_playlog
  CHANGE COLUMN isClear isClear TINYINT(1) NULL DEFAULT NULL;

ALTER TABLE aime.chuni_score_best
  CHANGE COLUMN isSuccess isSuccess TINYINT(1) NULL DEFAULT NULL ;

ALTER TABLE chuni_score_playlog
  DROP COLUMN ticketId;

SET FOREIGN_KEY_CHECKS = 1;