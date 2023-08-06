#!/usr/bin/env python
# -*- coding: utf-8 -*-

from versify.model.Testament import Testament


class Version:
    def __init__(self, name, code):
        self.name = name
        self.code = code
        self.testaments = []

    def get_testaments(self, dbt):
        t = []
        url = dbt.get_api_url("/library/volume", {"language_family_code": dbt.language, "media": "text"})
        testaments = dbt.get_request(url)
        for testament in testaments:
            if self.name != testament["version_code"]:
                continue
            t.append(Testament(testament['volume_name'],
                               testament['dam_id'],
                               testament['collection_code'],
                               self))
        return t
