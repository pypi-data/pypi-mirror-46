import json
import logging
import re
from datetime import datetime
from typing import List, Dict

import pandas as pd

from .actor_parsing import BallActor, CarActor
from carball.generated.api.game_pb2 import mutators_pb2 as mutators
from .goal import Goal
from .player import Player
from .team import Team
from .game_info import GameInfo

logger = logging.getLogger(__name__)

COMPONENT_ACTIVE_KEY = "TAGame.CarComponent_TA:Active"
COMPONENT_REPLICATED_ACTIVE_KEY = "TAGame.CarComponent_TA:ReplicatedActive"
BOOST_PER_SECOND = 80 * 1 / .93  # boost used per second out of 255
DATETIME_FORMATS = [
    '%Y-%m-%d %H-%M-%S',
    '%Y-%m-%d:%H-%M'
]


class Game:

    def __init__(self):
        self.file_path = None
        self.replay = None
        self.properties = None
        self.replay_id = None
        self.map = None
        self.name = None
        self.id = None
        self.datetime = None
        self.replay_version = None

        self.replay_data = None

        self.teams: List[Team] = None  # Added in parse_all_data
        self.players: List[Player] = None
        self.goals: List[Goal] = None
        self.primary_player: dict = None
        self.all_data = None

        self.frames = None
        self.kickoff_frames = None
        self.ball = None
        self.ball_type = None
        self.demos = None
        self.parties = None

    def initialize(self, file_path='', loaded_json=None, parse_replay: bool = True, clean_player_names: bool = False):
        self.file_path = file_path
        if loaded_json is None:
            with open(file_path, 'r') as f:
                self.replay = json.load(f)
        else:
            self.replay = loaded_json
        logger.debug('Loaded JSON')

        self.replay_data = self.replay['content']['body']['frames']

        # set properties
        self.properties = self.replay['header']['body']['properties']['value']
        self.replay_id = self.find_actual_value(self.properties['Id']['value'])
        if 'MapName' in self.properties:
            self.map = self.find_actual_value(self.properties['MapName']['value'])
        else:
            self.map = 'Unknown'
        self.name = self.find_actual_value(self.properties.get('ReplayName', None))
        self.match_type = self.find_actual_value(self.properties['MatchType']['value'])
        self.team_size = self.find_actual_value(self.properties['TeamSize']['value'])

        if self.name is None:
            logger.warning('Replay name not found')
        self.id = self.find_actual_value(self.properties["Id"]['value'])

        date_string = self.properties['Date']['value']['str']
        for date_format in DATETIME_FORMATS:
            try:
                self.datetime = datetime.strptime(date_string, date_format)
                break
            except ValueError:
                pass
        else:
            logger.error('Cannot parse date: ' + date_string)

        self.replay_version = self.properties.get('ReplayVersion', {}).get('value', {}).get('int', None)
        logger.info(f"version: {self.replay_version}, date: {self.datetime}")
        if self.replay_version is None:
            logger.warning('Replay version not found')

        self.players: List[Player] = self.create_players()
        self.goals: List[Goal] = self.get_goals()
        self.primary_player: dict = self.get_primary_player()

        if parse_replay:
            self.all_data = self.parse_replay()
            self.parse_all_data(self.all_data, clean_player_names)
            logger.info("Finished parsing %s" % self)

    def __repr__(self):
        team_0_name = self.teams[0].name
        team_1_name = self.teams[1].name
        team_0_score = self.teams[0].score
        team_1_score = self.teams[1].score
        return "%s: %s vs %s (%s:%s)" % (self.name, team_0_name, team_1_name, team_0_score, team_1_score)

    def create_players(self) -> List[Player]:
        players = []
        try:
            for player_stats in self.properties["PlayerStats"]["value"]["array"]:
                player = Player().parse_player_stats(player_stats["value"])
                players.append(player)
        except KeyError:
            pass
        return players

    def get_primary_player(self):
        owner_name = self.properties.get('PlayerName')
        if owner_name is not None:
            owner_name = owner_name['value']['str']
            for player in self.players:
                if player.name == owner_name:
                    return {'name': owner_name, 'id': player.online_id}
            return {'name': owner_name, 'id': None}

    def get_goals(self) -> List[Goal]:
        if "Goals" not in self.properties:
            return []

        goals = [g['value'] for g in self.properties["Goals"]["value"]["array"]]

        logger.info('Found %s goals.' % len(goals))
        logger.debug('Goals: %s' % goals)

        goals_list = []
        for goal_dict in goals:
            goal = Goal(goal_dict, self)
            goals_list.append(goal)
        return goals_list

    @staticmethod
    def find_actual_value(value_dict: dict) -> dict or int or bool or str:
        types = ['int', 'boolean', 'string', 'byte', 'str', 'name', ('flagged_int', 'int')]
        if value_dict is None:
            return None
        if 'value' in value_dict:
            value_dict = value_dict['value']
        for _type in types:
            if isinstance(_type, str):
                if _type in value_dict:
                    return value_dict[_type]
            else:
                value = value_dict
                if _type[0] in value:
                    for type_str in _type:
                        value = value[type_str]
                    return value
        else:
            return value_dict

    def parse_replay(self):
        """
        :return: all_data = {
            'player_ball_data': player_ball_data,
            'player_dicts': player_dicts,
            'team_dicts': team_dicts,
            'frames_data': frames_data,
            'cameras_data': cameras_data
            'demos_data': demos_data
        }

        player_ball_data format:
        {
        'ball': {frame_number: {pos_x, pos_y ...}, f_no2: {...} ...,}
        player_actor_id: {
            frame_number: {
                pos_x, pos_y ...,
                throttle, steer, ...,
                ping, ball_cam
            },
            f_no2: {...} ...,
        }

        currently implemented:
            inputs: posx, posy, posz, rotx, roty, rotz, vx, vy, vz, angvx, angy, angvz, boost_amt
            outputs: throttle, steer, handbrake, boost, jump, doublejump, dodge

        player_dicts  = {player_actor_id : {actor_data}, player_actor_id_2: {actor_data_2}}
        team_dicts = {team_actor_id: {actor_data, 'colour':'blue'/'orange', also includes name}
        frames_data = {frame_number: {time, delta, seconds_remaining, is_overtime, ball_has_been_hit}
        cameras_data = {player_actor_id: actor_data}
        demos_data = {frame_number: demolish_data}

        """
        player_ball_data = {'ball': {}}

        # dictionaries to contain data in frames
        player_dicts = {}  # player_actor_id: player_dict
        team_dicts = {}

        player_car_ids = {}  # player_actor_id: car_actor_id
        car_player_ids = {}  # car_actor_id: player_actor_id

        current_actor_ids = []
        current_actors = {}  # id:actor_update
        # stores car_actor_ids to collect data for at each frame
        current_car_ids_to_collect = []

        frames = self.replay_data
        frames_data = {}
        soccar_game_event_actor_id = None
        frame_number = 0
        current_goal_number = 0

        cameras_data = {}  # player_actor_id: actor_data
        demos_data = []  # frame_number: demolish_data

        game_info_actor = None
        parties = {}
        # loop through frames
        for i, frame in enumerate(frames):
            # # don't bother after last goal
            # if frame_number > last_goal_frame_number:
            #     break

            _f_time = frame["time"]
            _f_delta = frame["delta"]
            deleted_actor_ids = []
            actor_updates = []
            actor_spawns = []
            for replication in frame['replications']:
                category = list(replication['value'].keys())[0]
                if category == 'destroyed':
                    deleted_actor_ids.append(replication)
                elif category == 'updated':
                    actor_updates.append(replication)
                elif category == 'spawned':
                    actor_spawns.append(replication)
            # remove deleted actors
            for deleted_actor in deleted_actor_ids:
                deleted_actor_id = deleted_actor['actor_id']['value']
                current_actor_ids.remove(deleted_actor_id)
                current_actors.pop(deleted_actor_id)
                if deleted_actor_id in car_player_ids:
                    player_actor_id = car_player_ids[deleted_actor_id]
                    car_player_ids.pop(deleted_actor_id)
                    try:
                        player_car_ids.pop(player_actor_id)
                    except KeyError:
                        pass

            for actor_spawn in actor_spawns:
                actor_id = actor_spawn['actor_id']['value']
                current_actor_ids.append(actor_id)
                current_actors[actor_id] = {
                    'TypeName': actor_spawn['value']['spawned']['object_name'],
                    'ClassName': actor_spawn['value']['spawned']['class_name'],
                    'Name': actor_spawn['value']['spawned'].get('name', None),
                    'Id': actor_id
                }
            # apply actor updates
            for actor_update in actor_updates:
                actor_id = actor_update['actor_id']['value']
                # update_type = list(actor_update['value'].keys())[0]
                actual_update = {v['name']: self.find_actual_value(v['value']) for v in
                                 actor_update['value']['updated']}
                # TODO: process each subtype to a single value
                # add if new actor
                if actor_id not in current_actor_ids:
                    current_actor_ids.append(actor_id)
                    current_actors[actor_id] = actual_update
                else:
                    # update stuff in current_actors
                    for _k, _v in actual_update.items():
                        current_actors[actor_id][_k] = _v

            # server metadata
            if game_info_actor is None:
                for actor_id, actor_data in current_actors.items():
                    if actor_data['TypeName'].endswith(':GameReplicationInfoArchetype'):
                        game_info_actor = actor_data
                        break

            # find players and ball
            players_and_teams_data = self.parse_players_and_teams(current_actors, parties, player_dicts,
                                                                  player_ball_data, team_dicts)
            parties = players_and_teams_data["parties"]
            player_dicts = players_and_teams_data["player_dicts"]
            player_ball_data = players_and_teams_data["player_ball_data"]
            team_dicts = players_and_teams_data["team_dicts"]

            # stop data collection after goal
            REPLICATED_RB_STATE_KEY = "TAGame.RBActor_TA:ReplicatedRBState"
            try:
                if frame_number > self.goals[current_goal_number].frame_number:
                    # set all players to sleeping after goal
                    for car_actor_id in car_player_ids:
                        try:
                            car = current_actors[car_actor_id]
                            car[REPLICATED_RB_STATE_KEY]['Sleeping'] = True
                        except KeyError as e:
                            # Ignore the case where the car does not have a REPLICATED_RB_STATE_KEY
                            pass
                    current_goal_number += 1
            except IndexError:
                # after last goal.
                pass

            # gather data at this frame
            if _f_delta != 0:
                # frame stuff
                frame_data = {
                    'time': frame["time"],
                    'delta': frame["delta"],
                }
                if soccar_game_event_actor_id is None:
                    # set soccar_game_event_actor_id
                    for actor_id, actor_data in current_actors.items():
                        if actor_data["TypeName"] == "Archetypes.GameEvent.GameEvent_Soccar" \
                                or "TAGame.GameEvent_Soccar_TA:SecondsRemaining" in actor_data:
                            # TODO: Investigate if there's a less hacky way to detect GameActors with not TypeName
                            soccar_game_event_actor_id = actor_id
                            break

                frame_data['seconds_remaining'] = current_actors[soccar_game_event_actor_id].get(
                    "TAGame.GameEvent_Soccar_TA:SecondsRemaining", None)
                frame_data['replicated_seconds_remaining'] = current_actors[soccar_game_event_actor_id].get(
                    "TAGame.GameEvent_TA:ReplicatedGameStateTimeRemaining", None)
                frame_data['is_overtime'] = current_actors[soccar_game_event_actor_id].get(
                    "TAGame.GameEvent_Soccar_TA:bOverTime", None)
                frame_data['ball_has_been_hit'] = current_actors[soccar_game_event_actor_id].get(
                    "TAGame.GameEvent_Soccar_TA:bBallHasBeenHit", None)
                frames_data[frame_number] = frame_data

                # car and player stuff
                for actor_id, actor_data in current_actors.items():
                    if actor_data["TypeName"] == "Archetypes.Car.Car_Default" and \
                            "Engine.Pawn:PlayerReplicationInfo" in actor_data:
                        player_actor_id = actor_data[
                            "Engine.Pawn:PlayerReplicationInfo"]
                        # assign car player links
                        player_car_ids[player_actor_id] = actor_id
                        car_player_ids[actor_id] = player_actor_id

                        RBState = actor_data.get(
                            REPLICATED_RB_STATE_KEY, {})
                        # bDriving is missing?! TODO: Investigate bDriving in RBState
                        # car_is_driving = RBState.get("rigid_body_state", {}).get("TAGame.Vehicle_TA:bDriving", False)
                        car_is_sleeping = RBState.get("rigid_body_state", {}).get('sleeping', True)
                        # only collect data if car is driving and not sleeping
                        if not car_is_sleeping:
                            current_car_ids_to_collect.append(actor_id)

                            data_dict = CarActor.get_data_dict(actor_data, version=self.replay_version)
                            # save data from here
                            player_ball_data[player_actor_id][frame_number] = data_dict

                        # get demo data
                        if "TAGame.Car_TA:ReplicatedDemolish" in actor_data:

                            demo_data = actor_data["TAGame.Car_TA:ReplicatedDemolish"]['demolish']
                            # add attacker and victim player ids
                            attacker_car_id = demo_data["attacker_actor_id"]
                            victim_car_id = demo_data["victim_actor_id"]
                            if attacker_car_id != -1 and victim_car_id != -1 and \
                                    attacker_car_id < 1e9 and victim_car_id < 1e9:
                                # Filter out weird stuff where it's not a demo
                                # frame 1 of 0732D41D4AF83D610AE2A988ACBC977A (rlcs season 4 eu)
                                attacker_player_id = car_player_ids[attacker_car_id]
                                victim_player_id = car_player_ids[victim_car_id]
                                demo_data["attacker_player_id"] = attacker_player_id
                                demo_data["victim_player_id"] = victim_player_id
                                # add frame_number
                                demo_data['frame_number'] = frame_number
                                demos_data.append(demo_data)
                                logger.debug('ReplicatedDemolish: Att: %s, Def: %s' %
                                             (attacker_player_id, victim_player_id))
                                logger.debug('RepDemo Names: Att: %s. Def: %s' %
                                             (player_dicts[attacker_player_id]['name'],
                                              player_dicts[victim_player_id]['name']))
                                actor_data.pop("TAGame.Car_TA:ReplicatedDemolish")

                    elif actor_data["TypeName"] == "Archetypes.Ball.Ball_Default":
                        if actor_data.get('TAGame.RBActor_TA:bIgnoreSyncing', False):
                            continue
                        self.ball_type = mutators.DEFAULT
                        # RBState = actor_data.get(REPLICATED_RB_STATE_KEY, {})
                        # ball_is_sleeping = RBState.get('Sleeping', True)
                        data_dict = BallActor.get_data_dict(actor_data, version=self.replay_version)
                        player_ball_data['ball'][frame_number] = data_dict
                    elif actor_data["TypeName"] == "Archetypes.Ball.Ball_Basketball" or \
                            actor_data["TypeName"] == "Archetypes.Ball.Ball_BasketBall":
                        if actor_data.get('TAGame.RBActor_TA:bIgnoreSyncing', False):
                            continue
                        self.ball_type = mutators.BASKETBALL
                        data_dict = BallActor.get_data_dict(actor_data, version=self.replay_version)
                        player_ball_data['ball'][frame_number] = data_dict
                    elif actor_data["TypeName"] == "Archetypes.Ball.Ball_Puck":
                        if actor_data.get('TAGame.RBActor_TA:bIgnoreSyncing', False):
                            continue
                        self.ball_type = mutators.PUCK
                        data_dict = BallActor.get_data_dict(actor_data, version=self.replay_version)
                        player_ball_data['ball'][frame_number] = data_dict
                    elif actor_data["TypeName"] == "Archetypes.Ball.CubeBall":
                        if actor_data.get('TAGame.RBActor_TA:bIgnoreSyncing', False):
                            continue
                        self.ball_type = mutators.CUBEBALL
                        data_dict = BallActor.get_data_dict(actor_data, version=self.replay_version)
                        player_ball_data['ball'][frame_number] = data_dict
                    elif actor_data["TypeName"] == "Archetypes.Ball.Ball_Breakout":
                        if actor_data.get('TAGame.RBActor_TA:bIgnoreSyncing', False):
                            continue
                        self.ball_type = mutators.BREAKOUT
                        data_dict = BallActor.get_data_dict(actor_data, version=self.replay_version)
                        player_ball_data['ball'][frame_number] = data_dict

                for actor_id, actor_data in current_actors.items():
                    if actor_data["TypeName"] == "TAGame.Default__CameraSettingsActor_TA" and \
                            "TAGame.CameraSettingsActor_TA:PRI" in actor_data:
                        player_actor_id = actor_data["TAGame.CameraSettingsActor_TA:PRI"]  # may need to try another key
                        # add camera settings
                        if player_actor_id not in cameras_data and \
                                "TAGame.CameraSettingsActor_TA:ProfileSettings" in actor_data:
                            cameras_data[player_actor_id] = actor_data["TAGame.CameraSettingsActor_TA:ProfileSettings"]
                        # add ball cam to inputs
                        ball_cam = actor_data.get("TAGame.CameraSettingsActor_TA:bUsingSecondaryCamera", None)
                        try:
                            player_ball_data[player_actor_id][frame_number]['ball_cam'] = ball_cam
                        except KeyError:
                            # key error due to frame_number not in inputs
                            # ignore as no point knowing
                            pass
                    elif actor_data["TypeName"] == "TAGame.Default__PRI_TA" and \
                            "TAGame.PRI_TA:CameraSettings" in actor_data:
                        # oldstyle camera settings
                        if actor_id not in cameras_data:
                            cameras_data[actor_id] = actor_data["TAGame.PRI_TA:CameraSettings"]
                        ball_cam = actor_data.get("TAGame.CameraSettingsActor_TA:bUsingSecondaryCamera", None)
                        try:
                            player_ball_data[actor_id][frame_number]['ball_cam'] = ball_cam
                        except KeyError:
                            # key error due to frame_number not in inputs
                            # ignore as no point knowing
                            pass
                    elif actor_data["TypeName"] == "Archetypes.CarComponents.CarComponent_Boost":
                        car_actor_id = actor_data.get(
                            "TAGame.CarComponent_TA:Vehicle", None)
                        if car_actor_id is not None:
                            if car_actor_id in current_car_ids_to_collect:
                                player_actor_id = car_player_ids[car_actor_id]
                                boost_is_active_random_int = actor_data.get(
                                    COMPONENT_ACTIVE_KEY,
                                    actor_data.get(COMPONENT_REPLICATED_ACTIVE_KEY, False))
                                # boost_is_active when random_int is odd?!
                                boost_is_active = (boost_is_active_random_int % 2 == 1)
                                if boost_is_active:
                                    # manually decrease car boost amount (not shown in replay)
                                    # i assume game calculates the decrease itself similarly
                                    boost_amount = max(0,
                                                       actor_data.get(
                                                           "TAGame.CarComponent_Boost_TA:ReplicatedBoostAmount", 0) -
                                                       _f_delta * BOOST_PER_SECOND)
                                    actor_data["TAGame.CarComponent_Boost_TA:ReplicatedBoostAmount"] = boost_amount
                                else:
                                    boost_amount = actor_data.get("TAGame.CarComponent_Boost_TA:ReplicatedBoostAmount",
                                                                  None)

                                player_ball_data[player_actor_id][frame_number]['boost'] = boost_amount
                                player_ball_data[player_actor_id][frame_number]['boost_active'] = boost_is_active
                    elif actor_data["TypeName"] == "Archetypes.CarComponents.CarComponent_Jump":
                        car_actor_id = actor_data.get(
                            "TAGame.CarComponent_TA:Vehicle", None)
                        if car_actor_id is not None:
                            if car_actor_id in current_car_ids_to_collect:
                                player_actor_id = car_player_ids[car_actor_id]
                                jump_is_active = actor_data.get(
                                    COMPONENT_ACTIVE_KEY,
                                    actor_data.get(COMPONENT_REPLICATED_ACTIVE_KEY, False))
                                player_ball_data[player_actor_id][frame_number]['jump_active'] = jump_is_active
                    elif actor_data["TypeName"] == "Archetypes.CarComponents.CarComponent_DoubleJump":
                        car_actor_id = actor_data.get(
                            "TAGame.CarComponent_TA:Vehicle", None)
                        if car_actor_id is not None:
                            if car_actor_id in current_car_ids_to_collect:
                                player_actor_id = car_player_ids[car_actor_id]
                                double_jump_is_active = actor_data.get(
                                    COMPONENT_ACTIVE_KEY,
                                    actor_data.get(COMPONENT_REPLICATED_ACTIVE_KEY, False))
                                player_ball_data[player_actor_id][frame_number][
                                    'double_jump_active'] = double_jump_is_active
                    elif actor_data["TypeName"] == "Archetypes.CarComponents.CarComponent_Dodge":
                        car_actor_id = actor_data.get(
                            "TAGame.CarComponent_TA:Vehicle", None)
                        if car_actor_id is not None:
                            if car_actor_id in current_car_ids_to_collect:
                                player_actor_id = car_player_ids[car_actor_id]
                                dodge_is_active = actor_data.get(
                                    COMPONENT_ACTIVE_KEY,
                                    actor_data.get(COMPONENT_REPLICATED_ACTIVE_KEY, False))
                                player_ball_data[player_actor_id][frame_number]['dodge_active'] = dodge_is_active
                    elif actor_data["ClassName"] == "TAGame.VehiclePickup_Boost_TA":
                        REPLICATED_PICKUP_KEY = "TAGame.VehiclePickup_TA:ReplicatedPickupData"
                        if REPLICATED_PICKUP_KEY in actor_data and \
                                actor_data[REPLICATED_PICKUP_KEY] != -1 and \
                                'instigator_id' in actor_data[REPLICATED_PICKUP_KEY]['pickup']:
                            car_actor_id = actor_data[REPLICATED_PICKUP_KEY]['pickup']['instigator_id']
                            if car_actor_id in car_player_ids:
                                player_actor_id = car_player_ids[car_actor_id]
                                if frame_number in player_ball_data[player_actor_id]:
                                    player_ball_data[player_actor_id][frame_number]['boost_collect'] = True
                                    # TODO: Investigate and fix random imaginary boost collects
                                # set to false after acknowledging it's turned True
                                # it does not turn back false immediately although boost is only collected once.
                                # using actor_id!=-1
                                actor_data[REPLICATED_PICKUP_KEY]['pickup']["instigator_id"] = -1

                # rumble items
                for actor_id, actor_data in current_actors.items():
                    # rumble item count down
                    if actor_data["TypeName"] == "TAGame.Default__PRI_TA" and \
                            "TAGame.PRI_TA:TimeTillItem" in actor_data:
                        time_till_item = actor_data['TAGame.PRI_TA:TimeTillItem']
                        if frame_number in player_ball_data[actor_id]:
                            player_ball_data[actor_id][frame_number]['time_till_power_up'] = time_till_item

                    # rumble item / activated
                    elif actor_data['TypeName'].startswith('Archetypes.SpecialPickups.SpecialPickup_'):
                        car_actor_id = actor_data.get('TAGame.CarComponent_TA:Vehicle', None)
                        if car_actor_id is not None and car_actor_id in current_car_ids_to_collect:
                            player_actor_id = car_player_ids[car_actor_id]
                            item_name = actor_data['TypeName'] \
                                .replace('Archetypes.SpecialPickups.SpecialPickup_', '')
                            # CamelCase to snake_case
                            item_name = re.sub('([A-Z]+)', r'_\1', item_name).lower()[1:]
                            # item is active when this is odd
                            item_active = actor_data.get(COMPONENT_REPLICATED_ACTIVE_KEY, 0) % 2 == 1

                            player_ball_data[player_actor_id][frame_number]['power_up'] = item_name
                            player_ball_data[player_actor_id][frame_number]['power_up_active'] = item_active

                for player_actor_id in player_dicts:
                    actor_data = current_actors.get(player_actor_id, None)
                    if actor_data is None:
                        continue
                    if frame_number in player_ball_data[player_actor_id]:
                        player_ball_data[player_actor_id][frame_number]['ping'] = actor_data.get(
                            "Engine.PlayerReplicationInfo:Ping", None)
                    else:
                        player_ball_data[player_actor_id][frame_number] = {
                            'ping': actor_data.get("Engine.PlayerReplicationInfo:Ping", None)}

            current_car_ids_to_collect = []  # reset ids for next frame
            frame_number += 1

        all_data = {
            'player_ball_data': player_ball_data,
            'player_dicts': player_dicts,
            'team_dicts': team_dicts,
            'frames_data': frames_data,
            'cameras_data': cameras_data,
            'demos_data': demos_data,
            'game_info_actor': game_info_actor,
            'soccar_game_event_actor': current_actors[soccar_game_event_actor_id],
            'parties': parties
        }

        return all_data

    def parse_players_and_teams(self, current_actors, parties, player_dicts, player_ball_data, team_dicts) -> Dict:
        """
              :return: players_and_team_data = {
                  'parties': parties,
                  'player_dicts': player_dicts,
                  'player_ball_data': player_ball_data,
                  'team_dicts': team_dicts,
              }
        """

        for actor_id, actor_data in current_actors.items():
            if actor_data["TypeName"] == "TAGame.Default__PRI_TA" \
                    and "Engine.PlayerReplicationInfo:PlayerName" in actor_data:

                player_dict = {
                    'name': actor_data["Engine.PlayerReplicationInfo:PlayerName"],
                }
                # Conditionally add ['team'] key to player_dict
                player_team = actor_data.get("Engine.PlayerReplicationInfo:Team", None)
                if player_team is not None and player_team != -1:
                    player_dict['team'] = player_team

                if "TAGame.PRI_TA:PartyLeader" in actor_data:
                    try:
                        actor_type = \
                            list(actor_data["Engine.PlayerReplicationInfo:UniqueId"]['unique_id'][
                                     'remote_id'].keys())[
                                0]

                        # handle UniqueID for plays_station and switch
                        if actor_type == "play_station" or actor_type == "psy_net":
                            actor_name = actor_data["Engine.PlayerReplicationInfo:PlayerName"]
                            for player_stat in self.properties['PlayerStats']['value']["array"]:
                                if actor_name == player_stat['value']['Name']['value']['str']:
                                    unique_id = str(player_stat['value']['OnlineID']['value']['q_word'])
                        else:
                            unique_id = str(
                                actor_data['Engine.PlayerReplicationInfo:UniqueId']['unique_id']['remote_id'][actor_type])

                        # only process if party_leader id exists
                        if "party_leader" in actor_data["TAGame.PRI_TA:PartyLeader"] and \
                                "id" in actor_data["TAGame.PRI_TA:PartyLeader"]["party_leader"]:
                            leader_actor_type = list(
                                actor_data["TAGame.PRI_TA:PartyLeader"]["party_leader"]["id"][0].keys()
                            )[0]
                            if leader_actor_type == "play_station" or leader_actor_type == "psy_net":
                                leader_name = actor_data[
                                    "TAGame.PRI_TA:PartyLeader"
                                ]["party_leader"]["id"][0][leader_actor_type][0]

                                for player_stat in self.properties['PlayerStats']['value']["array"]:
                                    if leader_name == player_stat['value']['Name']['value']['str']:
                                        leader = str(player_stat['value']['OnlineID']['value']['q_word'])

                            else:  # leader is not using play_station nor switch (ie. xbox or steam)
                                leader = str(
                                    actor_data[
                                        "TAGame.PRI_TA:PartyLeader"
                                    ]["party_leader"]["id"][0][leader_actor_type]
                                )

                            if leader in parties:
                                if unique_id not in parties[leader]:
                                    parties[leader].append(unique_id)
                            else:
                                parties[leader] = [unique_id]

                    except KeyError:
                        logger.warning('Could not get party leader for actor id: ' + str(actor_id))

                if actor_id not in player_dicts:
                    # add new player
                    player_dicts[actor_id] = player_dict

                    logger.debug('Found player actor: %s (id: %s)' % (player_dict['name'], actor_id))
                    player_ball_data[actor_id] = {}
                else:
                    # update player_dicts
                    for _k, _v in {**actor_data, **player_dict}.items():
                        player_dicts[actor_id][_k] = _v
            elif actor_data["ClassName"] == "TAGame.Team_Soccar_TA":
                team_dicts[actor_id] = actor_data
                team_dicts[actor_id]['colour'] = 'blue' if actor_data[
                                                               "TypeName"] == "Archetypes.Teams.Team0" else 'orange'

        players_and_team_data = {
            'parties': parties,
            'player_dicts': player_dicts,
            'player_ball_data': player_ball_data,
            'team_dicts': team_dicts
        }

        return players_and_team_data

    def parse_all_data(self, all_data, clean_player_names: bool) -> None:
        """
        Finishes parsing after frame-parsing is done.
        E.g. Adds players not found in MatchStats metadata
        :param all_data: Dict returned by parse_replay
        :return:
        """
        # GAME INFO
        self.game_info = GameInfo().parse_game_info_actor(all_data['game_info_actor'],
                                                          all_data['soccar_game_event_actor'],
                                                          self.replay['content']['body']['objects'])

        # TEAMS
        self.teams = []
        for team_id, team_data in all_data['team_dicts'].items():
            team = Team().parse_team_data(team_data)
            self.teams.append(team)

        # PLAYERS
        player_actor_id_player_dict = {}  # player_actor_id: Player
        for _player_actor_id, _player_data in all_data['player_dicts'].items():
            if "TAGame.PRI_TA:MatchScore" not in _player_data:
                logger.warning(f"Player {_player_data['name']} as player has no MatchScore.")

            found_player = None
            for player in self.players:
                # if player leaves early, won't be created (as not found in metadata's player_stats)
                if _player_data['name'] == player.name:
                    found_player = player
                    player_actor_id_player_dict[_player_actor_id] = found_player
                    found_player.parse_actor_data(_player_data)  # just add extra stuff
                    break
            if found_player is None:
                # player not in endgame stats, create new player
                try:
                    found_player = Player().create_from_actor_data(_player_data, self.teams)
                except KeyError as e:
                    # KeyError: 'Engine.PlayerReplicationInfo:Team'
                    # in `team_actor_id = actor_data["Engine.PlayerReplicationInfo:Team"]`
                    # Player never actually joins the game.
                    if 'Engine.PlayerReplicationInfo:Team' not in _player_data:
                        logger.warning(f"Ignoring player: {_player_data['name']} as player has no team.")
                        continue
                    raise e
                self.players.append(found_player)
                player_actor_id_player_dict[_player_actor_id] = found_player

                # check if any goals are playerless and belong to this newly-created player
                for goal in self.goals:
                    if not goal.player and goal.player_name == found_player.name:
                        goal.player = found_player

            found_player.parse_data(all_data['player_ball_data'][_player_actor_id])
            # camera_settings might not exist (see 0AF8AC734890E6D3995B829E474F9924)
            found_player.get_camera_settings(all_data['cameras_data'].get(_player_actor_id, {}).get('cam_settings', {}))

            for team in self.teams:
                if found_player.is_orange == team.is_orange:
                    team.add_player(found_player)

            if clean_player_names:
                cleaned_player_name = re.sub(r'[^\x00-\x7f]', r'', found_player.name).strip()  # Support ASCII only
                if cleaned_player_name != found_player.name:
                    logger.warning(f"Cleaned player name to ASCII-only. From: {found_player.name} to: {cleaned_player_name}")
                    found_player.name = cleaned_player_name

        # GOAL - add player if not found earlier (ie player just created)
        for goal in self.goals:
            if goal.player is None:
                goal.player = goal.get_player(self)

        # BALL
        self.ball = pd.DataFrame.from_dict(self.all_data['player_ball_data']['ball'], orient='index')

        # FRAMES
        self.frames = pd.DataFrame.from_dict(self.all_data['frames_data'], orient='index')

        # DEMOS
        self.demos = []
        for _demo_data in all_data['demos_data']:
            demo = {
                'frame_number': _demo_data['frame_number'],
                'attacker': player_actor_id_player_dict[_demo_data['attacker_player_id']],
                'victim': player_actor_id_player_dict[_demo_data['victim_player_id']],
                'attacker_vel': (_demo_data["attacker_velocity"]["x"],
                                 _demo_data["attacker_velocity"]["y"],
                                 _demo_data["attacker_velocity"]["z"],),
                'victim_vel': (_demo_data["victim_velocity"]["x"],
                               _demo_data["victim_velocity"]["y"],
                               _demo_data["victim_velocity"]["z"],),
            }
            self.demos.append(demo)

        # PARTIES
        self.parties = all_data['parties']

        del self.replay_data
        del self.replay
        del self.all_data
