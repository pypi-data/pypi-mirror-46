#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Pybeeryaml
# Copyright (C) 2018  TROUVERIE Joachim <joachim.trouverie@linoame.fr>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from keyword import iskeyword

from yaml import safe_load

from pybeeryaml.fermentable import Fermentable
from pybeeryaml.hop import Hop
from pybeeryaml.mash import MashProfile, MashStep
from pybeeryaml.meta import BeerComponent
from pybeeryaml.misc import Misc
from pybeeryaml.style import Style
from pybeeryaml.water import Water
from pybeeryaml.yeast import Yeast


class Recipe(BeerComponent):
    """Recipe model"""

    def __init__(
        self,
        name,
        type,
        style,
        brewer,
        batch_size,
        boil_size,
        boil_time,
        **data: dict
    ):
        super().__init__()
        self.name = name
        self.type = type
        self.style = style
        self.brewer = brewer
        self.batch_size = batch_size
        self.boil_size = boil_size
        self.boil_time = boil_time

        self.set(data)

        if isinstance(self.style, dict):
            self.style = Style(**data["style"])

        hops = Recipe.flatten(data.get("hops", {}))
        self.hops = [Hop(**hdata) for hdata in hops]

        yeasts = Recipe.flatten(data.get("yeasts", {}))
        self.yeasts = [Yeast(**ydata) for ydata in yeasts]

        ferments = Recipe.flatten(data.get("fermentables", {}))
        self.fermentables = [Fermentable(**fdata) for fdata in ferments]

        miscs = Recipe.flatten(data.get("miscs", {}))
        self.miscs = [Misc(**mdata) for mdata in miscs]

        profile = data.get("mash", {"name": "mash", "grain_temp": 25})
        self.mash = MashProfile(**profile)

        steps = []
        if hasattr(self.mash, "mash_steps"):
            msdata = Recipe.flatten(self.mash.mash_steps)
            for mash_step in msdata:
                steps.append(MashStep(**mash_step))

        self.mash.mash_steps = steps

        waters = Recipe.flatten(data.get("waters", {}))
        self.waters = [Water(wdata) for wdata in waters]

    @classmethod
    def flatten(cls, data: dict) -> list:
        """Flatten yaml dict"""
        output = []
        for key, value in data.items():
            if isinstance(value, dict):
                if "name" not in value:
                    value["name"] = key

                for vkey, vvalue in value.items():
                    if iskeyword(vkey):
                        value["beeryaml_{}".format(vkey)] = vvalue
                        del value[vkey]

            output.append(value)
        return output

    def to_yaml(self) -> dict:
        """Convert object to YAML dict"""
        output = {}

        for key, value in self.__dict__.items():
            if key.startswith("_"):
                continue
            elif key.startswith("beeryaml_"):
                key = key[9:]

            if value:
                if isinstance(value, BeerComponent) and key != "mash":
                    data = value.to_yaml()
                    output.update(data)
                elif isinstance(value, list):
                    output[key] = {}
                    for elt in value:
                        output[key].update(elt.to_yaml())
                else:
                    output[key] = value

        # mash
        output["mash"] = self.mash.to_yaml()

        return output

    @classmethod
    def from_file(cls, filepath: str):
        """Create recipe from YAML file"""
        with open(filepath, "r") as fi:
            data = safe_load(fi.read())
        return cls(**data)

    @classmethod
    def from_yaml(cls, data: str):
        """Create recipe from YAML data

        :param data: YAML recipe data
        """
        return cls(**safe_load(data))
