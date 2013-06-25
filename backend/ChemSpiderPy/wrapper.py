# -*- coding: UTF-8 -*-
'''
Created on 2013-03-08

@author: tianwei

Desc: This is a search wrapper for ChemSpider.com with ChemSpidePy module.
'''

import os
import urllib2

from django.conf import settings
from django.db.models import Q
from django.core.files import File

from chemspipy import find_one
from backend.logging import logger, loginfo
from calcore.models import SearchEngineModel


def store_image(url, name):
    """
        Store image into specific file path
        Args:
            In: url, which only include image
            Out: path, which is a relatived path
    """
    path = ""

    if url is "" or url is None:
        return path
    else:
        try:
            filename = name + ".png"
            fpath = os.path.join(settings.SEARCH_IMAGE_PATH, filename)
            path = os.path.join(settings.SEARCH_IMAGE_PATH_RE, filename)

            if os.path.exists(fpath):
                return path
            # check file already
            data = urllib2.urlopen(url).read()

            # check folder path
            if not os.path.exists(settings.SEARCH_IMAGE_PATH):
                os.makedirs(settings.SEARCH_IMAGE_PATH)

            # record file into local filesystem
            f = file(fpath, "wb")
            f.write(data)
            f.close()
            logger.debug("***filename:%s, fpath:%s, path:%s, ****" % (filename, fpath, path))
        except Exception, err:
            logger.error("*" * 20)
            logger.error(err)
            logger.error("*" * 20)
            path = ""
        return path


def show_structure(ori_str):
    """
        generate Structure from original string,
        such as C_{13}H_{18}O_{2} will be shown as the following:
        C<sub>13</sub>H<sub>18</sub>O<sub>2</sub>,
    """
    if ori_str is "" or ori_str is None:
        return ""

    ori_str = ori_str.replace("_{", "<sub>")
    ori_str = ori_str.replace("}", "</sub>")

    return "<p>" + ori_str + "</p>"


def copy_results(content, database=False):
    """
    copy result into HTML
    """
    if database:
        loginfo(p="use local database!")
    # Fill ChemSpider search result
    search_result = {"is_valid": True,
                     "content": {},
                     }

    search_result["is_valid"] = True
    if not database:
        search_result["content"]["imagepath"] = "media/" + store_image(content.imageurl, content.commonname)
        search_result["content"]["mf"] = show_structure(content.mf)
    else:
        search_result["content"]["imagepath"] = content.image.url
        search_result["content"]["mf"] = content.mf

    search_result["content"]["commonname"] = content.commonname
    search_result["content"]["inchi"] = content.inchi
    search_result["content"]["inchikey"] = content.inchikey
    search_result["content"]["averagemass"] = content.averagemass
    search_result["content"]["molecularweight"] = content.molecularweight
    search_result["content"]["monoisotopicmass"] = content.monoisotopicmass
    search_result["content"]["alogp"] = content.alogp
    search_result["content"]["xlogp"] = content.xlogp
    search_result["content"]["smiles"] = content.smiles

    return search_result


def save_search_record(content, query):
    """
    save content into database
    """
    loginfo(p="save into search engine!")

    search_result = SearchEngineModel()
    search_result.commonname = content.commonname
    search_result.mf = show_structure(content.mf)
    search_result.inchi = content.inchi
    search_result.inchikey = content.inchikey
    search_result.averagemass = content.averagemass
    search_result.molecularweight = content.molecularweight
    search_result.monoisotopicmass = content.monoisotopicmass
    search_result.alogp = content.alogp
    search_result.xlogp = content.xlogp
    search_result.smiles = content.smiles
    search_result.search_query = query

    #TODO: There we can optimize the file storage flow!
    path = os.path.join(settings.MEDIA_ROOT, store_image(content.imageurl, content.commonname))
    f = File(open(path, "r"))
    loginfo(p=f, label="file")
    search_result.image = f
    search_result.save()


def search_cheminfo(query):
    """
        Search chem info wrapper

        Args:
            In: query string
            Out: a dict for search result ,
                 which include is_valid, content(it is also a dict)
    """
    search_result = {"is_valid": True,
                     "content": {},
                     }

    if query is None or query is "":
        search_result["is_valid"] = False
        return search_result

    database_result = SearchEngineModel.objects.filter(Q(commonname__contains=query)|
                                                      Q(smiles__contains=query)|
                                                      Q(search_query__contains=query))

    if len(database_result) != 0:
        return copy_results(database_result[0], database=True)

    try:
        content = find_one(query)
        search_result = copy_results(content)
        # We should ensure the main process
        try:
            save_search_record(content, query)
        except Exception, err:
            loginfo(p=err)
            pass
    except Exception, err:
        loginfo(p=err)
        search_result["is_valid"] = False
        return search_result

    return search_result
