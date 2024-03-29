ALTER TABLE mai2_item_card
CHANGE COLUMN cardId card_id INT NOT NULL AFTER user,
CHANGE COLUMN cardTypeId card_kind INT NOT NULL,
CHANGE COLUMN charaId chara_id INT NOT NULL,
CHANGE COLUMN mapId map_id INT NOT NULL,
CHANGE COLUMN startDate start_date TIMESTAMP NULL DEFAULT '2018-01-01 00:00:00',
CHANGE COLUMN endDate end_date TIMESTAMP NULL DEFAULT '2038-01-01 00:00:00';

ALTER TABLE mai2_item_item 
CHANGE COLUMN itemId item_id INT NOT NULL AFTER user,
CHANGE COLUMN itemKind item_kind INT NOT NULL,
CHANGE COLUMN isValid is_valid TINYINT(1) NOT NULL DEFAULT '1';

ALTER TABLE mai2_item_character 
CHANGE COLUMN characterId character_id INT NOT NULL,
CHANGE COLUMN useCount use_count INT NOT NULL DEFAULT '0';

ALTER TABLE mai2_item_charge 
CHANGE COLUMN chargeId charge_id INT NOT NULL,
CHANGE COLUMN purchaseDate purchase_date TIMESTAMP NOT NULL,
CHANGE COLUMN validDate valid_date TIMESTAMP NOT NULL;