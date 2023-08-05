import logging

from aiopvapi.helpers.aiorequest import PvApiError
from aiopvapi.helpers.constants import ATTR_ROOM_ID, ATTR_POSITION
from aiopvapi.resources.scene import Scene as PvScene
from aiopvapi.resources.shade import BaseShade
from aiopvapi.scene_members import SceneMembers


# from pv_prompt.glob import VERBOSE
from pv_prompt.base_prompts import (
    PvPrompt,
    Command,
    InvalidIdException,
    PvResourcePrompt,
    BasePrompt,
    YesNoPrompt,
)
from pv_prompt.helpers import spinner
from pv_prompt.settings import ATTR_VERBOSITY, GLOBALS

from pv_prompt.print_output import (
    info,
    print_scenes,
    warn,
    print_resource_data,
    print_table,
    print_shade_data,
    print_dict,
    print_key_values,
)
from pv_prompt.resource_cache import HubCache
from pv_prompt.shades import Position, Pos

LOGGER = logging.getLogger(__name__)


class Scenes(PvPrompt):
    def __init__(self, request, hub_cache: HubCache):
        super().__init__(request, hub_cache)
        self.api_resource = hub_cache.scenes
        self.register_commands(
            {
                "l": Command(function_=self.list_scenes),
                "a": Command(function_=self.activate_scene),
                "s": Command(function_=self.select_scene),
                "c": Command(function_=self.create_scene),
            }
        )

    async def list_scenes(self, *args, **kwargs):
        info("Getting scenes...")

        print_scenes(self.hub_cache.scenes, self.hub_cache.rooms)

    async def activate_scene(self, *args, **kwargs):
        try:
            _scene = await self.hub_cache.scenes.select_resource()

            await _scene.activate()

        except InvalidIdException as err:
            warn(err)
        except PvApiError as err:
            warn(err)

    async def select_scene(self, *args, **kwargs):
        try:
            pv_scene = await self.hub_cache.scenes.select_resource()
            scene = Scene(pv_scene, self.request, self.hub_cache)
            await scene.current_prompt()
        except InvalidIdException as err:
            warn(err)

    async def create_scene(self, *args, **kwargs):
        create_scene = CreateScene(self.request, self.hub_cache)
        await create_scene.current_prompt()


class CreateScene(PvPrompt):
    """Create scene context."""

    def __init__(self, request, hub_cache: HubCache):
        super().__init__(request, hub_cache)
        self.api_resource = hub_cache.scenes
        self.register_commands(
            {
                "r": Command(function_=self.select_room),
                "s": Command(function_=self.add_shade),
                "n": Command(function_=self.enter_name),
                "c": Command(function_=self.create_scene),
            }
        )
        self._room = None
        self._scene_name = None
        self._scene = None

    async def print_selection(self):
        """Print selection."""
        if self._room:
            print_table("room:", self._room.name, self._room.id)
        if self._scene_name:
            print_table("scene name:", self._scene_name)

    async def create_scene(self, *args, **kwargs):
        """Create an empty scene."""
        info("Creating an empty scene")
        # await self.select_room(default=self._room)
        await self.enter_name(default=self._scene_name)

        scenes_obj = self.hub_cache.scenes.api_entry_point
        _scene = await scenes_obj.create_scene(self._room.id, self._scene_name)
        self._scene = PvScene(_scene, self.request)
        if GLOBALS[ATTR_VERBOSITY]:
            print_dict(_scene)
        # update the scene cache.
        await self.hub_cache.scenes.get_resource()

    async def select_room(self, *args, **kwargs):
        default = kwargs.get("default", "")
        """Select a room."""
        print_resource_data(self.hub_cache.rooms)
        try:
            self._room = await self.hub_cache.rooms.select_resource(
                default=default
            )
            await self.print_selection()
        except InvalidIdException as err:
            warn(err)

    async def enter_name(self, *args, **kwargs):
        """Define scene name."""
        default = kwargs.get("default", "")
        base = BasePrompt()
        self._scene_name = await base.current_prompt(
            prompt_="Enter a scene name: ", autoreturn=True, default=default
        )
        await self.print_selection()

    async def add_shade(self, *args, **kwargs):
        print_shade_data(self.hub_cache.shades)

        pv_shade = None
        try:
            pv_shade = await self.hub_cache.shades.select_resource()
        except InvalidIdException as err:
            warn(err)

        scene_position = ScenePosition(
            self._scene, pv_shade, self.request, self.hub_cache
        )
        await scene_position.current_prompt("Choose a scene position.")


class Scene(PvResourcePrompt):
    """Scene context."""

    def __init__(self, scene: PvScene, request, hub_cache):
        super().__init__(scene, request, hub_cache)
        self._prompt = "scene {} {}:".format(scene.id, scene.name)
        self.register_commands(
            {
                "a": Command(function_=self.add_shade_to_scene),
                "l": Command(function_=self.list_available_shades),
                # "m": Command(function_=self.show_members)
            }
        )

    async def add_shade_to_scene(self, *args, **kwargs):
        print_shade_data(self.hub_cache.shades.list_resources())
        shade = await self.hub_cache.shades.select_resource()
        _scene_id = self.pv_resource.id

        _spinner = spinner("Getting current shade position")
        _get_position = _spinner(shade.get_current_position)
        _position = await _get_position()

        print_key_values("Current shade position", _position)

        use_current = await YesNoPrompt().current_prompt(
            "Use current position ?"
        )

        if not use_current:
            pos = Pos(shade, self.request, self.hub_cache)
            await pos.list_positions()
            await pos.put_values()
            _position = pos.position

        await self._create_scene_member(_position, shade)

    @spinner("Creating scene")
    async def _create_scene_member(self, position, shade: BaseShade):
        await (SceneMembers(self.request)).create_scene_member(
            position, self.pv_resource.id, shade.id
        )

    async def list_available_shades(self, *args, **kwargs):
        room_id = self.pv_resource.room_id
        LOGGER.debug("room id: %s", room_id)

        def filter(item):
            if item._raw_data.get(ATTR_ROOM_ID) == room_id:
                LOGGER.debug("Match")
                return True
            LOGGER.debug("No match")
            return False

        print_shade_data(self.hub_cache.shades.list_resources(filter=filter))


class ScenePosition(PvPrompt):
    def __init__(self, scene: PvScene, shade: BaseShade, request, hub_cache):
        super().__init__(request, hub_cache)
        self._scene = scene
        self._shade = shade
        self._shade_position = Pos(shade, request, hub_cache)

    async def save_scene(self, *args, **kwargs):
        await self._shade_position.put_values()
        await (SceneMembers(self.request)).create_scene_member(
            self._shade_position.position, self._scene.id, self._shade.id
        )

    async def current_prompt(
        self,
        prompt_=None,
        toolbar=None,
        autocomplete=None,
        autoreturn=False,
        default="",
    ):
        await self._shade_position.list_positions()

        await self.save_scene()

        await super().current_prompt()
