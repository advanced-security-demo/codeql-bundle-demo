import json
import unittest
import requests
import logging
import re
import sys
import argparse
import os
from prance import ResolvingParser
from http.client import HTTPConnection
from time import sleep

from test import BaseTestCase


def do_post_req(mytestcase, ep, headers, payload):
    """
    Perform an actual POST request
    returns the response object r
    """
    self = mytestcase
    try:
        # print("--- Starting POST request to {}".format(ep))
        sleep(0.05)
        r = self.client.open(
            ep, method="POST", data=json.dumps(payload), headers=headers
        )
        # r = requests.post('{}'.format(ep), data=payload,
        #                   headers=headers, timeout=20, allow_redirects=False)
    except Exception as e:
        print("    Exception connecting to {} with {}".format(ep, str(e)))
        return {"status_code": -1, "content": ""}
    else:
        # print("    POST request to {} returned status {}: {}".format(ep, r.status_code, r.data))
        return r


def do_get_req(mytestcase, ep, headers):
    """
    Perform an actual GET request
    returns the response object r
    """
    self = mytestcase
    try:
        # print("--- Starting GET request to {}".format(ep))
        sleep(0.05)
        r = self.client.open(ep, method="GET", headers=headers)
        # r = requests.get('{}'.format(ep), headers=headers,
        #                  timeout=20, allow_redirects=False)
    except Exception as e:
        print("    Exception connecting to {} with {}".format(ep, str(e)))
        return {"status_code": -1, "content": ""}
    else:
        # print("    GET request to {} returned status {}: {}".format(ep,r.status_code, r.content))
        return r


def get_happyday_pattern(datatype):
    fuzzdbfile = "test/fuzz-{}.txt".format(re.sub(r"[^a-zA-Z]", "", datatype))
    fuzzdbfallbackfile = "test/fuzz-fallback.txt"
    happydaystring = ""
    if os.path.exists(fuzzdbfile):
        with open(fuzzdbfile) as f:
            happydaystring = f.readlines()[0].rstrip()
    elif os.path.exists(fuzzdbfallbackfile):
        with open(fuzzdbfallbackfile) as f:
            happydaystring = f.readlines()[0].rstrip()
    else:
        happydaystring = "AAAAAAAAAstaticfallbackoffallbackstring"
    return happydaystring


def get_fuzz_patterns(datatype):
    fuzzdbfile = "test/fuzz-{}.txt".format(re.sub(r"[^a-zA-Z]", "", datatype))
    fuzzdbfallbackfile = "test/fuzz-fallback.txt"
    lines = []
    if os.path.exists(fuzzdbfile):
        with open(fuzzdbfile) as f:
            lines = f.readlines()
    elif os.path.exists(fuzzdbfallbackfile):
        with open(fuzzdbfallbackfile) as f:
            lines = f.readlines()
    else:
        lines = "AAAAAAAAAstaticfallbackoffallbackstring"
    return lines


def generate_happy_day_url_from_pathvars(baseurl, path, pathvars):
    """
    From a given OAS3 endpoint with path parameters,
    generate 1 URL while substituting all params with happy day strings
    """
    url = "{}{}".format(baseurl, path)
    if pathvars is not None:
        for pathvar in pathvars:
            datatype = pathvar.get("schema", {}).get("type", "fallback")
            happydaystring = get_happyday_pattern(datatype)
            url = url.replace(
                "{{{}}}".format(pathvar.get("name")), happydaystring.rstrip()
            )
    return url


def generate_urls_from_pathvars(baseurl, path, pathvars):
    """
    From a given OAS3 endpoint with path parameters,
    generate all the possible URLs to fuzz
    while only substituting 1 param with all fuzzing entries
    and using happy day strings for the other parameters
    """
    urls = set()
    for pathvar in pathvars:
        if pathvar.get("in", None) == "path" and "name" in pathvar.keys():
            datatype = pathvar.get("schema", {}).get("type", "fallback")
            lines = get_fuzz_patterns(datatype)
            for line in lines:
                url = "{}{}".format(baseurl, path)
                url = url.replace("{{{}}}".format(pathvar.get("name")), line.rstrip())
                for otherpathvar in pathvars:
                    datatype = otherpathvar.get("schema", {}).get("type", "fallback")
                    happydaystring = get_happyday_pattern(datatype)
                    url = url.replace(
                        "{{{}}}".format(otherpathvar.get("name")),
                        happydaystring.rstrip(),
                    )
                urls.add(url)
    return urls


def generate_payloads_from_postvars(postvars):
    """
    From a given OAS3 dict of requestBody variables
    generate a list of payload dicts
    """
    payloads = []
    payload = {}

    for jsontype in ["int", "str", "arr", "none"]:
        for fuzzparam in postvars.keys():
            datatype = postvars.get(fuzzparam, {}).get("type", "fallback")
            lines = get_fuzz_patterns(datatype)
            for line in lines:
                payload = {}
                for param in postvars.keys():
                    datatype = postvars.get(param, {}).get("type", "")
                    happydaystring = get_happyday_pattern(datatype)
                    if param == fuzzparam:
                        if (
                            jsontype == "int"
                            or datatype == "int"
                            or datatype == "number"
                        ):
                            try:
                                payload[param] = int(line.rstrip())
                            except ValueError:
                                payload[param] = line.rstrip()
                        elif jsontype == "str":
                            payload[param] = line.rstrip()
                    else:
                        if datatype == "int" or datatype == "number":
                            try:
                                payload[param] = int(happydaystring)
                            except ValueError:
                                payload[param] = happydaystring
                        else:
                            payload[param] = happydaystring
                payloads.append(payload)
    payloads_uniq = []
    for payload in payloads:
        if payload not in payloads_uniq:
            payloads_uniq.append(payload)
    return payloads_uniq


def do_post_fuzzing(*args, **kwargs):
    baseurl = kwargs.get("baseurl", "")
    headers = kwargs.get("headers", {})
    path = kwargs.get("path", None)
    pathvars = kwargs.get("pathvars", {})
    postvars = kwargs.get("postvars", {})
    responses = kwargs.get("responses", [])
    self = kwargs.get("mytestcase", None)

    newresponses = []
    for response in responses:
        try:
            newresponses.append(int(response))
        except ValueError:
            newresponses.append(response)
    responses = newresponses

    url = generate_happy_day_url_from_pathvars(baseurl, path, pathvars)
    payloads = generate_payloads_from_postvars(postvars)

    for payload in payloads:
        with self.subTest(method="POST", url=url, payload=payload, headers=headers):
            r = do_post_req(self, url, headers, payload)
            responses.append(500)
            self.assertIn(r.status_code, responses)
    return True


def do_get_fuzzing(*args, **kwargs):
    """
    Perform fuzzing on a GET endpoint
    """
    baseurl = kwargs.get("baseurl", "")
    headers = kwargs.get("headers", {})
    path = kwargs.get("path", None)
    pathvars = kwargs.get("pathvars", {})
    responses = kwargs.get("responses", [])
    self = kwargs.get("mytestcase", None)

    urls = generate_urls_from_pathvars(baseurl, path, pathvars)
    stats = {}
    stats["path"] = path
    stats["method"] = "GET"

    newresponses = []
    for response in responses:
        try:
            newresponses.append(int(response))
        except ValueError:
            newresponses.append(response)
    responses = newresponses

    for url in urls:
        with self.subTest(method="GET", url=url, headers=headers):
            r = do_get_req(self, url, headers)
            responses.append(500)
            self.assertIn(r.status_code, responses)
    return True


def do_fuzzing(mytestcase, headers):

    self = mytestcase
    baseurl = ""

    parser = ResolvingParser("openapi/vAPI.yaml")
    spec = parser.specification  # contains fully resolved specs as a dict
    # print(json.dumps(parser.specification.get("paths").get("/employees/expenses/{expenses_id}/attachments").get("post"),indent=2))
    for path, pathvalues in spec.get("paths", {}).items():
        for method, methodvalues in pathvalues.items():
            pathvars = {}
            # postvars = {}
            if method == "get":
                if "parameters" in methodvalues.keys():
                    pathvars = methodvalues.get("parameters", {})
                    responses = list(methodvalues.get("responses", {}).keys())
                    # print("--------------------------------------------")
                    # print("GET fuzzing {}".format(path))
                    do_get_fuzzing(
                        mytestcase=self,
                        baseurl=baseurl,
                        headers=headers,
                        path=path,
                        pathvars=pathvars,
                        responses=responses,
                    )
            if method == "post":
                responses = list(methodvalues.get("responses", {}).keys())
                if (
                    "requestBody" in methodvalues.keys()
                    and "parameters" in methodvalues.keys()
                ):
                    pathvars = methodvalues.get("parameters")
                    postvars = (
                        methodvalues.get("requestBody", {})
                        .get("content", {})
                        .get("application/json", {})
                        .get("schema", {})
                        .get("properties", {})
                    )
                    # print("--------------------------------------------")
                    # print("POST fuzzing param URL {}:".format(path))
                    do_post_fuzzing(
                        mytestcase=self,
                        baseurl=baseurl,
                        headers=headers,
                        path=path,
                        pathvars=pathvars,
                        postvars=postvars,
                        responses=responses,
                    )
                elif "requestBody" in methodvalues.keys():
                    postvars = (
                        methodvalues.get("requestBody", {})
                        .get("content", {})
                        .get("application/json", {})
                        .get("schema", {})
                        .get("properties", {})
                    )
                    # print("--------------------------------------------")
                    # print("POST fuzzing non-param URL {}:".format(path))
                    do_post_fuzzing(
                        mytestcase=self,
                        baseurl=baseurl,
                        headers=headers,
                        path=path,
                        postvars=postvars,
                        responses=responses,
                    )


class TestvAPI(BaseTestCase):
    def test_unauth_fuzzing(self):
        headers = {"Content-type": "application/json"}
        do_fuzzing(self, headers)

    def test_auth_fuzzing(self):
        headers = {"Content-type": "application/json"}
        payload = {"username": "user1", "password": "pass1"}
        url = "/tokens"
        r = self.client.open(
            url, method="POST", data=json.dumps(payload), headers=headers
        )
        self.assertEqual(r.status_code, 200)
        self.assertRegex(r.json["access"]["token"]["id"], r"\w{32}")
        token = r.json["access"]["token"]["id"]
        headers["X-Auth-Token"] = token
        do_fuzzing(self, headers)


if __name__ == "__main__":
    unittest.main()
