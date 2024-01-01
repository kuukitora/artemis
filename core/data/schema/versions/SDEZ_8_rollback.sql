ALTER TABLE mai2_profile_detail
    DROP COLUMN currentPlayCount,
    DROP COLUMN renameCredit;

ALTER TABLE mai2_playlog
    DROP COLUMN extBool1;

DROP TABLE IF EXISTS `mai2_playlog_2p`;
