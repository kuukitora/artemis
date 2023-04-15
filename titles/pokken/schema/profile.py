from typing import Optional, Dict, List
from sqlalchemy import Table, Column, UniqueConstraint, PrimaryKeyConstraint, and_, case
from sqlalchemy.types import Integer, String, TIMESTAMP, Boolean, JSON
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func, select, update, delete
from sqlalchemy.engine import Row
from sqlalchemy.dialects.mysql import insert

from core.data.schema import BaseData, metadata
from ..const import PokkenConstants

# Some more of the repeated fields could probably be their own tables, for now I just did the ones that made sense to me
# Having the profile table be this massive kinda blows for updates but w/e, **kwargs to the rescue
profile = Table(
    'pokken_profile',
    metadata,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user', ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"), nullable=False, unique=True),
    Column('trainer_name', String(16)), # optional
    Column('home_region_code', Integer),
    Column('home_loc_name', String(255)),
    Column('pref_code', Integer),
    Column('navi_newbie_flag', Boolean),
    Column('navi_enable_flag', Boolean),
    Column('pad_vibrate_flag', Boolean),
    Column('trainer_rank_point', Integer),
    Column('wallet', Integer),
    Column('fight_money', Integer),
    Column('score_point', Integer),
    Column('grade_max_num', Integer),
    Column('extra_counter', Integer), # Optional
    Column('tutorial_progress_flag', JSON), # Repeated, Integer
    Column('total_play_days', Integer),
    Column('play_date_time', Integer),
    Column('achievement_flag', JSON), # Repeated, Integer
    Column('lucky_box_fail_num', Integer),
    Column('event_reward_get_flag', Integer),
    Column('rank_pvp_all', Integer),
    Column('rank_pvp_loc', Integer),
    Column('rank_cpu_all', Integer),
    Column('rank_cpu_loc', Integer),
    Column('rank_event', Integer),
    Column('awake_num', Integer),
    Column('use_support_num', Integer),
    Column('rankmatch_flag', Integer),
    Column('rankmatch_max', Integer), # Optional
    Column('rankmatch_progress', JSON), # Repeated, Integer
    Column('rankmatch_success', Integer), # Optional
    Column('beat_num', Integer), # Optional
    Column('title_text_id', Integer),
    Column('title_plate_id', Integer),
    Column('title_decoration_id', Integer),
    Column('support_pokemon_list', JSON), # Repeated, Integer
    Column('support_set_1_1', Integer), # Repeated, Integer
    Column('support_set_1_2', Integer),
    Column('support_set_2_1', Integer), # Repeated, Integer
    Column('support_set_2_2', Integer),
    Column('support_set_3_1', Integer), # Repeated, Integer
    Column('support_set_3_2', Integer),
    Column('navi_trainer', Integer),
    Column('navi_version_id', Integer),
    Column('aid_skill_list', JSON), # Repeated, Integer
    Column('aid_skill', Integer),
    Column('comment_text_id', Integer),
    Column('comment_word_id', Integer),
    Column('latest_use_pokemon', Integer),
    Column('ex_ko_num', Integer),
    Column('wko_num', Integer),
    Column('timeup_win_num', Integer),
    Column('cool_ko_num', Integer),
    Column('perfect_ko_num', Integer),
    Column('record_flag', Integer),
    Column('continue_num', Integer),
    Column('avatar_body', Integer), # Optional
    Column('avatar_gender', Integer), # Optional
    Column('avatar_background', Integer), # Optional
    Column('avatar_head', Integer), # Optional
    Column('avatar_battleglass', Integer), # Optional
    Column('avatar_face0', Integer), # Optional
    Column('avatar_face1', Integer), # Optional
    Column('avatar_face2', Integer), # Optional
    Column('avatar_bodyall', Integer), # Optional
    Column('avatar_wear', Integer), # Optional
    Column('avatar_accessory', Integer), # Optional
    Column('avatar_stamp', Integer), # Optional
    Column('event_state', Integer),
    Column('event_id', Integer),
    Column('sp_bonus_category_id_1', Integer),
    Column('sp_bonus_key_value_1', Integer),
    Column('sp_bonus_category_id_2', Integer),
    Column('sp_bonus_key_value_2', Integer),
    Column('last_play_event_id', Integer), # Optional
    Column('event_achievement_flag', JSON), # Repeated, Integer
    Column('event_achievement_param', JSON), # Repeated, Integer
    Column('battle_num_vs_wan', Integer), # 4?
    Column('win_vs_wan', Integer),
    Column('battle_num_vs_lan', Integer), # 3?
    Column('win_vs_lan', Integer),
    Column('battle_num_vs_cpu', Integer), # 2
    Column('win_cpu', Integer),
    Column('battle_num_tutorial', Integer), # 1?
    mysql_charset="utf8mb4"
)

pokemon_data = Table(
    'pokken_pokemon_data',
    metadata,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('user', ForeignKey("aime_user.id", ondelete="cascade", onupdate="cascade"), nullable=False),
    Column('char_id', Integer, nullable=False),
    Column('illustration_book_no', Integer),
    Column('pokemon_exp', Integer),
    Column('battle_num_vs_wan', Integer), # 4?
    Column('win_vs_wan', Integer),
    Column('battle_num_vs_lan', Integer), # 3?
    Column('win_vs_lan', Integer),
    Column('battle_num_vs_cpu', Integer), # 2
    Column('win_cpu', Integer),
    Column('battle_all_num_tutorial', Integer),
    Column('battle_num_tutorial', Integer), # 1?
    Column('bp_point_atk', Integer),
    Column('bp_point_res', Integer),
    Column('bp_point_def', Integer),
    Column('bp_point_sp', Integer),
    UniqueConstraint('user', 'char_id', name="pokken_pokemon_data_uk"),
    mysql_charset="utf8mb4"
)

class PokkenProfileData(BaseData):
    def create_profile(self, user_id: int) -> Optional[int]:
        sql = insert(profile).values(user = user_id)
        conflict = sql.on_duplicate_key_update(user = user_id)
        
        result = self.execute(conflict)
        if result is None:
            self.logger.error(f"Failed to create pokken profile for user {user_id}!")
            return None
        return result.lastrowid
    
    def set_profile_name(self, user_id: int, new_name: str) -> None:
        sql = update(profile).where(profile.c.user == user_id).values(trainer_name = new_name)
        result = self.execute(sql)
        if result is None:
            self.logger.error(f"Failed to update pokken profile name for user {user_id}!")
    
    def update_profile_tutorial_flags(self, user_id: int, tutorial_flags: Dict) -> None:
        pass

    def add_profile_points(self, user_id: int, rank_pts: int, money: int, score_pts: int) -> None:
        pass

    def get_profile(self, user_id: int) -> Optional[Row]:
        sql = profile.select(profile.c.user == user_id)
        result = self.execute(sql)
        if result is None: return None
        return result.fetchone()

    def put_pokemon_data(self, user_id: int, pokemon_id: int, illust_no: int, get_exp: int, atk: int, res: int, defe: int, sp: int) -> Optional[int]:
        pass

    def get_pokemon_data(self, user_id: int, pokemon_id: int) -> Optional[Row]:
        pass

    def get_all_pokemon_data(self, user_id: int) -> Optional[List[Row]]:
        pass

    def put_results(self, user_id: int, pokemon_id: int, match_type: int, match_result: int) -> None:
        """
        Records the match stats (type and win/loss) for the pokemon and profile
        """
        pass

    def put_stats(self, user_id: int, exkos: int, wkos: int, timeout_wins: int, cool_kos: int, perfects: int, continues: int) -> None:
        """
        Records profile stats
        """
        pass