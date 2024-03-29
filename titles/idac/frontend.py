import json
import yaml
import jinja2
from os import path
from twisted.web.util import redirectTo
from twisted.web.http import Request
from twisted.web.server import Session

from core.frontend import FE_Base, IUserSession
from core.config import CoreConfig
from titles.idac.database import IDACData
from titles.idac.schema.profile import *
from titles.idac.schema.item import *
from titles.idac.config import IDACConfig
from titles.idac.const import IDACConstants


class IDACFrontend(FE_Base):
    def __init__(
        self, cfg: CoreConfig, environment: jinja2.Environment, cfg_dir: str
    ) -> None:
        super().__init__(cfg, environment)
        self.data = IDACData(cfg)
        self.game_cfg = IDACConfig()
        if path.exists(f"{cfg_dir}/{IDACConstants.CONFIG_NAME}"):
            self.game_cfg.update(
                yaml.safe_load(open(f"{cfg_dir}/{IDACConstants.CONFIG_NAME}"))
            )
        self.nav_name = "頭文字D THE ARCADE"
        # TODO: Add version list
        self.version = IDACConstants.VER_IDAC_SEASON_2

        self.ticket_names = {
            3: "car_dressup_points",
            5: "avatar_points",
            25: "full_tune_tickets",
            34: "full_tune_fragments",
        }

    def generate_all_tables_json(self, user_id: int):
        json_export = {}

        idac_tables = {
            profile,
            config,
            avatar,
            rank,
            stock,
            theory,
            car,
            ticket,
            story,
            episode,
            difficulty,
            course,
            trial,
            challenge,
            theory_course,
            theory_partner,
            theory_running,
            vs_info,
            stamp,
            timetrial_event
        }

        for table in idac_tables:
            sql = select(table).where(
                table.c.user == user_id,
            )

            # check if the table has a version column
            if "version" in table.c:
                sql = sql.where(table.c.version == self.version)

            # lol use the profile connection for items, dirty hack
            result = self.data.profile.execute(sql)
            data_list = result.fetchall()

            # add the list to the json export with the correct table name
            json_export[table.name] = []
            for data in data_list:
                tmp = data._asdict()
                tmp.pop("id")
                tmp.pop("user")
                json_export[table.name].append(tmp)

        return json.dumps(json_export, indent=4, default=str, ensure_ascii=False)

    def render_GET(self, request: Request) -> bytes:
        uri: str = request.uri.decode()

        template = self.environment.get_template(
            "titles/idac/frontend/idac_index.jinja"
        )
        sesh: Session = request.getSession()
        usr_sesh = IUserSession(sesh)
        user_id = usr_sesh.userId
        # user_id = usr_sesh.user_id

        # profile export
        if uri.startswith("/game/idac/export"):
            if user_id == 0:
                return redirectTo(b"/game/idac", request)

            # set the file name, content type and size to download the json
            content = self.generate_all_tables_json(user_id).encode("utf-8")
            request.responseHeaders.addRawHeader(
                b"content-type", b"application/octet-stream"
            )
            request.responseHeaders.addRawHeader(
                b"content-disposition", b"attachment; filename=idac_profile.json"
            )
            request.responseHeaders.addRawHeader(
                b"content-length", str(len(content)).encode("utf-8")
            )

            self.logger.info(f"User {user_id} exported their IDAC data")
            return content

        profile_data, tickets, rank = None, None, None
        if user_id > 0:
            profile_data = self.data.profile.get_profile(user_id, self.version)
            ticket_data = self.data.item.get_tickets(user_id)
            rank = self.data.profile.get_profile_rank(user_id, self.version)

            tickets = {
                self.ticket_names[ticket["ticket_id"]]: ticket["ticket_cnt"]
                for ticket in ticket_data
            }

        return template.render(
            title=f"{self.core_config.server.name} | {self.nav_name}",
            game_list=self.environment.globals["game_list"],
            profile=profile_data,
            tickets=tickets,
            rank=rank,
            sesh=vars(usr_sesh),
            active_page="idac",
        ).encode("utf-16")

    def render_POST(self, request: Request) -> bytes:
        pass
