ALTER TABLE mai2_item_card
CHANGE COLUMN card_id cardId INT NOT NULL AFTER user,
CHANGE COLUMN card_kind cardTypeId INT NOT NULL,
CHANGE COLUMN chara_id charaId INT NOT NULL,
CHANGE COLUMN map_id mapId INT NOT NULL,
CHANGE COLUMN startDate startDate TIMESTAMP NULL DEFAULT '2018-01-01 00:00:00',
CHANGE COLUMN endDate endDate TIMESTAMP NULL DEFAULT '2038-01-01 00:00:00';

ALTER TABLE mai2_item_item 
CHANGE COLUMN item_id itemId INT NOT NULL AFTER user,
CHANGE COLUMN item_kind itemKind INT NOT NULL,
CHANGE COLUMN is_valid isValid TINYINT(1) NOT NULL DEFAULT '1';

ALTER TABLE mai2_item_character 
CHANGE COLUMN character_id characterId INT NOT NULL,
CHANGE COLUMN use_count useCount INT NOT NULL DEFAULT '0';

ALTER TABLE mai2_item_charge 
CHANGE COLUMN charge_id chargeId INT NOT NULL,
CHANGE COLUMN purchase_date purchaseDate TIMESTAMP NOT NULL,
CHANGE COLUMN valid_date validDate TIMESTAMP NOT NULL;
